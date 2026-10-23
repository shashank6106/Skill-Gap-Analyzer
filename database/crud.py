"""
PyMongo CRUD Operations Layer.
Demonstrates explicit MongoDB CRUD commands, query operators ($gt, $gte, $in, $and, $or, $exists),
and array modifiers ($push, $pull, $addToSet).
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult
from database.db_connection import get_database


def _now():
    """Returns current UTC timestamp without timezone offset issues in MongoDB."""
    return datetime.now(timezone.utc)



# =====================================================================
# 1. USER COLLECTION CRUD OPERATIONS
# =====================================================================

def insert_user(user_data: Dict[str, Any]) -> InsertOneResult:
    """
    Demonstrates: insert_one()
    Inserts a single user document into the 'users' collection.
    """
    db = get_database()
    users: Collection = db["users"]
    if "created_at" not in user_data:
        user_data["created_at"] = _now()
    return users.insert_one(user_data)


def insert_users_bulk(user_list: List[Dict[str, Any]]) -> InsertManyResult:
    """
    Demonstrates: insert_many()
    Inserts multiple user documents in a single network round-trip.
    """
    db = get_database()
    users: Collection = db["users"]
    for u in user_list:
        if "created_at" not in u:
            u["created_at"] = _now()
    return users.insert_many(user_list, ordered=False)


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Demonstrates: find_one() with exact equality filter.
    """
    try:
        db = get_database()
        res = db["users"].find_one({"user_id": user_id})
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import USERS_DATA
    return next((u for u in USERS_DATA if u.get("user_id") == user_id), None)


def get_all_users() -> List[Dict[str, Any]]:
    """
    Demonstrates: find() with sort on integer key.
    """
    try:
        db = get_database()
        res = list(db["users"].find().sort("user_id", 1))
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import USERS_DATA
    return USERS_DATA


def update_user_skills(user_id: int, new_skill: str) -> UpdateResult:
    """
    Demonstrates: update_one() with array operator $addToSet.
    $addToSet adds the value to the array only if it does not already exist,
    preventing duplicate skills in the candidate profile.
    """
    db = get_database()
    return db["users"].update_one(
        {"user_id": user_id},
        {
            "$addToSet": {"skills": new_skill},
            "$set": {"updated_at": _now()}
        }
    )


def push_skill_to_user(user_id: int, new_skill: str) -> UpdateResult:
    """
    Demonstrates: update_one() with array operator $push.
    Appends skill directly to array.
    """
    db = get_database()
    return db["users"].update_one(
        {"user_id": user_id},
        {"$push": {"skills": new_skill}}
    )


def pull_skill_from_user(user_id: int, skill_to_remove: str) -> UpdateResult:
    """
    Demonstrates: update_one() with array operator $pull.
    Removes matching skill from the array.
    """
    db = get_database()
    return db["users"].update_one(
        {"user_id": user_id},
        {"$pull": {"skills": skill_to_remove}}
    )


def delete_user(user_id: int) -> DeleteResult:
    """
    Demonstrates: delete_one()
    Deletes a user by user_id.
    """
    db = get_database()
    return db["users"].delete_one({"user_id": user_id})


def save_optimized_bullets(user_id: int, optimized_bullets: List[Dict[str, Any]]) -> UpdateResult:
    """
    Demonstrates: update_one() with $set operator.
    Saves ATS-optimized resume bullet points to the candidate document in MongoDB.
    """
    db = get_database()
    return db["users"].update_one(
        {"user_id": user_id},
        {
            "$set": {
                "optimized_bullets": optimized_bullets,
                "bullets_updated_at": _now()
            }
        }
    )


# =====================================================================
# 2. RESUMES COLLECTION CRUD OPERATIONS
# =====================================================================

def insert_resume(resume_data: Dict[str, Any]) -> InsertOneResult:
    """
    Demonstrates: insert_one()
    Stores extracted resume metadata, projects, and detected skills.
    """
    db = get_database()
    if "uploaded_at" not in resume_data:
        resume_data["uploaded_at"] = _now()
    return db["resumes"].insert_one(resume_data)


def get_resume_by_id(resume_id: int) -> Optional[Dict[str, Any]]:
    """Demonstrates: find_one() by resume_id."""
    db = get_database()
    return db["resumes"].find_one({"resume_id": resume_id})


