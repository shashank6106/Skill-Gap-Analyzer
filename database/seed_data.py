"""
Database Seed Script.
Populates the 'skill_gap_analyzer' database with realistic initial data
across all 6 collections: users, resumes, jobs, skills, analyses, recommendations.
"""

import os
import sys
from datetime import datetime, timezone, timedelta

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_connection import get_database, setup_indexes


def _utcnow():
    return datetime.now(timezone.utc)



USERS_DATA = [
    {
        "user_id": 101,
        "name": "Shashank",
        "email": "shashank@example.com",
        "phone": "+91 98765 43210",
        "education": {
            "degree": "B.Tech",
            "branch": "CSE",
            "college": "National Institute of Technology",
            "grad_year": 2025
        },
        "skills": ["Python", "C++", "SQL", "MongoDB", "Pandas"],
        "experience_years": 1,
        "created_at": _utcnow() - timedelta(days=20)
    },
    {
        "user_id": 102,
        "name": "Ananya Sharma",
        "email": "ananya.sharma@example.com",
        "phone": "+91 98765 43211",
        "education": {
            "degree": "B.Tech",
            "branch": "Data Science",
            "college": "Tech University",
            "grad_year": 2024
        },
        "skills": ["Python", "SQL", "Power BI", "Excel", "Statistics", "Tableau"],
        "experience_years": 2,
        "created_at": _utcnow() - timedelta(days=18)
    },
    {
        "user_id": 103,
        "name": "Rahul Verma",
        "email": "rahul.v@example.com",
        "phone": "+91 98765 43212",
        "education": {
            "degree": "B.E",
            "branch": "Information Technology",
            "college": "Apex Engineering Institute",
            "grad_year": 2025
        },
        "skills": ["JavaScript", "React", "Node.js", "Express", "MongoDB", "Git"],
        "experience_years": 1,
        "created_at": _utcnow() - timedelta(days=15)
    },
    {
        "user_id": 104,
        "name": "Priya Nair",
        "email": "priya.nair@example.com",
        "phone": "+91 98765 43213",
        "education": {
            "degree": "M.Tech",
            "branch": "Artificial Intelligence",
            "college": "Indian Institute of Science",
            "grad_year": 2024
        },
        "skills": ["Python", "PyTorch", "Scikit-learn", "NLP", "Pandas", "SQL", "Docker"],
        "experience_years": 3,
        "created_at": _utcnow() - timedelta(days=12)
    },
    {
        "user_id": 105,
        "name": "Vikram Malhotra",
        "email": "vikram.m@example.com",
        "phone": "+91 98765 43214",
        "education": {
            "degree": "B.Tech",
            "branch": "CSE",
            "college": "State Technological University",
            "grad_year": 2023
        },
        "skills": ["Python", "Django", "PostgreSQL", "Docker", "AWS", "Git", "Linux"],
        "experience_years": 3,
        "created_at": _utcnow() - timedelta(days=10)
    }
]


