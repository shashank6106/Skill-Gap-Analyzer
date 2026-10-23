"""
Skill Gap Analyzer - Core Analysis Engine
Modules for PDF parsing, skill extraction, and ML similarity matching.
"""
from engine.resume_parser import extract_text_from_pdf, parse_resume_content
from engine.skill_extractor import extract_skills_from_text, get_known_skills_set
from engine.matcher import calculate_skill_gap, compute_semantic_similarity
from engine.rag_engine import optimize_resume_bullets_rag

__all__ = [
    "extract_text_from_pdf",
    "parse_resume_content",
    "extract_skills_from_text",
    "get_known_skills_set",
    "calculate_skill_gap",
    "compute_semantic_similarity",
    "optimize_resume_bullets_rag"
]
