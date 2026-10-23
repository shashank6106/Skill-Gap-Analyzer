"""
Database Connection Manager using PyMongo.
Handles client lifecycle, connection pooling, and collection indexing.
"""

import os
import re
import urllib.parse
from typing import Optional, Tuple, Dict, Any
from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

DEFAULT_URI = "mongodb://localhost:27017/"
DEFAULT_DB_NAME = "skill_gap_analyzer"

_client: Optional[MongoClient] = None
_db: Optional[Database] = None


def sanitize_mongo_uri(uri: str) -> str:
    """
    Sanitizes MongoDB URI:
    1. Removes accidental '<' and '>' brackets from username/password.
    2. URL-encodes (RFC 3986) username and password so special characters
       like '@', '#', '$' don't break the connection.
    """
    if not uri or "://" not in uri:
        return uri

    # Match protocol://[credentials@]host/path
    pattern = r"^(mongodb(?:\+srv)?:\/\/)(.*):(.*)@([^@]+)$"
    match = re.match(pattern, uri.strip())
    if not match:
        return uri.strip()

    protocol, raw_user, raw_pwd, host_and_params = match.groups()

    # Strip accidental angle brackets: <user> -> user
    clean_user = raw_user.strip("<>").strip()
    clean_pwd = raw_pwd.strip("<>").strip()

    # Encode according to RFC 3986 as required by MongoDB
    safe_user = urllib.parse.quote_plus(urllib.parse.unquote_plus(clean_user))
    safe_pwd = urllib.parse.quote_plus(urllib.parse.unquote_plus(clean_pwd))

    return f"{protocol}{safe_user}:{safe_pwd}@{host_and_params}"


def _get_config_value(key: str, fallback: str) -> str:
    """
    Retrieves configuration value checking:
    1. Streamlit secrets (for Streamlit Community Cloud)
    2. OS Environment variables
    3. Provided default fallback
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            val = str(st.secrets[key]).strip()
            if val:
                return val
    except Exception:
        pass
    return os.getenv(key, fallback).strip()


def get_client(uri: Optional[str] = None) -> MongoClient:
    """
    Returns a cached PyMongo MongoClient instance.
    Uses 2.5s timeouts so Streamlit Community Cloud page never hangs on startup.
    """
    global _client
    if _client is None:
        raw_uri = uri or _get_config_value("MONGODB_URI", DEFAULT_URI)
        mongo_uri = sanitize_mongo_uri(raw_uri)
        _client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=2500,
            connectTimeoutMS=2500,
            socketTimeoutMS=2500,
            maxPoolSize=25
        )
    return _client


def get_database(db_name: Optional[str] = None, uri: Optional[str] = None) -> Database:
    """
    Returns the target MongoDB database object.
    """
    global _db
    if _db is None:
        client = get_client(uri)
        target_db = db_name or _get_config_value("DATABASE_NAME", DEFAULT_DB_NAME)
        _db = client[target_db]
    return _db


def check_connection() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Pings the MongoDB server to verify live connectivity.
    Returns (success, message, server_info).
    """
    try:
        client = get_client()
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
        server_info = client.server_info()
        version = server_info.get("version", "unknown")
        return True, f"Connected to MongoDB Server v{version}", server_info
    except (ConnectionFailure, ServerSelectionTimeoutError) as err:
        return False, f"MongoDB connection failed: {str(err)}", {}
    except Exception as err:
        return False, f"Unexpected database error: {str(err)}", {}


def setup_indexes() -> Dict[str, list]:
    """
    Sets up indexes across all collections to demonstrate NoSQL indexing principles.
    - Unique indexes ensure data integrity (user_id, job_id, skill name)
    - Multikey indexes optimize array queries (skills array)
    - Compound & Text indexes support complex search
    """
    db = get_database()
    index_results = {}

    try:
        # Users collection indexes
        users = db["users"]
        idx1 = users.create_index([("user_id", ASCENDING)], unique=True, name="uniq_user_id")
        idx2 = users.create_index([("email", ASCENDING)], unique=True, sparse=True, name="uniq_email")
        index_results["users"] = [idx1, idx2]

        # Resumes collection indexes (Multikey index on skills array)
        resumes = db["resumes"]
        idx3 = resumes.create_index([("resume_id", ASCENDING)], unique=True, name="uniq_resume_id")
        idx4 = resumes.create_index([("user_id", ASCENDING)], name="idx_resume_user")
        idx5 = resumes.create_index([("skills", ASCENDING)], name="multikey_resume_skills")
        index_results["resumes"] = [idx3, idx4, idx5]

        # Jobs collection indexes (Multikey on required_skills + Text search on title)
        jobs = db["jobs"]
        idx6 = jobs.create_index([("job_id", ASCENDING)], unique=True, name="uniq_job_id")
        idx7 = jobs.create_index([("required_skills", ASCENDING)], name="multikey_job_skills")
        idx8 = jobs.create_index([("title", TEXT), ("company", TEXT)], name="text_job_search")
        index_results["jobs"] = [idx6, idx7, idx8]

        # Analyses collection indexes
        analyses = db["analyses"]
        idx9 = analyses.create_index([("analysis_id", ASCENDING)], unique=True, name="uniq_analysis_id")
        idx10 = analyses.create_index([("user_id", ASCENDING)], name="idx_analysis_user")
        idx11 = analyses.create_index([("job_id", ASCENDING)], name="idx_analysis_job")
        idx12 = analyses.create_index([("match_score", ASCENDING)], name="idx_match_score")
        index_results["analyses"] = [idx9, idx10, idx11, idx12]

        # Skills master catalog
        skills = db["skills"]
        idx13 = skills.create_index([("name", ASCENDING)], unique=True, name="uniq_skill_name")
        idx14 = skills.create_index([("category", ASCENDING)], name="idx_skill_category")
        index_results["skills"] = [idx13, idx14]

        # Recommendations catalog
        recs = db["recommendations"]
        idx15 = recs.create_index([("skill", ASCENDING)], unique=True, name="uniq_rec_skill")
        index_results["recommendations"] = [idx15]

    except Exception as exc:
        print(f"Warning: Index setup warning: {exc}")

    return index_results


def close_connection() -> None:
    """Closes the client connection."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