RESUMES_DATA = [
    {
        "resume_id": 1001,
        "user_id": 101,
        "filename": "shashank_resume.pdf",
        "parsed_name": "Shashank",
        "email": "shashank@example.com",
        "skills": ["Python", "C++", "SQL", "MongoDB", "Pandas"],
        "projects": [
            {
                "name": "Air Quality Analysis",
                "technologies": ["Python", "Pandas", "Matplotlib"],
                "description": "Cleaned 100k IoT sensor records and built time-series air quality alerts."
            },
            {
                "name": "Library Catalog Microservice",
                "technologies": ["Python", "MongoDB", "FastAPI"],
                "description": "RESTful book inventory management system with MongoDB schema design."
            }
        ],
        "uploaded_at": _utcnow() - timedelta(days=20)
    },
    {
        "resume_id": 1002,
        "user_id": 102,
        "filename": "ananya_analytics_resume.pdf",
        "parsed_name": "Ananya Sharma",
        "email": "ananya.sharma@example.com",
        "skills": ["Python", "SQL", "Power BI", "Excel", "Statistics", "Tableau"],
        "projects": [
            {
                "name": "Retail Sales Forecasting Dashboard",
                "technologies": ["Power BI", "SQL", "Excel", "Statistics"],
                "description": "Constructed interactive Power BI KPI dashboards and predictive models."
            }
        ],
        "uploaded_at": _utcnow() - timedelta(days=18)
    },
    {
        "resume_id": 1003,
        "user_id": 103,
        "filename": "rahul_fullstack_resume.pdf",
        "parsed_name": "Rahul Verma",
        "email": "rahul.v@example.com",
        "skills": ["JavaScript", "React", "Node.js", "Express", "MongoDB", "Git"],
        "projects": [
            {
                "name": "Campus Market MERN App",
                "technologies": ["React", "Node.js", "MongoDB", "Express"],
                "description": "Full-stack e-commerce marketplace featuring user auth and cart."
            }
        ],
        "uploaded_at": _utcnow() - timedelta(days=15)
    },
    {
        "resume_id": 1004,
        "user_id": 104,
        "filename": "priya_ml_resume.pdf",
        "parsed_name": "Priya Nair",
        "email": "priya.nair@example.com",
        "skills": ["Python", "PyTorch", "Scikit-learn", "NLP", "Pandas", "SQL", "Docker"],
        "projects": [
            {
                "name": "Biomedical Text Classifier",
                "technologies": ["Python", "PyTorch", "NLP", "Docker"],
                "description": "Fine-tuned transformer model for clinical notes multi-label tagging."
            }
        ],
        "uploaded_at": _utcnow() - timedelta(days=12)
    },
    {
        "resume_id": 1005,
        "user_id": 105,
        "filename": "vikram_backend_resume.pdf",
        "parsed_name": "Vikram Malhotra",
        "email": "vikram.m@example.com",
        "skills": ["Python", "Django", "PostgreSQL", "Docker", "AWS", "Git", "Linux"],
        "projects": [
            {
                "name": "Cloud Payment Gateway Service",
                "technologies": ["Python", "Django", "AWS", "Docker", "PostgreSQL"],
                "description": "High-throughput payment orchestration engine on AWS ECS."
            }
        ],
        "uploaded_at": _utcnow() - timedelta(days=10)
    }
]


JOBS_DATA = [
    {
        "job_id": 501,
        "title": "Data Analyst",
        "company": "ABC Technologies",
        "location": "Bengaluru (Hybrid)",
        "experience_years": 1,
        "description": "Looking for an analytical mindset capable of querying relational datasets, developing Power BI dashboards, and performing statistical exploratory analysis.",
        "required_skills": ["Python", "SQL", "Power BI", "Excel", "Statistics"]
    },
    {
        "job_id": 502,
        "title": "Machine Learning Engineer",
        "company": "Nexus AI Labs",
        "location": "Hyderabad (On-site)",
        "experience_years": 2,
        "description": "Develop and deploy state-of-the-art NLP and ML pipelines. Hands-on experience with PyTorch, Scikit-learn, Docker, and SQL is required.",
        "required_skills": ["Python", "Scikit-learn", "PyTorch", "NLP", "Docker", "SQL"]
    },
    {
        "job_id": 503,
        "title": "Full Stack Developer (MERN)",
        "company": "CloudPeak Software",
        "location": "Pune (Remote)",
        "experience_years": 2,
        "description": "Build responsive React web applications backed by Node.js, Express, and MongoDB NoSQL database pipelines.",
        "required_skills": ["JavaScript", "React", "Node.js", "MongoDB", "Git", "Docker"]
    },
    {
        "job_id": 504,
        "title": "Cloud Data Engineer",
        "company": "DataNova Systems",
        "location": "Bengaluru (On-site)",
        "experience_years": 2,
        "description": "Architect scalable data pipelines processing structured and semi-structured documents. Heavy use of Python, MongoDB, SQL, and AWS cloud services.",
        "required_skills": ["Python", "SQL", "MongoDB", "AWS", "Apache Spark", "Docker"]
    },
    {
        "job_id": 505,
        "title": "Backend Python Developer",
        "company": "FinTech Solutions",
        "location": "Mumbai (Hybrid)",
        "experience_years": 3,
        "description": "Engineer robust microservices handling secure financial transactions. Deep knowledge of Python frameworks, PostgreSQL, MongoDB, Docker, and Git.",
        "required_skills": ["Python", "Django", "PostgreSQL", "MongoDB", "Docker", "Git"]
    }
]


