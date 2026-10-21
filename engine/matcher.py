"""
Skill Gap Matcher and Scikit-learn Similarity Engine.
Calculates direct skill overlap, missing skills, TF-IDF cosine similarity,
and compiles learning recommendations from MongoDB.
"""

from typing import List, Dict, Any, Set, Tuple, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database.crud import get_recommendations_for_skills
from database.aggregations import get_most_demanded_job_skills


def compute_direct_skill_match(
    candidate_skills: List[str],
    job_required_skills: List[str]
) -> Tuple[List[str], List[str], List[str], float]:
    """
    Computes exact set overlap between candidate skills and job requirements.
    Returns: (matched_skills, missing_skills, extra_skills, direct_score_percentage)
    """
    # Create case-insensitive lookup dictionaries mapped back to original display casing
    cand_dict = {s.strip().lower(): s.strip() for s in candidate_skills if s.strip()}
    job_dict = {s.strip().lower(): s.strip() for s in job_required_skills if s.strip()}

    cand_set: Set[str] = set(cand_dict.keys())
    job_set: Set[str] = set(job_dict.keys())

    matched_keys = sorted(list(cand_set.intersection(job_set)))
    missing_keys = sorted(list(job_set - cand_set))
    extra_keys = sorted(list(cand_set - job_set))

    # Map keys back to original nice casing (preferring job casing for requirements)
    matched_skills = [job_dict.get(k, cand_dict.get(k, k)) for k in matched_keys]
    missing_skills = [job_dict[k] for k in missing_keys]
    extra_skills = [cand_dict[k] for k in extra_keys]

    if not job_required_skills:
        score = 100.0 if candidate_skills else 0.0
    else:
        score = round((len(matched_skills) / len(job_required_skills)) * 100.0, 1)

    return matched_skills, missing_skills, extra_skills, score


def compute_semantic_similarity(text_a: str, text_b: str) -> float:
    """
    Computes Scikit-learn TF-IDF vectorization and Cosine Similarity
    between two blocks of text (Resume Text vs Job Description).
    Returns similarity score between 0.0 and 100.0.
    """
    if not text_a.strip() or not text_b.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=1000,
            ngram_range=(1, 2)
        )
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        # Scale to 0-100 range
        scaled_score = round(float(np.clip(cos_sim * 100.0, 0.0, 100.0)), 1)
        return scaled_score
    except Exception:
        return 0.0


def calculate_skill_gap(
    candidate_skills: List[str],
    job: Dict[str, Any],
    resume_text: str = "",
    user_id: Optional[int] = None,
    user_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Comprehensive Skill Gap Analysis Orchestrator.
    Combines:
    1. Direct Skill Overlap (70% weight)
    2. Semantic TF-IDF similarity between Resume text and Job description (30% weight)
    3. Targeted Course & Roadmap Recommendations from MongoDB
    """
    job_id = job.get("job_id", 0)
    job_title = job.get("title", "Unknown Role")
    company = job.get("company", "Unknown Company")
    job_skills = job.get("required_skills", [])
    job_desc = job.get("description", "") + " " + " ".join(job_skills)

    # 1. Compute direct skill matching
    matched_skills, missing_skills, extra_skills, direct_score = compute_direct_skill_match(
        candidate_skills, job_skills
    )

    # 2. Compute semantic TF-IDF text similarity
    if not resume_text and candidate_skills:
        resume_text = "Experienced in " + ", ".join(candidate_skills)
    semantic_score = compute_semantic_similarity(resume_text, job_desc)

    # 3. Hybrid Match Score (70% direct skill match + 30% semantic text similarity)
    if job_skills:
        final_score = round((0.70 * direct_score) + (0.30 * semantic_score), 1)
    else:
        final_score = semantic_score

    # 4. Fetch targeted learning recommendations from MongoDB
    recommendations_list = []
    if missing_skills:
        db_recs = get_recommendations_for_skills(missing_skills)
        rec_by_skill = {r["skill"].lower(): r for r in db_recs}

        # Check job market demand to dynamically prioritize missing skills
        try:
            market_demand, _ = get_most_demanded_job_skills(limit=20)
            demand_map = {item["skill"].lower(): item["demand_frequency"] for item in market_demand}
        except Exception:
            demand_map = {}

        for missing in missing_skills:
            low_missing = missing.lower()
            rec = rec_by_skill.get(low_missing)
            
            # Determine dynamic priority based on demand frequency in MongoDB
            freq = demand_map.get(low_missing, 1)
            if freq >= 3:
                priority = "High"
            elif freq == 2:
                priority = "Medium"
            else:
                priority = "Normal"

            if rec:
                recommendations_list.append({
                    "skill": missing,
                    "priority": rec.get("priority", priority),
                    "course_title": rec.get("course_title", f"Mastering {missing}"),
                    "platform": rec.get("platform", "Online Course"),
                    "estimated_hours": rec.get("estimated_hours", 20),
                    "roadmap": rec.get("roadmap", f"Learn fundamentals of {missing} and build 1 practical project."),
                    "resource_url": rec.get("resource_url", "#")
                })
            else:
                recommendations_list.append({
                    "skill": missing,
                    "priority": priority,
                    "course_title": f"Complete {missing} Professional Guide",
                    "platform": "Self-Paced / Official Documentation",
                    "estimated_hours": 15,
                    "roadmap": f"1. Core syntax & concepts of {missing} -> 2. Build practice project.",
                    "resource_url": "https://google.com/search?q=" + missing + "+tutorial"
                })

    # Sort recommendations by priority: High first, then Medium, then Normal
    priority_order = {"High": 1, "Medium": 2, "Normal": 3}
    recommendations_list.sort(key=lambda r: priority_order.get(r["priority"], 4))

    return {
        "user_id": user_id,
        "user_name": user_name or "Candidate",
        "job_id": job_id,
        "job_title": job_title,
        "company": company,
        "match_score": final_score,
        "direct_skill_score": direct_score,
        "semantic_score": semantic_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "candidate_skills": candidate_skills,
        "job_required_skills": job_skills,
        "recommendations": recommendations_list,
        "status": "Evaluated"
    }
