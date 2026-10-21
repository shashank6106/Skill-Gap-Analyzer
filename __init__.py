"""
Skill Gap Analyzer - Database Package
MongoDB & PyMongo integration layer.
"""
from database.db_connection import get_database, check_connection, close_connection
from database.crud import (
    # Users
    insert_user, get_user_by_id, get_all_users, update_user_skills, delete_user,
    # Resumes
    insert_resume, get_resume_by_user, get_all_resumes, add_skill_to_resume,
    # Jobs
    insert_job, get_job_by_id, get_all_jobs, find_jobs_by_skills,
    # Analyses
    insert_analysis, get_analysis_by_id, get_analyses_by_user, get_recent_analyses,
    # Skills & Recommendations
    get_all_skills, get_recommendations_for_skills
)

__all__ = [
    "get_database", "check_connection", "close_connection",
    "insert_user", "get_user_by_id", "get_all_users", "update_user_skills", "delete_user",
    "insert_resume", "get_resume_by_user", "get_all_resumes", "add_skill_to_resume",
    "insert_job", "get_job_by_id", "get_all_jobs", "find_jobs_by_skills",
    "insert_analysis", "get_analysis_by_id", "get_analyses_by_user", "get_recent_analyses",
    "get_all_skills", "get_recommendations_for_skills"
]