SKILLS_DATA = [
    # Programming Languages
    {"name": "Python", "category": "Programming Languages", "demand_level": "Very High"},
    {"name": "C++", "category": "Programming Languages", "demand_level": "Medium"},
    {"name": "JavaScript", "category": "Programming Languages", "demand_level": "High"},
    {"name": "TypeScript", "category": "Programming Languages", "demand_level": "High"},
    {"name": "Java", "category": "Programming Languages", "demand_level": "High"},
    
    # Databases & NoSQL
    {"name": "MongoDB", "category": "Databases (NoSQL)", "demand_level": "Very High"},
    {"name": "SQL", "category": "Databases (SQL)", "demand_level": "Very High"},
    {"name": "PostgreSQL", "category": "Databases (SQL)", "demand_level": "High"},
    {"name": "Redis", "category": "Databases (NoSQL)", "demand_level": "Medium"},
    
    # Data & Analytics
    {"name": "Pandas", "category": "Data Science", "demand_level": "High"},
    {"name": "Power BI", "category": "Business Intelligence", "demand_level": "High"},
    {"name": "Excel", "category": "Business Intelligence", "demand_level": "High"},
    {"name": "Statistics", "category": "Data Science", "demand_level": "High"},
    {"name": "Tableau", "category": "Business Intelligence", "demand_level": "Medium"},
    {"name": "Apache Spark", "category": "Big Data", "demand_level": "High"},
    
    # Machine Learning & AI
    {"name": "Scikit-learn", "category": "Machine Learning", "demand_level": "High"},
    {"name": "PyTorch", "category": "Deep Learning", "demand_level": "High"},
    {"name": "TensorFlow", "category": "Deep Learning", "demand_level": "Medium"},
    {"name": "NLP", "category": "Artificial Intelligence", "demand_level": "High"},
    
    # Web & Backend
    {"name": "React", "category": "Web Development", "demand_level": "High"},
    {"name": "Node.js", "category": "Backend Development", "demand_level": "High"},
    {"name": "Express", "category": "Backend Development", "demand_level": "Medium"},
    {"name": "Django", "category": "Backend Development", "demand_level": "High"},
    {"name": "FastAPI", "category": "Backend Development", "demand_level": "High"},
    
    # DevOps & Cloud
    {"name": "Docker", "category": "DevOps & Cloud", "demand_level": "Very High"},
    {"name": "AWS", "category": "DevOps & Cloud", "demand_level": "Very High"},
    {"name": "Git", "category": "DevOps & Cloud", "demand_level": "High"},
    {"name": "Kubernetes", "category": "DevOps & Cloud", "demand_level": "High"},
    {"name": "Linux", "category": "DevOps & Cloud", "demand_level": "Medium"}
]