def get_resume_by_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Demonstrates: find_one() with sort descending to fetch latest uploaded resume."""
    db = get_database()
    return db["resumes"].find_one({"user_id": user_id}, sort=[("resume_id", -1)])


def get_all_resumes() -> List[Dict[str, Any]]:
    """Demonstrates: find() fetching all resumes."""
    db = get_database()
    return list(db["resumes"].find().sort("resume_id", -1))


def add_skill_to_resume(resume_id: int, skill_name: str) -> UpdateResult:
    """
    Demonstrates: update_one() with $addToSet on resumes collection.
    """
    db = get_database()
    return db["resumes"].update_one(
        {"resume_id": resume_id},
        {"$addToSet": {"skills": skill_name}}
    )


def delete_resume(resume_id: int) -> DeleteResult:
    """Demonstrates: delete_one() on resumes collection."""
    db = get_database()
    return db["resumes"].delete_one({"resume_id": resume_id})


# =====================================================================
# 3. JOBS COLLECTION CRUD & OPERATORS DEMONSTRATION
# =====================================================================

def insert_job(job_data: Dict[str, Any]) -> InsertOneResult:
    """Demonstrates: insert_one() on jobs collection."""
    db = get_database()
    if "created_at" not in job_data:
        job_data["created_at"] = _now()
    return db["jobs"].insert_one(job_data)


def insert_jobs_bulk(jobs_list: List[Dict[str, Any]]) -> InsertManyResult:
    """Demonstrates: insert_many() on jobs collection."""
    db = get_database()
    return db["jobs"].insert_many(jobs_list, ordered=False)


def get_job_by_id(job_id: int) -> Optional[Dict[str, Any]]:
    """Demonstrates: find_one() on jobs collection."""
    try:
        db = get_database()
        res = db["jobs"].find_one({"job_id": job_id})
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import JOBS_DATA
    return next((j for j in JOBS_DATA if j.get("job_id") == job_id), None)


def get_all_jobs() -> List[Dict[str, Any]]:
    """Demonstrates: find() on jobs collection."""
    try:
        db = get_database()
        res = list(db["jobs"].find().sort("job_id", 1))
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import JOBS_DATA
    return JOBS_DATA


def find_jobs_by_skills(skills: List[str], match_all: bool = False) -> List[Dict[str, Any]]:
    """
    Demonstrates:
    - Array operator $in: Matches jobs requiring ANY of the specified skills.
    - Array operator $all: Matches jobs requiring ALL of the specified skills.
    """
    try:
        db = get_database()
        operator = "$all" if match_all else "$in"
        query = {"required_skills": {operator: skills}}
        res = list(db["jobs"].find(query))
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import JOBS_DATA
    if match_all:
        return [j for j in JOBS_DATA if all(s in j.get("required_skills", []) for s in skills)]
    else:
        return [j for j in JOBS_DATA if any(s in j.get("required_skills", []) for s in skills)]


def find_jobs_with_experience(min_years: int, max_years: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Demonstrates Query Comparison Operators:
    - $gte (greater than or equal)
    - $lte (less than or equal)
    - $and compound logic
    """
    try:
        db = get_database()
        conditions = [{"experience_years": {"$gte": min_years}}]
        if max_years is not None:
            conditions.append({"experience_years": {"$lte": max_years}})

        query = {"$and": conditions} if len(conditions) > 1 else conditions[0]
        res = list(db["jobs"].find(query))
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import JOBS_DATA
    return [j for j in JOBS_DATA if j.get("experience_years", 0) >= min_years and (max_years is None or j.get("experience_years", 0) <= max_years)]


def search_jobs_by_keyword(keyword: str) -> List[Dict[str, Any]]:
    """
    Demonstrates:
    - $or operator with $regex pattern matching for flexible full-text query.
    """
    try:
        db = get_database()
        query = {
            "$or": [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"company": {"$regex": keyword, "$options": "i"}},
                {"required_skills": {"$in": [keyword]}}
            ]
        }
        res = list(db["jobs"].find(query))
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import JOBS_DATA
    kw = keyword.lower()
    return [j for j in JOBS_DATA if kw in j.get("title", "").lower() or kw in j.get("company", "").lower() or any(kw in s.lower() for s in j.get("required_skills", []))]


def delete_job(job_id: int) -> DeleteResult:
    """Demonstrates: delete_one() on jobs."""
    db = get_database()
    return db["jobs"].delete_one({"job_id": job_id})


# =====================================================================
# 4. ANALYSES COLLECTION CRUD & FILTER OPERATORS
# =====================================================================

