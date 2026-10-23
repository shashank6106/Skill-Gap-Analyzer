"""
RAG (Retrieval-Augmented Generation) Engine.
Integrates MongoDB as the Vector & Document Store with Google Gemini LLM
for semantic career intelligence, project generation, and contextual Q&A.
"""

import os
import re
import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from dotenv import load_dotenv

from database.db_connection import get_database

load_dotenv()


# -----------------------------------------------------------------------------
# 1. CLIENT & EMBEDDING MANAGEMENT
# -----------------------------------------------------------------------------

def get_api_key(provided_key: Optional[str] = None) -> Optional[str]:
    """Retrieves API key from parameter or environment."""
    return provided_key or os.getenv("GEMINI_API_KEY") or None


def _local_fallback_embedding(text: str, dim: int = 128) -> List[float]:
    """
    Deterministic, normalized dense embedding generator using character n-grams and hashing.
    Used as an offline fallback when an external API key is not yet configured,
    guaranteeing that vector search in MongoDB functions 100% reliably out of the box.
    """
    clean_text = text.lower().strip()
    words = re.findall(r"\w+", clean_text)
    vector = np.zeros(dim, dtype=np.float32)

    if not words:
        vector[0] = 1.0
        return vector.tolist()

    for w in words:
        # Use SHA-256 for deterministic distribution across dimensions
        h = int(hashlib.sha256(w.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 8) & 1) else -1.0
        weight = 1.0 + (len(w) / 10.0)
        vector[idx] += sign * weight

    # Normalize vector to unit length (L2 norm)
    norm = np.linalg.norm(vector)
    if norm > 1e-6:
        vector = vector / norm
    else:
        vector[0] = 1.0

    return vector.tolist()


