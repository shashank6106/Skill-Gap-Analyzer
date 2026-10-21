"""
MongoDB Aggregation Pipelines executed via PyMongo.
Demonstrates:
- $unwind (flattening arrays)
- $group (computing counts, averages, min/max)
- $sort, $limit, $project
- $lookup (NoSQL foreign collection joins)
- $match (filtering documents prior to grouping)
"""

from typing import List, Dict, Any, Tuple
from database.db_connection import get_database


def get_system_kpis() -> Dict[str, Any]:
    """
    Computes top-level counts and averages directly from MongoDB.
    """
    db = get_database()
    total_users = db["users"].count_documents({})
    total_resumes = db["resumes"].count_documents({})
    total_jobs = db["jobs"].count_documents({})
    total_analyses = db["analyses"].count_documents({})

    # Compute average match score across all analyses via aggregation
    pipeline = [
        {
            "$group": {
                "_id": None,
                "avg_score": {"$avg": "$match_score"},
                "min_score": {"$min": "$match_score"},
                "max_score": {"$max": "$match_score"}
            }
        }
    ]
    cursor = list(db["analyses"].aggregate(pipeline))
    avg_score = round(cursor[0]["avg_score"], 1) if cursor and cursor[0].get("avg_score") is not None else 0.0
    min_score = round(cursor[0]["min_score"], 1) if cursor and cursor[0].get("min_score") is not None else 0.0
    max_score = round(cursor[0]["max_score"], 1) if cursor and cursor[0].get("max_score") is not None else 0.0

    return {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "total_jobs": total_jobs,
        "total_analyses": total_analyses,
        "avg_score": avg_score,
        "min_score": min_score,
        "max_score": max_score
    }


def get_most_matched_skills(limit: int = 10) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Aggregation Pipeline 1:
    Identifies which candidate skills most frequently match employer job postings.
    Returns: (results, raw_pipeline_definition)
    """
    pipeline = [
        {"$unwind": "$matched_skills"},
        {
            "$group": {
                "_id": "$matched_skills",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": limit},
        {
            "$project": {
                "_id": 0,
                "skill": "$_id",
                "count": 1
            }
        }
    ]
    db = get_database()
    results = list(db["analyses"].aggregate(pipeline))
    return results, pipeline


def get_most_common_missing_skills(limit: int = 10) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Aggregation Pipeline 2:
    Identifies the most frequent skill gaps among applicants.
    Returns: (results, raw_pipeline_definition)
    """
    pipeline = [
        {"$unwind": "$missing_skills"},
        {
            "$group": {
                "_id": "$missing_skills",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": limit},
        {
            "$project": {
                "_id": 0,
                "skill": "$_id",
                "gap_count": "$count"
            }
        }
    ]
    db = get_database()
    results = list(db["analyses"].aggregate(pipeline))
    return results, pipeline


def get_most_demanded_job_skills(limit: int = 10) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Aggregation Pipeline 3:
    Determines the top demanded skills across all job listings.
    Returns: (results, raw_pipeline_definition)
    """
    pipeline = [
        {"$unwind": "$required_skills"},
        {
            "$group": {
                "_id": "$required_skills",
                "frequency": {"$sum": 1}
            }
        },
        {"$sort": {"frequency": -1}},
        {"$limit": limit},
        {
            "$project": {
                "_id": 0,
                "skill": "$_id",
                "demand_frequency": "$frequency"
            }
        }
    ]
    db = get_database()
    results = list(db["jobs"].aggregate(pipeline))
    return results, pipeline


def get_job_performance_breakdown() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Aggregation Pipeline 4:
    Demonstrates $lookup (NoSQL join) between 'analyses' and 'jobs'.
    Computes average match score and applicant volume per job opening.
    Returns: (results, raw_pipeline_definition)
    """
    pipeline = [
        {
            "$lookup": {
                "from": "jobs",
                "localField": "job_id",
                "foreignField": "job_id",
                "as": "job_details"
            }
        },
        {"$unwind": "$job_details"},
        {
            "$group": {
                "_id": "$job_id",
                "job_title": {"$first": "$job_details.title"},
                "company": {"$first": "$job_details.company"},
                "avg_match_score": {"$avg": "$match_score"},
                "total_evaluations": {"$sum": 1},
                "highest_score": {"$max": "$match_score"}
            }
        },
        {"$sort": {"avg_match_score": -1}},
        {
            "$project": {
                "_id": 0,
                "job_id": "$_id",
                "job_title": 1,
                "company": 1,
                "avg_match_score": {"$round": ["$avg_match_score", 1]},
                "highest_score": 1,
                "total_evaluations": 1
            }
        }
    ]
    db = get_database()
    results = list(db["analyses"].aggregate(pipeline))
    return results, pipeline


def get_score_distribution_aggregation() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Aggregation Pipeline 5:
    Buckets match scores into ranges (<40%, 40-59%, 60-79%, 80-100%).
    Demonstrates $bucket operator.
    Returns: (results, raw_pipeline_definition)
    """
    pipeline = [
        {
            "$bucket": {
                "groupBy": "$match_score",
                "boundaries": [0, 40, 60, 80, 101],
                "default": "Other",
                "output": {
                    "count": {"$sum": 1},
                    "average_score": {"$avg": "$match_score"}
                }
            }
        }
    ]
    db = get_database()
    results = list(db["analyses"].aggregate(pipeline))

    # Format boundaries into readable labels
    label_map = {
        0: "0% - 39% (Low Match)",
        40: "40% - 59% (Moderate Match)",
        60: "60% - 79% (Good Match)",
        80: "80% - 100% (High Match)"
    }
    formatted = []
    for r in results:
        b_id = r.get("_id")
        formatted.append({
            "range": label_map.get(b_id, str(b_id)),
            "count": r.get("count", 0),
            "average_score": round(r.get("average_score", 0), 1)
        })

    return formatted, pipeline


def get_candidate_supply_vs_demand() -> List[Dict[str, Any]]:
    """
    Cross-collection comparison:
    Job Demand frequency vs Candidate Resume Supply count for each top skill.
    """
    demand_res, _ = get_most_demanded_job_skills(limit=12)
    demand_dict = {item["skill"]: item["demand_frequency"] for item in demand_res}

    # Aggregate candidate supply from 'resumes' collection
    db = get_database()
    resume_pipeline = [
        {"$unwind": "$skills"},
        {
            "$group": {
                "_id": "$skills",
                "supply_count": {"$sum": 1}
            }
        }
    ]
    supply_res = list(db["resumes"].aggregate(resume_pipeline))
    supply_dict = {item["_id"]: item["supply_count"] for item in supply_res}

    combined = []
    for skill, demand in demand_dict.items():
        supply = supply_dict.get(skill, 0)
        gap = demand - supply
        combined.append({
            "skill": skill,
            "demand": demand,
            "supply": supply,
            "gap": gap
        })
    return combined