def insert_analysis(analysis_data: Dict[str, Any]) -> InsertOneResult:
    """
    Demonstrates: insert_one()
    Saves the computed skill gap, matched skills, missing skills, and score.
    """
    db = get_database()
    if "created_at" not in analysis_data:
        analysis_data["created_at"] = _now()
    return db["analyses"].insert_one(analysis_data)


def get_analysis_by_id(analysis_id: int) -> Optional[Dict[str, Any]]:
    """Demonstrates: find_one() on analyses collection."""
    db = get_database()
    return db["analyses"].find_one({"analysis_id": analysis_id})


def get_analyses_by_user(user_id: int) -> List[Dict[str, Any]]:
    """Demonstrates: find() filtered by user_id with descending timestamp."""
    db = get_database()
    return list(db["analyses"].find({"user_id": user_id}).sort("created_at", -1))


def get_recent_analyses(limit: int = 10) -> List[Dict[str, Any]]:
    """Demonstrates: find() with sort() and limit()."""
    db = get_database()
    return list(db["analyses"].find().sort("created_at", -1).limit(limit))


def find_high_scoring_candidates(min_score: float = 70.0) -> List[Dict[str, Any]]:
    """
    Demonstrates:
    - Comparison operator $gte on match_score.
    """
    db = get_database()
    return list(db["analyses"].find({"match_score": {"$gte": min_score}}).sort("match_score", -1))


def filter_analyses_advanced(
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    has_missing_skills: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """
    Demonstrates:
    - $gte, $lte, $exists, and $ne operators in a dynamic query filter.
    """
    db = get_database()
    query: Dict[str, Any] = {}

    score_conditions = {}
    if min_score is not None:
        score_conditions["$gte"] = min_score
    if max_score is not None:
        score_conditions["$lte"] = max_score
    if score_conditions:
        query["match_score"] = score_conditions

    if has_missing_skills is True:
        # Array exists and is not empty ($ne: [])
        query["missing_skills"] = {"$exists": True, "$ne": []}
    elif has_missing_skills is False:
        query["missing_skills"] = []

    return list(db["analyses"].find(query).sort("match_score", -1))


def delete_analysis(analysis_id: int) -> DeleteResult:
    """Demonstrates: delete_one() on analyses."""
    db = get_database()
    return db["analyses"].delete_one({"analysis_id": analysis_id})


def delete_analyses_many(filter_criteria: Dict[str, Any]) -> DeleteResult:
    """
    Demonstrates: delete_many()
    Deletes all analyses matching the given query filter.
    """
    db = get_database()
    return db["analyses"].delete_many(filter_criteria)


# =====================================================================
# 5. SKILLS & RECOMMENDATIONS COLLECTIONS
# =====================================================================

def get_all_skills() -> List[Dict[str, Any]]:
    """Returns all canonical skills stored in MongoDB."""
    try:
        db = get_database()
        res = list(db["skills"].find().sort("name", 1))
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import SKILLS_DATA
    return SKILLS_DATA


def get_recommendations_for_skills(missing_skills: List[str]) -> List[Dict[str, Any]]:
    """
    Demonstrates: $in operator
    Finds targeted learning recommendations for the list of missing skills.
    """
    try:
        db = get_database()
        res = list(db["recommendations"].find({"skill": {"$in": missing_skills}}))
        if res:
            return res
    except Exception:
        pass
    from database.seed_data import RECOMMENDATIONS_DATA
    return [r for r in RECOMMENDATIONS_DATA if r.get("skill") in missing_skills]


def update_recommendation_priority(skill: str, new_priority: str) -> UpdateResult:
    """
    Demonstrates: update_one() with $set operator.
    """
    db = get_database()
    return db["recommendations"].update_one(
        {"skill": skill},
        {"$set": {"priority": new_priority, "updated_at": _now()}}
    )


# =====================================================================
# 6. ID GENERATOR HELPER
# =====================================================================

def get_next_id(collection_name: str, id_field: str, base_start: int = 100) -> int:
    """
    Computes next auto-incrementing ID for demo simplicity using find_one + sort.
    """
    try:
        db = get_database()
        latest = db[collection_name].find_one(sort=[(id_field, -1)])
        if latest and id_field in latest and isinstance(latest[id_field], int):
            return latest[id_field] + 1
    except Exception:
        pass
    import random
    return base_start + random.randint(1, 99)
