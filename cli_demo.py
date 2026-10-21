"""
Skill Gap Analyzer - Terminal / Viva Live Demo Script.
Demonstrates live PyMongo CRUD operations, query operators, and aggregation pipelines
directly from the terminal. Perfect for answering professor questions and lab evaluations!
"""

import os
import sys
import json
from pprint import pprint

# Ensure current directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.db_connection import check_connection, get_database
from database.crud import (
    insert_user, get_user_by_id, update_user_skills, pull_skill_from_user, delete_user,
    find_jobs_by_skills, find_jobs_with_experience
)
from database.aggregations import (
    get_system_kpis, get_most_matched_skills, get_most_common_missing_skills,
    get_most_demanded_job_skills, get_job_performance_breakdown
)


def print_header(title: str):
    print("\n" + "=" * 70)
    print(f" {title.upper()} ")
    print("=" * 70)


def print_step(step_num: int, title: str, explanation: str):
    print(f"\n[Step {step_num}] {title}")
    print(f"--> Concept: {explanation}")


def run_demo():
    print_header("Skill Gap Analyzer - PyMongo & MongoDB Viva Demonstration")

    # 1. Connection check
    print_step(1, "MongoDB Connection Check", "Client ping and server information")
    ok, msg, info = check_connection()
    print(f"Status: {msg}")
    print(f"MongoDB Version: {info.get('version', 'N/A')}")
    print(f"Host: {info.get('host', 'localhost')}")

    # 2. Database & Collections
    print_step(2, "Database & Collections Inspection", "Listing all collections in 'skill_gap_analyzer'")
    db = get_database()
    collections = db.list_collection_names()
    print(f"Active Collections: {collections}")
    for coll in sorted(collections):
        print(f"  - {coll:<16}: {db[coll].count_documents({})} documents")

    # 3. CRUD Demonstration: INSERT
    print_step(3, "PyMongo CRUD: insert_one()", "Inserting a candidate document into 'users'")
    demo_user_id = 999
    # Clean up previous run if any
    delete_user(demo_user_id)

    new_candidate = {
        "user_id": demo_user_id,
        "name": "Demo Candidate (Viva)",
        "email": "demo.viva@example.com",
        "education": {"degree": "B.Tech", "branch": "CSE"},
        "skills": ["Python", "SQL"]
    }
    insert_res = insert_user(new_candidate)
    print(f"Executed: db.users.insert_one({{...}})")
    print(f"Inserted Document ID: {insert_res.inserted_id}")

    # 4. CRUD Demonstration: READ
    print_step(4, "PyMongo CRUD: find_one()", "Querying the candidate document by user_id")
    found_user = get_user_by_id(demo_user_id)
    print("Fetched User Document:")
    print(f"  Name  : {found_user['name']}")
    print(f"  Skills: {found_user['skills']}")

    # 5. CRUD Demonstration: UPDATE with $addToSet
    print_step(5, "PyMongo Array Operator: $addToSet", "Adding 'MongoDB' to skills array without creating duplicates")
    print("Action 1: Adding 'MongoDB'...")
    update_user_skills(demo_user_id, "MongoDB")
    user_updated = get_user_by_id(demo_user_id)
    print(f"  Skills after 1st addition: {user_updated['skills']}")

    print("Action 2: Attempting to add duplicate 'MongoDB'...")
    update_user_skills(demo_user_id, "MongoDB")
    user_dedup = get_user_by_id(demo_user_id)
    print(f"  Skills after duplicate addition: {user_dedup['skills']} (No duplicate created!)")

    # 6. CRUD Demonstration: UPDATE with $pull
    print_step(6, "PyMongo Array Operator: $pull", "Removing 'SQL' from skills array")
    pull_skill_from_user(demo_user_id, "SQL")
    user_pulled = get_user_by_id(demo_user_id)
    print(f"  Skills after $pull 'SQL': {user_pulled['skills']}")

    # 7. Query Operators: $in and $all
    print_step(7, "PyMongo Query Operator: $in vs $all", "Finding jobs matching required skills")
    search_skills = ["Python", "MongoDB"]
    matched_in = find_jobs_by_skills(search_skills, match_all=False)
    matched_all = find_jobs_by_skills(search_skills, match_all=True)
    print(f"Jobs requiring ANY of {search_skills} ($in): {len(matched_in)} jobs found")
    for j in matched_in:
        print(f"  - {j['title']} @ {j['company']} (Requires: {j['required_skills']})")
    print(f"\nJobs requiring ALL of {search_skills} ($all): {len(matched_all)} jobs found")
    for j in matched_all:
        print(f"  - {j['title']} @ {j['company']}")

    # 8. Query Comparison Operators: $gte and $lte
    print_step(8, "PyMongo Comparison Operators: $gte and $lte", "Finding jobs by experience range")
    exp_jobs = find_jobs_with_experience(min_years=2, max_years=3)
    print(f"Jobs with experience 2 to 3 years: {len(exp_jobs)} found")
    for j in exp_jobs:
        print(f"  - {j['title']} (Experience: {j['experience_years']} yrs)")

    # 9. Aggregation Pipeline 1: Most Demanded Skills
    print_step(9, "MongoDB Aggregation: $unwind + $group + $sort", "Most Demanded Job Skills")
    skills_res, pipeline1 = get_most_demanded_job_skills(limit=5)
    print("Executed Pipeline:")
    print(json.dumps(pipeline1, indent=2))
    print("\nAggregation Results:")
    for item in skills_res:
        print(f"  - {item['skill']:<15}: Demanded in {item['demand_frequency']} jobs")

    # 10. Aggregation Pipeline 2: Most Common Missing Skills
    print_step(10, "MongoDB Aggregation: Common Skill Gaps", "Which skills do candidates lack most?")
    missing_res, pipeline2 = get_most_common_missing_skills(limit=5)
    print("Aggregation Results:")
    for item in missing_res:
        print(f"  - {item['skill']:<15}: Missing in {item['gap_count']} candidate evaluations")

    # 11. Aggregation Pipeline 3: $lookup Foreign Join
    print_step(11, "MongoDB Aggregation: $lookup (NoSQL Join)", "Joining 'analyses' with 'jobs' collection")
    job_perf, pipeline3 = get_job_performance_breakdown()
    print("Aggregation Results (Job Leaderboard):")
    for item in job_perf:
        print(f"  - {item['job_title']:<25} @ {item['company']:<20}: Avg Match = {item['avg_match_score']}% (Evaluations: {item['total_evaluations']})")

    # 12. CRUD Demonstration: DELETE
    print_step(12, "PyMongo CRUD: delete_one()", "Cleaning up demo candidate")
    del_res = delete_user(demo_user_id)
    print(f"Deleted user_id {demo_user_id}, deleted_count: {del_res.deleted_count}")

    print_header("Demonstration Complete! All MongoDB & PyMongo operations verified.")


if __name__ == "__main__":
    run_demo()