RECOMMENDATIONS_DATA = [
    {
        "skill": "Power BI",
        "priority": "High",
        "course_title": "Microsoft Power BI Data Analyst Professional Certificate",
        "platform": "Coursera / Microsoft",
        "estimated_hours": 35,
        "roadmap": "1. Data modeling & DAX basics -> 2. Visualizations & Drill-downs -> 3. Power BI Service & Publishing",
        "resource_url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"
    },
    {
        "skill": "AWS",
        "priority": "High",
        "course_title": "AWS Certified Solutions Architect Associate Prep",
        "platform": "AWS Skill Builder / Udemy",
        "estimated_hours": 40,
        "roadmap": "1. IAM & S3 Core -> 2. EC2 & VPC Networking -> 3. DynamoDB & RDS -> 4. Serverless Lambda",
        "resource_url": "https://aws.amazon.com/training/"
    },
    {
        "skill": "Docker",
        "priority": "High",
        "course_title": "Docker Mastery with Swarm and Compose",
        "platform": "Udemy / Docker Docs",
        "estimated_hours": 20,
        "roadmap": "1. Dockerfiles & Container lifecycle -> 2. Docker Compose multi-service -> 3. Volume persistence & Networking",
        "resource_url": "https://docs.docker.com/get-started/"
    },
    {
        "skill": "Excel",
        "priority": "Medium",
        "course_title": "Advanced Excel for Business Analytics",
        "platform": "LinkedIn Learning",
        "estimated_hours": 15,
        "roadmap": "1. XLOOKUP & INDEX/MATCH -> 2. Pivot Tables & Slicers -> 3. What-if analysis and Power Query",
        "resource_url": "https://support.microsoft.com/en-us/excel"
    },
    {
        "skill": "Statistics",
        "priority": "High",
        "course_title": "Statistical Thinking for Data Science and Analytics",
        "platform": "edX / Columbia University",
        "estimated_hours": 30,
        "roadmap": "1. Probability distributions -> 2. Hypothesis testing (p-value, t-test, ANOVA) -> 3. Linear Regression modeling",
        "resource_url": "https://www.khanacademy.org/math/statistics-probability"
    },
    {
        "skill": "Apache Spark",
        "priority": "High",
        "course_title": "Taming Big Data with Apache Spark and Python (PySpark)",
        "platform": "Databricks Academy",
        "estimated_hours": 35,
        "roadmap": "1. Spark DataFrames & RDD internals -> 2. Structured Streaming -> 3. Spark SQL performance tuning",
        "resource_url": "https://spark.apache.org/docs/latest/"
    },
    {
        "skill": "MongoDB",
        "priority": "High",
        "course_title": "MongoDB Node.js & Python Developer Path",
        "platform": "MongoDB University (Free)",
        "estimated_hours": 20,
        "roadmap": "1. Document modeling & Schema design -> 2. PyMongo CRUD & Indexes -> 3. Complex Aggregation Pipelines",
        "resource_url": "https://learn.mongodb.com/"
    },
    {
        "skill": "PyTorch",
        "priority": "High",
        "course_title": "Deep Learning with PyTorch",
        "platform": "DeepLearning.AI",
        "estimated_hours": 35,
        "roadmap": "1. Tensors & Autograd -> 2. Neural Net architectures -> 3. Computer Vision & NLP Transfer Learning",
        "resource_url": "https://pytorch.org/tutorials/"
    },
    {
        "skill": "NLP",
        "priority": "High",
        "course_title": "Natural Language Processing Specialization",
        "platform": "Coursera / DeepLearning.AI",
        "estimated_hours": 45,
        "roadmap": "1. Tokenization & Regular expressions -> 2. TF-IDF & Word2Vec embeddings -> 3. Transformer attention models",
        "resource_url": "https://huggingface.co/learn/nlp-course/"
    },
    {
        "skill": "Scikit-learn",
        "priority": "Medium",
        "course_title": "Machine Learning in Python with Scikit-learn",
        "platform": "INRIA / MOOC",
        "estimated_hours": 25,
        "roadmap": "1. Preprocessing & pipelines -> 2. Supervised classification/regression -> 3. Cross-validation & Hyperparameter tuning",
        "resource_url": "https://scikit-learn.org/stable/tutorial/index.html"
    },
    {
        "skill": "React",
        "priority": "Medium",
        "course_title": "The Complete React 18 Course",
        "platform": "Udemy / React.dev",
        "estimated_hours": 30,
        "roadmap": "1. JSX & Components -> 2. Hooks (useState, useEffect, useMemo) -> 3. Global state management & routing",
        "resource_url": "https://react.dev/learn"
    },
    {
        "skill": "PostgreSQL",
        "priority": "Medium",
        "course_title": "PostgreSQL Bootcamp: Go from Beginner to Advanced",
        "platform": "Udemy",
        "estimated_hours": 20,
        "roadmap": "1. Advanced JOINs & Aggregates -> 2. Window functions -> 3. Query planning & EXPLAIN ANALYZE indexing",
        "resource_url": "https://www.postgresql.org/docs/"
    }
]


