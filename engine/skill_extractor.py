"""
Skill Extractor Module.
Identifies canonical technical skills and tools from unstructured text
using taxonomy matching and regular expression tokenization.
"""

import re
from typing import List, Set, Dict, Any, Optional
from database.db_connection import get_database


# Fallback taxonomy of canonical technical skills
DEFAULT_CANONICAL_SKILLS = [
    "Python", "C++", "C", "Java", "JavaScript", "TypeScript", "SQL",
    "MongoDB", "PostgreSQL", "MySQL", "Redis", "Cassandra",
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Scikit-learn",
    "PyTorch", "TensorFlow", "Keras", "NLP", "Computer Vision",
    "Power BI", "Tableau", "Excel", "Statistics", "Data Analysis",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux", "Git",
    "React", "Angular", "Vue.js", "Node.js", "Express", "Django",
    "Flask", "FastAPI", "Spring Boot", "HTML", "CSS", "REST API",
    "Apache Spark", "Hadoop", "Kafka", "Airflow", "CI/CD"
]


def get_known_skills_set() -> Set[str]:
    """
    Fetches the latest set of known canonical skills from MongoDB.
    Falls back to internal default list if MongoDB is offline.
    """
    try:
        db = get_database()
        cursor = db["skills"].find({}, {"name": 1, "_id": 0})
        db_skills = {doc["name"] for doc in cursor if "name" in doc}
        if db_skills:
            return db_skills
    except Exception:
        pass
    return set(DEFAULT_CANONICAL_SKILLS)


def extract_skills_from_text(text: str, custom_skills: Optional[List[str]] = None) -> List[str]:
    """
    Extracts all canonical skills present in the resume text.
    Handles exact casing, symbols (C++, C#, Node.js), and multi-word terms (Power BI, Apache Spark).
    """
    if not text:
        return []

    known_skills = get_known_skills_set()
    if custom_skills:
        known_skills.update(custom_skills)

    detected: Set[str] = set()

    # Pre-clean text slightly for consistent matching
    normalized_text = " " + text + " "

    for skill in known_skills:
        # Construct boundary-safe regex pattern
        # Characters like '+', '.', '#' need escaping, but word boundaries differ for non-word chars
        escaped_skill = re.escape(skill)
        
        # Build robust pattern for both alphanumeric skills and symbolic skills (e.g. C++, C#, Node.js)
        # normalized_text has leading and trailing spaces guaranteed.
        escaped_skill = re.escape(skill)
        
        # Leading delimiter check: must be preceded by whitespace or common punctuation
        # Trailing delimiter check: must be followed by whitespace or common punctuation
        pattern = r"(?:(?<=[\s,;:/\(\)\[\]\{\}]))" + escaped_skill + r"(?:(?=[\s,;:/\(\)\[\]\{\}\.]|$))"
        
        if re.search(pattern, normalized_text, re.IGNORECASE):
            detected.add(skill)

    # Return sorted list of detected skills
    return sorted(list(detected))


def extract_projects_from_text(text: str, detected_skills: List[str]) -> List[Dict[str, Any]]:
    """
    Detects project blocks and maps relevant detected skills to each project.
    """
    projects: List[Dict[str, Any]] = []
    
    # Try finding lines containing "Project" or bullet lines
    lines = text.split("\n")
    current_proj = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check if line indicates a project header
        if re.search(r"(project|developed|built|designed|system|analysis|dashboard|platform)\b", stripped, re.IGNORECASE) and len(stripped) < 70:
            if current_proj:
                projects.append(current_proj)
            techs = [s for s in detected_skills if s.lower() in stripped.lower()]
            current_proj = {
                "name": stripped.title(),
                "technologies": techs,
                "description": stripped
            }
        elif current_proj and len(current_proj["description"]) < 200:
            current_proj["description"] += " " + stripped
            # Add newly discovered skills in project description
            for s in detected_skills:
                if s.lower() in stripped.lower() and s not in current_proj["technologies"]:
                    current_proj["technologies"].append(s)

    if current_proj:
        projects.append(current_proj)

    # If no structured projects were identified, create a generic one from detected skills
    if not projects and detected_skills:
        projects.append({
            "name": "Portfolio & Academic Work",
            "technologies": detected_skills[:4],
            "description": f"Applied technical skills including {', '.join(detected_skills[:4])} across various implementations."
        })

    return projects[:4]