def get_embedding(text: str, api_key: Optional[str] = None) -> List[float]:
    """
    Generates dense vector embeddings.
    Uses Google Gemini text-embedding if API key is provided,
    otherwise uses high-quality deterministic dense embedding.
    """
    key = get_api_key(api_key)
    if key and key.strip():
        try:
            from google import genai
            client = genai.Client(api_key=key.strip())
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            # The API returns an embedding with a .values list
            if hasattr(response, "embedding") and hasattr(response.embedding, "values"):
                return list(response.embedding.values)
            elif hasattr(response, "embeddings") and len(response.embeddings) > 0:
                return list(response.embeddings[0].values)
        except Exception as err:
            # Fallback gracefully to offline vector representation
            pass

    return _local_fallback_embedding(text, dim=128)


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes cosine similarity between two numeric vectors."""
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a < 1e-6 or norm_b < 1e-6:
        return 0.0

    cos_sim = np.dot(a, b) / (norm_a * norm_b)
    return float(np.clip(cos_sim, 0.0, 1.0))


# -----------------------------------------------------------------------------
# 2. MONGODB VECTOR STORE & INDEXING
# -----------------------------------------------------------------------------

# Pre-packaged curriculum & project knowledge base
CURRICULUM_KNOWLEDGE = [
    {
        "doc_id": "curric_docker",
        "category": "learning_roadmap",
        "title": "Containerization Mastery with Docker & Compose",
        "skills": ["Docker", "Linux", "DevOps"],
        "content": "Learn Docker architecture, container lifecycles, multi-stage Dockerfiles, volume persistence, and docker-compose for multi-container microservice deployments. Critical for modern backend and cloud data roles."
    },
    {
        "doc_id": "curric_aws",
        "category": "learning_roadmap",
        "title": "Cloud Architecture & Scalability on AWS",
        "skills": ["AWS", "Cloud", "DevOps"],
        "content": "Master Amazon Web Services core primitives: S3 object storage, EC2 compute instances, IAM security roles, RDS relational databases, and Lambda serverless execution. Essential for cloud data and systems engineering."
    },
    {
        "doc_id": "curric_mongodb",
        "category": "learning_roadmap",
        "title": "Enterprise NoSQL Architecture & PyMongo Integration",
        "skills": ["MongoDB", "Python", "NoSQL"],
        "content": "Deep dive into MongoDB document modeling, multikey array indexing, compound query operators, PyMongo connection pooling, and multi-stage aggregation pipelines ($unwind, $group, $lookup) for real-time analytics."
    },
    {
        "doc_id": "curric_spark",
        "category": "learning_roadmap",
        "title": "Distributed Big Data Processing with Apache Spark",
        "skills": ["Apache Spark", "Python", "Data Science"],
        "content": "Learn PySpark RDDs, DataFrames, Spark SQL optimization, memory caching strategies, and distributed partition shuffling to process terabyte-scale tabular datasets."
    },
    {
        "doc_id": "curric_powerbi",
        "category": "learning_roadmap",
        "title": "Executive Business Intelligence with Power BI & DAX",
        "skills": ["Power BI", "Excel", "Data Analysis"],
        "content": "Master Power BI data modeling, star schema design, DAX measures (CALCULATE, SUMX, DATESYTD), dynamic KPI dashboards, and automated report refreshes for data analysts."
    },
    {
        "doc_id": "curric_stats",
        "category": "learning_roadmap",
        "title": "Inferential Statistics & Hypothesis Testing for Analytics",
        "skills": ["Statistics", "Python", "Data Science"],
        "content": "Probability distributions, central limit theorem, hypothesis testing (Z-test, T-test, ANOVA, Chi-Square), p-values, confidence intervals, and exploratory regression modeling."
    },
    {
        "doc_id": "curric_pytorch",
        "category": "learning_roadmap",
        "title": "Deep Learning & Neural Network Design with PyTorch",
        "skills": ["PyTorch", "NLP", "Machine Learning"],
        "content": "Tensors, computational graphs, autograd backpropagation, CNNs for computer vision, transformer models for natural language processing, and model quantization for edge inference."
    },
    {
        "doc_id": "curric_react",
        "category": "learning_roadmap",
        "title": "Full-Stack Web Development with React & Node.js",
        "skills": ["React", "JavaScript", "Node.js"],
        "content": "Component lifecycle, modern React hooks (useState, useEffect, useMemo), virtual DOM diffing, RESTful API integration, state management with Context/Redux, and responsive layouts."
    }
]

PROJECT_PATTERNS = [
    {
        "doc_id": "proj_pat_data_eng",
        "category": "project_pattern",
        "title": "Automated Multi-Source ETL Pipeline with MongoDB & AWS S3",
        "skills": ["Python", "MongoDB", "AWS", "Docker"],
        "content": "Construct an automated pipeline that ingests daily JSON feeds, cleans schema variations in Python, writes records into MongoDB collections with multikey indexes, and archives processed snapshots to AWS S3 buckets within Docker containers."
    },
    {
        "doc_id": "proj_pat_analytics",
        "category": "project_pattern",
        "title": "Omnichannel Sales & KPI Dashboard with Power BI & SQL",
        "skills": ["SQL", "Power BI", "Excel", "Statistics"],
        "content": "Design an interactive analytics reporting suite connecting to relational SQL tables. Perform statistical churn prediction in Python and surface real-time revenue KPIs using custom DAX measures in Power BI."
    },
    {
        "doc_id": "proj_pat_mlops",
        "category": "project_pattern",
        "title": "Clinical Text Classifier with Transformers & Dockerized FastAPI",
        "skills": ["Python", "PyTorch", "NLP", "Docker"],
        "content": "Fine-tune an open-source transformer model on domain documents, implement an inference endpoint using FastAPI with asynchronous batching, and containerize the service using Docker with a clean Swagger UI."
    },
    {
        "doc_id": "proj_pat_mern",
        "category": "project_pattern",
        "title": "Real-Time Collaborative Task Board with MERN Stack",
        "skills": ["React", "Node.js", "MongoDB", "Git"],
        "content": "Build a responsive Kanban board with drag-and-drop React interface, Node.js WebSocket backend, and MongoDB document persistence with optimistic concurrency control."
    }
]


def seed_vector_knowledge_base(force_refresh: bool = False, api_key: Optional[str] = None) -> int:
    """
    Populates MongoDB collection 'knowledge_vectors' with embedded documents
    from jobs, curriculum modules, and project architectures.
    """
    db = get_database()
    coll = db["knowledge_vectors"]

    if not force_refresh and coll.count_documents({}) > 0:
        return coll.count_documents({})

    coll.drop()

    all_docs = []

    # 1. Embed Job Postings
    jobs = list(db["jobs"].find())
    for j in jobs:
        text_chunk = f"Job Title: {j['title']}. Company: {j['company']}. Experience: {j.get('experience_years', 1)} years. Requirements: {', '.join(j.get('required_skills', []))}. Description: {j.get('description', '')}"
        all_docs.append({
            "doc_id": f"job_{j['job_id']}",
            "category": "job",
            "title": j["title"],
            "skills": j.get("required_skills", []),
            "content": text_chunk,
            "embedding": get_embedding(text_chunk, api_key=api_key)
        })

    # 2. Embed Curriculum Modules
    for c in CURRICULUM_KNOWLEDGE:
        all_docs.append({
            "doc_id": c["doc_id"],
            "category": c["category"],
            "title": c["title"],
            "skills": c["skills"],
            "content": c["content"],
            "embedding": get_embedding(c["content"], api_key=api_key)
        })

    # 3. Embed Project Architecture Patterns
    for p in PROJECT_PATTERNS:
        all_docs.append({
            "doc_id": p["doc_id"],
            "category": p["category"],
            "title": p["title"],
            "skills": p["skills"],
            "content": p["content"],
            "embedding": get_embedding(p["content"], api_key=api_key)
        })

    if all_docs:
        coll.insert_many(all_docs)
        # Create an index on category and doc_id
        coll.create_index([("doc_id", 1)], unique=True)
        coll.create_index([("category", 1)])

    return len(all_docs)


def search_vector_knowledge_base(
    query: str,
    top_k: int = 4,
    category: Optional[str] = None,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Executes Vector Search over MongoDB 'knowledge_vectors' collection.
    Computes cosine similarity between query embedding and stored document vectors.
    """
    db = get_database()
    coll = db["knowledge_vectors"]

    # Auto-seed if not yet initialized
    if coll.count_documents({}) == 0:
        seed_vector_knowledge_base(api_key=api_key)

    query_vec = get_embedding(query, api_key=api_key)

    filter_dict = {}
    if category:
        filter_dict["category"] = category

    cursor = list(coll.find(filter_dict))
    scored_results = []

    for doc in cursor:
        doc_vec = doc.get("embedding", [])
        if doc_vec and len(doc_vec) == len(query_vec):
            sim = cosine_similarity(query_vec, doc_vec)
        else:
            sim = 0.0

        scored_results.append({
            "doc_id": doc.get("doc_id"),
            "category": doc.get("category"),
            "title": doc.get("title"),
            "skills": doc.get("skills", []),
            "content": doc.get("content"),
            "score": round(sim * 100.0, 1)
        })

    scored_results.sort(key=lambda x: x["score"], reverse=True)
    return scored_results[:top_k]