ANALYSES_DATA = [
    {
        "analysis_id": 9001,
        "user_id": 101,
        "user_name": "Shashank",
        "job_id": 501,
        "job_title": "Data Analyst",
        "company": "ABC Technologies",
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["Power BI", "Excel", "Statistics"],
        "match_score": 40.0,
        "direct_skill_score": 40.0,
        "semantic_score": 52.0,
        "candidate_skills": ["Python", "C++", "SQL", "MongoDB", "Pandas"],
        "job_required_skills": ["Python", "SQL", "Power BI", "Excel", "Statistics"],
        "status": "Evaluated",
        "created_at": _utcnow() - timedelta(days=19)
    },
    {
        "analysis_id": 9002,
        "user_id": 101,
        "user_name": "Shashank",
        "job_id": 504,
        "job_title": "Cloud Data Engineer",
        "company": "DataNova Systems",
        "matched_skills": ["Python", "SQL", "MongoDB"],
        "missing_skills": ["AWS", "Apache Spark", "Docker"],
        "match_score": 50.0,
        "direct_skill_score": 50.0,
        "semantic_score": 58.0,
        "candidate_skills": ["Python", "C++", "SQL", "MongoDB", "Pandas"],
        "job_required_skills": ["Python", "SQL", "MongoDB", "AWS", "Apache Spark", "Docker"],
        "status": "Evaluated",
        "created_at": _utcnow() - timedelta(days=17)
    },
    {
        "analysis_id": 9003,
        "user_id": 102,
        "user_name": "Ananya Sharma",
        "job_id": 501,
        "job_title": "Data Analyst",
        "company": "ABC Technologies",
        "matched_skills": ["Python", "SQL", "Power BI", "Excel", "Statistics"],
        "missing_skills": [],
        "match_score": 100.0,
        "direct_skill_score": 100.0,
        "semantic_score": 94.0,
        "candidate_skills": ["Python", "SQL", "Power BI", "Excel", "Statistics", "Tableau"],
        "job_required_skills": ["Python", "SQL", "Power BI", "Excel", "Statistics"],
        "status": "Evaluated",
        "created_at": _utcnow() - timedelta(days=16)
    },
    {
        "analysis_id": 9004,
        "user_id": 103,
        "user_name": "Rahul Verma",
        "job_id": 503,
        "job_title": "Full Stack Developer (MERN)",
        "company": "CloudPeak Software",
        "matched_skills": ["JavaScript", "React", "Node.js", "MongoDB", "Git"],
        "missing_skills": ["Docker"],
        "match_score": 83.3,
        "direct_skill_score": 83.3,
        "semantic_score": 88.0,
        "candidate_skills": ["JavaScript", "React", "Node.js", "Express", "MongoDB", "Git"],
        "job_required_skills": ["JavaScript", "React", "Node.js", "MongoDB", "Git", "Docker"],
        "status": "Evaluated",
        "created_at": _utcnow() - timedelta(days=14)
    },
    {
        "analysis_id": 9005,
        "user_id": 104,
        "user_name": "Priya Nair",
        "job_id": 502,
        "job_title": "Machine Learning Engineer",
        "company": "Nexus AI Labs",
        "matched_skills": ["Python", "Scikit-learn", "PyTorch", "NLP", "Docker", "SQL"],
        "missing_skills": [],
        "match_score": 100.0,
        "direct_skill_score": 100.0,
        "semantic_score": 96.0,
        "candidate_skills": ["Python", "PyTorch", "Scikit-learn", "NLP", "Pandas", "SQL", "Docker"],
        "job_required_skills": ["Python", "Scikit-learn", "PyTorch", "NLP", "Docker", "SQL"],
        "status": "Evaluated",
        "created_at": _utcnow() - timedelta(days=11)
    },
    {
        "analysis_id": 9006,
        "user_id": 105,
        "user_name": "Vikram Malhotra",
        "job_id": 505,
        "job_title": "Backend Python Developer",
        "company": "FinTech Solutions",
        "matched_skills": ["Python", "Django", "PostgreSQL", "Docker", "Git"],
        "missing_skills": ["MongoDB"],
        "match_score": 83.3,
        "direct_skill_score": 83.3,
        "semantic_score": 85.0,
        "candidate_skills": ["Python", "Django", "PostgreSQL", "Docker", "AWS", "Git", "Linux"],
        "job_required_skills": ["Python", "Django", "PostgreSQL", "MongoDB", "Docker", "Git"],
        "status": "Evaluated",
        "created_at": _utcnow() - timedelta(days=9)
    }
]


def seed_database(drop_existing: bool = True) -> dict:
    """
    Seeds all collections with initial data.
    If drop_existing is True, clears existing collections first to guarantee fresh clean state.
    """
    db = get_database()

    counts = {}
    collections = ["users", "resumes", "jobs", "skills", "recommendations", "analyses"]

    if drop_existing:
        for coll in collections:
            db[coll].drop()

    # Create indexes across all collections
    setup_indexes()

    # 1. Users
    db["users"].insert_many(USERS_DATA)
    counts["users"] = db["users"].count_documents({})

    # 2. Resumes
    db["resumes"].insert_many(RESUMES_DATA)
    counts["resumes"] = db["resumes"].count_documents({})

    # 3. Jobs
    db["jobs"].insert_many(JOBS_DATA)
    counts["jobs"] = db["jobs"].count_documents({})

    # 4. Skills
    db["skills"].insert_many(SKILLS_DATA)
    counts["skills"] = db["skills"].count_documents({})

    # 5. Recommendations
    db["recommendations"].insert_many(RECOMMENDATIONS_DATA)
    counts["recommendations"] = db["recommendations"].count_documents({})

    # 6. Analyses
    db["analyses"].insert_many(ANALYSES_DATA)
    counts["analyses"] = db["analyses"].count_documents({})

    return counts


if __name__ == "__main__":
    print("Connecting to MongoDB and seeding 'skill_gap_analyzer' database...")
    result = seed_database(drop_existing=True)
    print("Database seeding completed successfully!")
    for coll, count in result.items():
        print(f"  - Collection '{coll}': {count} documents")