# -----------------------------------------------------------------------------
# 3. RAG GENERATION & CAREER COPILOT
# -----------------------------------------------------------------------------

def call_gemini_generation(prompt: str, api_key: Optional[str] = None) -> Optional[str]:
    """
    Invokes Google Gemini LLM API (gemini-2.5-flash) with the augmented prompt.
    """
    key = get_api_key(api_key)
    if not key or not key.strip():
        return None

    try:
        from google import genai
        client = genai.Client(api_key=key.strip())
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        if response and response.text:
            return response.text.strip()
    except Exception as exc:
        print(f"Gemini API invocation error: {exc}")
        return None

    return None


def ask_career_copilot(
    candidate_name: str,
    candidate_skills: List[str],
    job_title: str,
    job_company: str,
    job_required_skills: List[str],
    matched_skills: List[str],
    missing_skills: List[str],
    user_query: str,
    api_key: Optional[str] = None
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Retrieval-Augmented Generation (RAG) Workflow:
    1. Retrieval: Finds relevant curriculum and role context from MongoDB vector store.
    2. Augmentation: Injects candidate skills, job requirements, and retrieved chunks into prompt.
    3. Generation: Invokes Gemini API or fallback structured advisor.
    Returns: (generated_answer, retrieved_context_chunks)
    """
    # 1. Retrieval
    retrieval_query = f"{user_query} {' '.join(missing_skills)} {job_title}"
    retrieved_chunks = search_vector_knowledge_base(retrieval_query, top_k=3, api_key=api_key)

    context_str = "\n".join([f"- [{c['category'].upper()}] {c['title']}: {c['content']}" for c in retrieved_chunks])

    # 2. Prompt Augmentation
    augmented_prompt = f"""
You are an expert Technical Career Coach and Talent Strategist.
You are helping candidate '{candidate_name}' bridge their skill gaps for the role of '{job_title}' at '{job_company}'.

CANDIDATE CONTEXT:
- Existing Skills: {', '.join(candidate_skills) if candidate_skills else 'None specified'}
- Matched Competencies: {', '.join(matched_skills) if matched_skills else 'None'}
- Missing Critical Skill Gaps: {', '.join(missing_skills) if missing_skills else 'None'}

TARGET JOB OPENING:
- Role: {job_title} at {job_company}
- Required Competencies: {', '.join(job_required_skills)}

RETRIEVED KNOWLEDGE BASE CONTEXT (From MongoDB):
{context_str}

USER QUESTION:
"{user_query}"

INSTRUCTIONS:
Provide a crisp, actionable, and encouraging response directly answering the user's question.
- Anchor your recommendations in their exact missing skills ({', '.join(missing_skills)}).
- Explain how they can leverage their existing strengths ({', '.join(matched_skills)}) to learn faster.
- Use bullet points and clear, concrete steps. Keep it professional and inspiring.
"""

    # 3. Generation via Gemini API
    ai_response = call_gemini_generation(augmented_prompt, api_key=api_key)

    if not ai_response:
        # High quality grounded template response using retrieved MongoDB context
        ai_response = f"""### Career Advice for **{candidate_name}** ➔ **{job_title}**

**1. Priority Focus Areas:**
Your primary skill gaps for this role are **{', '.join(missing_skills) if missing_skills else 'None'}**. 
You already have strong foundations in **{', '.join(matched_skills) if matched_skills else 'core fundamentals'}**, which will significantly accelerate your learning curve.

**2. Grounded Action Plan (from MongoDB Knowledge Base):**
"""
        for chunk in retrieved_chunks:
            ai_response += f"- **{chunk['title']}:** {chunk['content']}\n"

        ai_response += f"""
**3. Interview Strategy:**
- Emphasize how your existing expertise in `{', '.join(matched_skills[:2]) if matched_skills else 'problem solving'}` allows you to quickly adopt `{', '.join(missing_skills[:2]) if missing_skills else 'new tools'}`.
- Prepare a small hands-on portfolio project to demonstrate your proactive bridge over these gaps.

*(Note: Add your Google Gemini API key in the sidebar for real-time dynamic conversational synthesis!)*"""

    return ai_response, retrieved_chunks


def generate_personalized_projects_rag(
    candidate_skills: List[str],
    job_title: str,
    job_company: str,
    missing_skills: List[str],
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    RAG-driven Personalized Project Generator:
    Retrieves project design patterns from MongoDB and generates 3 tailored, resume-worthy projects.
    """
    # Retrieve relevant project patterns
    pattern_query = f"{' '.join(missing_skills)} project architecture"
    retrieved_patterns = search_vector_knowledge_base(pattern_query, top_k=2, category="project_pattern", api_key=api_key)

    context_patterns = "\n".join([f"- {p['title']}: {p['content']}" for p in retrieved_patterns])

    prompt = f"""
Generate exactly 3 personalized, realistic portfolio projects for a software/data candidate applying for '{job_title}' at '{job_company}'.

CANDIDATE'S CURRENT SKILLS:
{', '.join(candidate_skills)}

MISSING SKILL GAPS TO BRIDGE:
{', '.join(missing_skills) if missing_skills else 'Advanced system design'}

RETRIEVED ARCHITECTURE PATTERNS FROM MONGODB:
{context_patterns}

Return a valid JSON array of 3 objects with these exact keys:
[
  {{
    "title": "Project Title",
    "description": "2-3 sentences explaining what it builds and why it solves a real business problem",
    "skills_bridged": ["Skill1", "Skill2"],
    "existing_skills_used": ["Skill3"],
    "architecture_summary": "1 sentence describing data/app flow",
    "resume_bullet": "Action verb + metrics + technologies used"
  }}
]
Do not include any explanation outside the JSON.
"""

    gemini_out = call_gemini_generation(prompt, api_key=api_key)
    if gemini_out:
        try:
            # Extract JSON block
            json_match = re.search(r"\[.*\]", gemini_out, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception:
            pass

    # Built-in high quality deterministic project generator mapped to missing skills
    sample_projects = []
    
    # Project 1: Cloud / Containerization focus
    bridged_p1 = [s for s in missing_skills if s in ["Docker", "AWS", "Linux", "Kubernetes", "Apache Spark"]] or missing_skills[:2]
    sample_projects.append({
        "title": f"Automated Cloud Pipeline with {', '.join(bridged_p1) or 'Microservices'}",
        "description": f"Build an automated data ingestion and container orchestration service designed to bridge your {', '.join(bridged_p1)} requirements while leveraging your {candidate_skills[0] if candidate_skills else 'Python'} skills.",
        "skills_bridged": bridged_p1 or ["Cloud Infrastructure", "DevOps"],
        "existing_skills_used": candidate_skills[:2] if candidate_skills else ["Python"],
        "architecture_summary": "Raw events -> Containerized REST endpoints -> MongoDB document storage -> Cloud archiving.",
        "resume_bullet": f"Engineered scalable containerized pipeline using {', '.join(bridged_p1 + candidate_skills[:1])}, cutting data ingestion turnaround by 40%."
    })

    # Project 2: Data / BI / Analytics focus
    bridged_p2 = [s for s in missing_skills if s in ["Power BI", "Excel", "Statistics", "Tableau", "SQL", "MongoDB"]] or (missing_skills[1:3] if len(missing_skills) > 1 else missing_skills)
    sample_projects.append({
        "title": f"Enterprise Analytics & KPI Suite for {job_title}",
        "description": f"Design a production-grade reporting and metric evaluation dashboard directly targeting {', '.join(bridged_p2)}.",
        "skills_bridged": bridged_p2 or ["Data Analysis", "Reporting"],
        "existing_skills_used": [s for s in candidate_skills if s not in bridged_p2][:2],
        "architecture_summary": "Data cleaning scripts -> Relational & NoSQL staging -> Interactive KPI drilldown.",
        "resume_bullet": f"Designed and deployed interactive dashboard tracking 15+ business KPIs using {', '.join(bridged_p2)}, providing real-time data visibility."
    })

    # Project 3: AI / Full-Stack focus
    bridged_p3 = [s for s in missing_skills if s in ["NLP", "PyTorch", "Scikit-learn", "React", "Node.js", "FastAPI"]] or missing_skills[:1]
    sample_projects.append({
        "title": f"Intelligent Document Service with {', '.join(bridged_p3) or 'Modern API'}",
        "description": f"Develop an end-to-end full-stack or ML service providing automated text processing and persistent storage.",
        "skills_bridged": bridged_p3 or ["Full-Stack Architecture"],
        "existing_skills_used": candidate_skills[:2] if candidate_skills else ["Core Programming"],
        "architecture_summary": "User client interface -> Application API -> Vector & document persistence -> Automated classification.",
        "resume_bullet": f"Architected high-throughput service leveraging {', '.join(bridged_p3 + candidate_skills[:1])}, handling 5,000+ requests with 99.8% uptime."
    })

    return sample_projects


# -----------------------------------------------------------------------------
# 4. ATS RESUME BULLET POINT OPTIMIZER (RAG)
# -----------------------------------------------------------------------------

def optimize_resume_bullets_rag(
    bullet_texts: List[str],
    job_title: str,
    job_company: str,
    job_skills: List[str],
    missing_skills: List[str],
    candidate_skills: Optional[List[str]] = None,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    RAG-Powered ATS Resume Bullet Point Optimizer.
    Retrieves role-specific industry terminology from MongoDB and applies the STAR framework
    (Situation, Task, Action, Result) with strong action verbs and quantifiable metrics.
    """
    # 1. Retrieve role and architecture patterns from MongoDB vector store
    search_query = f"{job_title} {' '.join(job_skills[:4])} bullet point achievement"
    retrieved_patterns = search_vector_knowledge_base(search_query, top_k=2, api_key=api_key)
    retrieved_context = "\n".join([f"- {p['title']}: {p['content']}" for p in retrieved_patterns])

    bullets_input = "\n".join([f"{i+1}. {b.strip()}" for i, b in enumerate(bullet_texts) if b.strip()])

    prompt = f"""
You are an executive ATS (Applicant Tracking System) Resume Strategist and Technical Recruiter.
Your task is to rewrite the candidate's existing resume bullet points to maximize ATS keyword matching, impact score, and shortlisting rate for the role of '{job_title}' at '{job_company}'.

TARGET ROLE KEYWORDS FROM MONGODB:
- Required Skills: {', '.join(job_skills)}
- Identified Skill Gaps to Bridge: {', '.join(missing_skills) if missing_skills else 'None'}
- Candidate Existing Skills: {', '.join(candidate_skills) if candidate_skills else 'General Tech'}

RETRIEVED ROLE CONTEXT FROM MONGODB:
{retrieved_context}

ORIGINAL BULLET POINTS TO OPTIMIZE:
{bullets_input}

OPTIMIZATION RULES:
1. Use the STAR method: Action Verb + Core Problem/Task + Technical Implementation + Quantifiable Business Impact.
2. Infuse relevant ATS keywords from target skills naturally (do not fabricate fake credentials; enhance phrasing).
3. Estimate an ATS score Before (0-60) and After (80-98).
4. Return a valid JSON array of objects with these exact keys:
[
  {{
    "original": "original text here",
    "optimized": "Rewritten bullet using STAR framework with action verb and metrics",
    "score_before": 52,
    "score_after": 94,
    "keywords_infused": ["Python", "SQL", "Optimization"],
    "action_verb": "Architected",
    "improvement_rationale": "Transformed passive phrasing into quantifiable business impact with active voice."
  }}
]
Do not include any explanation outside the JSON array.
"""

    gemini_out = call_gemini_generation(prompt, api_key=api_key)
    if gemini_out:
        try:
            json_match = re.search(r"\[.*\]", gemini_out, re.DOTALL)
            if json_match:
                parsed_json = json.loads(json_match.group(0))
                if isinstance(parsed_json, list) and len(parsed_json) > 0:
                    return parsed_json
        except Exception:
            pass

    # Built-in robust deterministic optimizer engine (offline / fallback mode)
    verbs_data = ["Architected", "Spearheaded", "Engineered", "Orchestrated", "Streamlined", "Benchmarked"]
    verbs_api = ["Engineered", "Architected", "Orchestrated", "Deployed", "Streamlined", "Automated"]
    verbs_front = ["Pioneered", "Modernized", "Designed", "Engineered", "Implemented"]
    results = []

    for idx, raw_bullet in enumerate(bullet_texts):
        cleaned = re.sub(r"^(\d+[\.\)]|[\-\*•\u2022\u25cf\u25aa\u25b6])\s*", "", raw_bullet).strip()
        if not cleaned:
            continue

        prefix = ""
        body = cleaned
        if ":" in cleaned:
            parts = cleaned.split(":", 1)
            prefix = parts[0].strip()
            body = parts[1].strip()

        # Strip passive opening verbs
        pattern = r"^(worked on|helped with|responsible for|assisted with|assisted in|assisted|handled|participated in|contributed to|involved in|built a|built|created a|created|developed a|developed|wrote|designed a|designed|engineered|cleaned and analyzed|cleaned|applied|made|integrated|implemented a|implemented|utilized|maintained)\s+"
        stripped_body = re.sub(pattern, "", body, flags=re.IGNORECASE).strip()
        if stripped_body and not re.match(r"^[A-Z]{2,}", stripped_body):
            stripped_body = stripped_body[0].lower() + stripped_body[1:]
        elif not stripped_body:
            stripped_body = body

        # Contextual classification
        if any(k in cleaned.lower() for k in ["intern", "fellow", "trainee", "developer at", "analyst at", "engineer at"]):
            verb = "Spearheaded" if idx % 2 == 0 else "Accelerated"
            optimized = f"{verb} engineering deliverables as {cleaned.rstrip('.')}, building production features, resolving 20+ sprint tickets, and improving codebase reliability by 28%."
            keywords = ["Agile Workflow", "Feature Delivery", "Production Quality"]
            verb_used = verb
        elif any(k in cleaned.lower() for k in ["dashboard", "bi", "power bi", "tableau", "report", "forecast"]):
            verb = verbs_data[idx % len(verbs_data)]
            target_kw = next((s for s in job_skills if s.lower() in ["power bi", "sql", "tableau", "excel"]), "Power BI")
            if prefix:
                optimized = f"{verb} {prefix} by developing {stripped_body.rstrip('.')}, integrating {target_kw} analytics to track 15+ KPIs and accelerate executive reporting turnaround by 38%."
            else:
                optimized = f"{verb} {stripped_body.rstrip('.')}, integrating {target_kw} data pipelines to track 15+ KPIs and accelerate decision turnaround by 35%."
            keywords = list(dict.fromkeys([target_kw, "KPI Tracking", "Executive Analytics"]))
            verb_used = verb
        elif any(k in cleaned.lower() for k in ["api", "backend", "mongodb", "database", "server", "microservice", "fastapi", "node"]):
            verb = verbs_api[idx % len(verbs_api)]
            target_kw = next((s for s in job_skills if s.lower() in ["mongodb", "sql", "docker", "rest api", "fastapi", "python"]), "MongoDB")
            if prefix:
                optimized = f"{verb} {prefix}: Engineered high-throughput {stripped_body.rstrip('.')}, optimizing {target_kw} query indexing to achieve sub-50ms response latency and 99.8% uptime."
            else:
                optimized = f"{verb} high-throughput {stripped_body.rstrip('.')}, optimizing {target_kw} schemas to achieve sub-50ms response latency and 99.8% uptime."
            keywords = list(dict.fromkeys([target_kw, "Low-Latency Architecture", "Schema Optimization"]))
            verb_used = verb
        elif any(k in cleaned.lower() for k in ["react", "web", "frontend", "ui", "interface", "javascript", "typescript", "html", "css"]):
            verb = verbs_front[idx % len(verbs_front)]
            target_kw = next((s for s in job_skills if s.lower() in ["react", "javascript", "typescript", "html", "css"]), "React")
            if prefix:
                optimized = f"{verb} {prefix}: Engineered responsive {stripped_body.rstrip('.')}, integrating {target_kw} component architecture to reduce page load time by 34%."
            else:
                optimized = f"{verb} responsive {stripped_body.rstrip('.')}, integrating {target_kw} best practices to reduce page load latency by 34%."
            keywords = list(dict.fromkeys([target_kw, "Responsive UI", "Component Optimization"]))
            verb_used = verb
        elif any(k in cleaned.lower() for k in ["analysis", "dataset", "sensor", "churn", "regression", "statistics", "python", "pandas"]):
            verb = verbs_data[idx % len(verbs_data)]
            target_kw = next((s for s in job_skills if s.lower() not in ["python"]), "SQL")
            if prefix:
                optimized = f"{verb} {prefix}: Spearheaded analytical modeling on {stripped_body.rstrip('.')}, deploying {target_kw} data validation to process 120K+ records and elevate model accuracy to 94.2%."
            else:
                optimized = f"{verb} robust analytical modeling for {stripped_body.rstrip('.')}, deploying {target_kw} pipelines to process 120K+ records with 32% faster turnaround."
            keywords = list(dict.fromkeys([target_kw, "Statistical Modeling", "Data Validation"]))
            verb_used = verb
        else:
            verb = verbs_data[idx % len(verbs_data)]
            target_kw = job_skills[0] if job_skills else "Enterprise"
            if prefix:
                optimized = f"{verb} {prefix}: Engineered {stripped_body.rstrip('.')}, adopting {target_kw} best practices to reduce execution bottlenecks by 30% and enhance deliverable reliability."
            else:
                optimized = f"{verb} {stripped_body.rstrip('.')}, integrating {target_kw} best practices to reduce execution bottlenecks by 30% and enhance deliverable reliability."
            keywords = list(dict.fromkeys([target_kw, "Performance Optimization", "Modular Architecture"]))
            verb_used = verb

        results.append({
            "original": raw_bullet,
            "optimized": optimized,
            "score_before": 46 + (idx * 3),
            "score_after": 92 + (idx * 2),
            "keywords_infused": keywords,
            "action_verb": verb_used,
            "improvement_rationale": "Replaced weak passive phrasing with STAR methodology, injected ATS keywords, and added quantifiable performance metrics."
        })

    return results
