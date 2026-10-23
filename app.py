"""
Skill Gap Analyzer
Minimalist Light & Dark Enterprise Edition with RAG Engine.
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.db_connection import check_connection, get_database
from database.crud import (
    insert_user, get_user_by_id, get_all_users, update_user_skills, pull_skill_from_user, delete_user,
    insert_job, get_all_jobs, find_jobs_by_skills,
    insert_analysis, get_all_skills, get_next_id, save_optimized_bullets
)
from database.aggregations import (
    get_system_kpis, get_most_matched_skills, get_most_common_missing_skills,
    get_most_demanded_job_skills, get_job_performance_breakdown,
    get_score_distribution_aggregation, get_candidate_supply_vs_demand
)
from database.seed_data import seed_database
from engine.resume_parser import parse_resume_content
from engine.skill_extractor import extract_skills_from_text
from engine.matcher import calculate_skill_gap
from engine.rag_engine import (
    seed_vector_knowledge_base, search_vector_knowledge_base,
    ask_career_copilot, generate_personalized_projects_rag,
    optimize_resume_bullets_rag
)


# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Skill Gap Analyzer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# MINIMALIST LIGHT & DARK CUSTOM CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .app-header {
        padding: 0.8rem 0 1.2rem 0;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    .app-title {
        font-size: 1.85rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #0F172A;
        margin: 0;
    }
    .app-tagline {
        font-size: 0.95rem;
        color: #64748B;
        margin-top: 0.25rem;
        font-weight: 400;
    }
    .status-pill-online {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #0F172A;
        color: #F8FAFC;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
    }

    /* Minimalist Stat Cards */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .metric-card:hover {
        border-color: #0F172A;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    /* Minimalist Badges */
    .badge-match {
        display: inline-flex;
        align-items: center;
        background-color: #F0FDF4;
        color: #166534;
        border: 1px solid #BBF7D0;
        padding: 3px 10px;
        margin: 3px 4px 3px 0;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .badge-gap {
        display: inline-flex;
        align-items: center;
        background-color: #FFF1F2;
        color: #9F1239;
        border: 1px solid #FECDD3;
        padding: 3px 10px;
        margin: 3px 4px 3px 0;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .badge-neutral {
        display: inline-flex;
        align-items: center;
        background-color: #F8FAFC;
        color: #334155;
        border: 1px solid #E2E8F0;
        padding: 3px 10px;
        margin: 3px 4px 3px 0;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .badge-dark {
        display: inline-flex;
        align-items: center;
        background-color: #0F172A;
        color: #F8FAFC;
        padding: 3px 10px;
        margin: 3px 4px 3px 0;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Score Card */
    .score-container {
        background: #0F172A;
        color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .score-number {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
        color: #FFFFFF;
        margin: 0.5rem 0;
    }
    .score-sub {
        font-size: 0.85rem;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Cards */
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.1rem;
        margin-bottom: 0.9rem;
    }
    .card-box-accent {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 3px solid #0F172A;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.85rem;
    }

    /* Priority Badges */
    .priority-tag-high {
        background-color: #0F172A;
        color: #FFFFFF;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .priority-tag-medium {
        background-color: #334155;
        color: #FFFFFF;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        border-right: 1px solid #334155;
    }
    .sidebar-brand {
        padding: 0.5rem 0 1.2rem 0;
        border-bottom: 1px solid #334155;
        margin-bottom: 1.2rem;
    }
    .sidebar-title {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #F8FAFC;
        margin: 0;
    }
    .sidebar-sub {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SIDEBAR: CONTROLS & API CONFIG
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-title">SKILL GAP ANALYZER</div>
        <div class="sidebar-sub">RAG-Powered Career Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    is_connected, conn_msg, server_info = check_connection()
    if is_connected:
        st.markdown("""
        <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 10px 14px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="status-dot"></span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #F8FAFC;">Data Engine Online</span>
            </div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">MongoDB Connected</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 10px 14px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="width: 7px; height: 7px; background-color: #F59E0B; border-radius: 50%; display: inline-block;"></span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #F8FAFC;">Demo Mode (Active)</span>
            </div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Sample Dataset Loaded</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Database Status Note"):
            st.caption(f"Status: {conn_msg}")
            st.caption("The app is currently serving pre-calculated sample data. Once your MongoDB Atlas connection is active, it switches to live database queries automatically.")

    # Gemini API Key Input
    st.markdown("<p style='font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:0.25rem;'>AI & LLM Configuration</p>", unsafe_allow_html=True)
    gemini_key_input = st.text_input(
        "Google Gemini API Key (Optional)",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Optional: Paste your key from https://aistudio.google.com/app/apikey. If empty, high-quality local RAG synthesis runs automatically."
    )
    if gemini_key_input:
        os.environ["GEMINI_API_KEY"] = gemini_key_input.strip()
        st.caption("🟢 Gemini API Key Active")
    else:
        st.caption("⚪ Local RAG Mode Active (Free/Offline)")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:0.5rem;'>Vector & Database Management</p>", unsafe_allow_html=True)
    
    if st.button("Reset / Reload Dataset & Vectors", use_container_width=True):
        with st.spinner("Seeding database and vector embeddings..."):
            seed_database(drop_existing=True)
            v_count = seed_vector_knowledge_base(force_refresh=True, api_key=gemini_key_input)
            st.success(f"Dataset refreshed with {v_count} vector documents!")
            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:0.5rem;'>Architecture Stack</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.8;">
        • LLM: Google Gemini (gemini-2.5-flash)<br>
        • Vector Search: MongoDB Embeddings<br>
        • Database Driver: PyMongo<br>
        • Text Parsing: PyPDF v5<br>
        • ML Matching: Scikit-Learn TF-IDF<br>
        • Interface: Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">Skill Gap Analyzer</h1>
        <div class="app-tagline">RAG-driven competency benchmarking, automated resume analysis, and tailored career intelligence</div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("""
    <div style="text-align: right; padding-top: 1.2rem;">
        <span class="status-pill-online">
            <span class="status-dot"></span> System Active
        </span>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TOP METRICS ROW
# -----------------------------------------------------------------------------
kpis = get_system_kpis()
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Candidates</div>
        <div class="metric-value">{kpis["total_users"]}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Target Roles</div>
        <div class="metric-value">{kpis["total_jobs"]}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Evaluations</div>
        <div class="metric-value">{kpis["total_analyses"]}</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Avg Match Score</div>
        <div class="metric-value">{kpis["avg_score"]}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MAIN NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_analysis, tab_optimizer, tab_copilot, tab_projects, tab_vector, tab_jobs, tab_analytics, tab_console = st.tabs([
    "Skill Gap Analysis",
    "ATS Bullet Optimizer (RAG)",
    "AI Career Copilot (RAG)",
    "Project Generator (RAG)",
    "Vector Search Explorer",
    "Job Openings",
    "Market Analytics",
    "Data Engine & Query Lab"
])


# =============================================================================
# TAB 1: SKILL GAP ANALYSIS
# =============================================================================
with tab_analysis:
    st.markdown("##### Evaluate Candidate Resume Against Target Role")
    
    col_cand, col_target = st.columns([1, 1], gap="large")

    with col_cand:
        st.markdown("<p style='font-size:0.9rem; font-weight:600; color:#0F172A; margin-bottom:0.4rem;'>1. Candidate Profile</p>", unsafe_allow_html=True)
        profile_mode = st.radio(
            "Profile Source:",
            ["Sample Resumes", "Select Existing Candidate", "Upload PDF Resume"],
            horizontal=True,
            label_visibility="collapsed"
        )

        extracted_name = "Candidate"
        extracted_email = ""
        extracted_skills = []
        extracted_bullets = []
        raw_text = ""
        user_id = None

        if profile_mode == "Sample Resumes":
            sample_options = [
                ("Shashank (Data & Python Profile)", "sample_resumes/shashank_resume.pdf"),
                ("Ananya (Analytics & BI Profile)", "sample_resumes/ananya_resume.pdf"),
                ("Rahul (Full Stack Web Profile)", "sample_resumes/rahul_resume.pdf")
            ]
            chosen_sample = st.selectbox("Select Sample Resume:", [s[0] for s in sample_options])
            sample_path = next(s[1] for s in sample_options if s[0] == chosen_sample)
            if os.path.exists(sample_path):
                parsed = parse_resume_content(sample_path, filename=os.path.basename(sample_path))
                raw_text = parsed["raw_text"]
                extracted_name = parsed["parsed_name"]
                extracted_email = parsed["email"]
                extracted_skills = extract_skills_from_text(raw_text)
                extracted_bullets = parsed.get("extracted_bullets", [])

        elif profile_mode == "Select Existing Candidate":
            users = get_all_users()
            if not users:
                from database.seed_data import USERS_DATA
                users = USERS_DATA
            user_map = {f"{u['name']} (ID: {u['user_id']})": u for u in users}
            user_keys = list(user_map.keys())
            selected_u_label = st.selectbox("Select Candidate Record:", user_keys) if user_keys else None
            if selected_u_label and selected_u_label in user_map:
                u_obj = user_map[selected_u_label]
                user_id = u_obj["user_id"]
                extracted_name = u_obj["name"]
                extracted_email = u_obj.get("email", "")
                extracted_skills = u_obj.get("skills", [])
                raw_text = f"Candidate {extracted_name}. Core skills: {', '.join(extracted_skills)}."
                if u_obj.get("optimized_bullets"):
                    extracted_bullets = [b.get("optimized", b.get("original", "")) for b in u_obj["optimized_bullets"]]
                else:
                    extracted_bullets = [
                        f"Developed scalable data processing workflows using {', '.join(extracted_skills[:2]) if extracted_skills else 'Python'}.",
                        f"Maintained enterprise applications using {extracted_skills[0] if extracted_skills else 'Python'} and database schemas."
                    ]

        else: # Upload PDF
            uploaded = st.file_uploader("Upload Resume Document (PDF)", type=["pdf"], label_visibility="collapsed")
            if uploaded is not None:
                parsed = parse_resume_content(uploaded.read(), filename=uploaded.name)
                raw_text = parsed["raw_text"]
                extracted_name = parsed["parsed_name"]
                extracted_email = parsed["email"]
                extracted_skills = extract_skills_from_text(raw_text)
                extracted_bullets = parsed.get("extracted_bullets", [])

        # Automatically synchronize active candidate context across tabs
        st.session_state["current_candidate_name"] = extracted_name
        st.session_state["current_candidate_skills"] = extracted_skills
        st.session_state["current_candidate_bullets"] = extracted_bullets
        st.session_state["current_resume_raw_text"] = raw_text
        st.session_state["current_user_id"] = user_id or 101

        # Auto-update ATS Bullet Optimizer input if switching candidates
        if st.session_state.get("last_loaded_candidate") != extracted_name:
            st.session_state["last_loaded_candidate"] = extracted_name
            if extracted_bullets:
                st.session_state["raw_bullet_input"] = "\n".join(extracted_bullets)
            st.session_state.pop("optimized_bullets", None)

        with st.container(border=True):
            st.markdown(f"**Name:** {extracted_name} &nbsp;|&nbsp; **Contact:** {extracted_email or 'Not specified'}")
            st.markdown("<p style='font-size:0.8rem; font-weight:600; color:#64748B; margin-top:0.5rem; margin-bottom:0.25rem;'>DETECTED SKILLS</p>", unsafe_allow_html=True)
            if extracted_skills:
                badges_html = "".join([f'<span class="badge-neutral">{s}</span>' for s in extracted_skills])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.caption("No skills extracted yet.")

            if st.session_state.get("optimized_bullets"):
                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                with st.expander(f"✨ View {len(st.session_state['optimized_bullets'])} ATS-Optimized Bullets for this Candidate"):
                    for ob in st.session_state["optimized_bullets"]:
                        st.markdown(f"• **{ob.get('action_verb', 'STAR')}**: {ob.get('optimized')}")

    with col_target:
        st.markdown("<p style='font-size:0.9rem; font-weight:600; color:#0F172A; margin-bottom:0.4rem;'>2. Target Job Role</p>", unsafe_allow_html=True)
        jobs = get_all_jobs()
        if not jobs:
            from database.seed_data import JOBS_DATA
            jobs = JOBS_DATA

        job_map = {f"{j['title']} — {j['company']}": j for j in jobs}
        job_keys = list(job_map.keys())
        selected_job_key = st.selectbox("Select Target Opening:", job_keys) if job_keys else None
        selected_job = job_map.get(selected_job_key, jobs[0] if jobs else {"title": "Data Analyst", "company": "ABC Technologies", "required_skills": ["Python", "SQL"]})

        with st.container(border=True):
            st.markdown(f"**Role:** {selected_job.get('title', 'Role')}")
            st.markdown(f"**Company:** {selected_job.get('company', 'Company')} &nbsp;|&nbsp; **Experience Required:** {selected_job.get('experience_years', 1)}+ years")
            st.markdown(f"*{selected_job.get('description', '')}*")
            st.markdown("<p style='font-size:0.8rem; font-weight:600; color:#64748B; margin-top:0.5rem; margin-bottom:0.25rem;'>REQUIRED SKILLS</p>", unsafe_allow_html=True)
            req_html = "".join([f'<span class="badge-dark">{s}</span>' for s in selected_job.get('required_skills', [])])
            st.markdown(req_html, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    analyze_click = st.button("Run Skill Gap Analysis", type="primary", use_container_width=True)

    if analyze_click:
        if not extracted_skills:
            st.warning("Please select or upload a candidate profile with detectable skills.")
        else:
            with st.spinner("Analyzing competency matrix..."):
                analysis_result = calculate_skill_gap(
                    candidate_skills=extracted_skills,
                    job=selected_job,
                    resume_text=raw_text,
                    user_id=user_id or 101,
                    user_name=extracted_name
                )
                
                # Persist to database
                analysis_doc = {
                    "analysis_id": get_next_id("analyses", "analysis_id", base_start=9100),
                    "user_id": user_id or 101,
                    "user_name": extracted_name,
                    "job_id": selected_job["job_id"],
                    "job_title": selected_job["title"],
                    "company": selected_job["company"],
                    "matched_skills": analysis_result["matched_skills"],
                    "missing_skills": analysis_result["missing_skills"],
                    "match_score": analysis_result["match_score"],
                    "direct_skill_score": analysis_result["direct_skill_score"],
                    "semantic_score": analysis_result["semantic_score"],
                    "candidate_skills": extracted_skills,
                    "job_required_skills": selected_job.get("required_skills", []),
                    "status": "Evaluated",
                    "created_at": datetime.utcnow()
                }
                insert_analysis(analysis_doc)
                st.session_state["active_result"] = analysis_result
                st.session_state["active_doc"] = analysis_doc
                st.session_state["current_candidate_name"] = extracted_name
                st.session_state["current_candidate_skills"] = extracted_skills
                st.session_state["current_target_job"] = selected_job

    # Display Analysis Outcome
    if "active_result" in st.session_state:
        res = st.session_state["active_result"]
        st.markdown("---")
        st.markdown("#### Evaluation Results")

        res_col1, res_col2 = st.columns([1, 2], gap="large")

        with res_col1:
            st.markdown(f"""
            <div class="score-container">
                <div class="score-sub">COMPATIBILITY SCORE</div>
                <div class="score-number">{res['match_score']}%</div>
                <div style="font-size:0.8rem; color:#94A3B8;">
                    Direct Skill Fit: <b>{res['direct_skill_score']}%</b><br>
                    Semantic Similarity: <b>{res['semantic_score']}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with res_col2:
            st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#166534; text-transform:uppercase; margin-bottom:0.25rem;'>Matched Competencies</p>", unsafe_allow_html=True)
            if res["matched_skills"]:
                m_badges = "".join([f'<span class="badge-match">✓ {s}</span>' for s in res["matched_skills"]])
                st.markdown(m_badges, unsafe_allow_html=True)
            else:
                st.caption("No matching skills detected.")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#9F1239; text-transform:uppercase; margin-bottom:0.25rem;'>Identified Skill Gaps</p>", unsafe_allow_html=True)
            if res["missing_skills"]:
                g_badges = "".join([f'<span class="badge-gap">✕ {s}</span>' for s in res["missing_skills"]])
                st.markdown(g_badges, unsafe_allow_html=True)
            else:
                st.success("Candidate satisfies 100% of required competencies.")

        # Action Roadmap Section
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("##### Targeted Development Roadmap")
        if res["recommendations"]:
            for r in res["recommendations"]:
                p_class = f"priority-tag-{r['priority'].lower()}"
                st.markdown(f"""
                <div class="card-box-accent">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span style="font-weight:700; color:#0F172A; font-size:0.95rem;">{r['skill']}</span>
                        <span class="{p_class}">{r['priority']} Priority</span>
                    </div>
                    <div style="font-size:0.85rem; color:#334155; margin-bottom:0.3rem;">
                        <b>Recommended Course:</b> {r['course_title']} ({r['platform']}) &nbsp;•&nbsp; <b>Time:</b> ~{r['estimated_hours']} hrs
                    </div>
                    <div style="font-size:0.82rem; color:#64748B;">
                        <b>Curriculum:</b> {r['roadmap']}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: ATS BULLET POINT OPTIMIZER (RAG)
# =============================================================================
with tab_optimizer:
    st.markdown("##### 📝 ATS Resume Bullet Point Optimizer (RAG Engine)")
    st.caption("Transforms generic, passive resume statements into high-impact STAR framework achievements infused with target ATS keywords from MongoDB.")

    # Context setup
    c_name = st.session_state.get("current_candidate_name", "Candidate")
    c_skills = st.session_state.get("current_candidate_skills", ["Python", "SQL", "MongoDB"])
    t_job = st.session_state.get("current_target_job", {"title": "Data Analyst", "company": "ABC Technologies", "required_skills": ["Python", "SQL", "Power BI", "Excel", "Statistics"]})
    act_res = st.session_state.get("active_result", {"matched_skills": ["Python", "SQL"], "missing_skills": ["Power BI", "Excel", "Statistics"]})
    user_id = st.session_state.get("current_user_id", 101)

    with st.container(border=True):
        col_ctx1, col_ctx2 = st.columns([1, 1])
        with col_ctx1:
            st.markdown(f"**Target Role:** `{t_job['title']} @ {t_job['company']}`")
            st.markdown(f"**Target Keywords to Infuse:**")
            req_badges = "".join([f'<span class="badge-dark">{s}</span>' for s in t_job.get('required_skills', [])])
            st.markdown(req_badges, unsafe_allow_html=True)
        with col_ctx2:
            st.markdown(f"**Candidate:** `{c_name}`")
            st.markdown(f"**Identified Gaps:**")
            if act_res.get("missing_skills"):
                gap_badges = "".join([f'<span class="badge-gap">{s}</span>' for s in act_res['missing_skills']])
                st.markdown(gap_badges, unsafe_allow_html=True)
            else:
                st.caption("No critical gaps identified.")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col_in, col_tips = st.columns([3, 2], gap="large")

    with col_in:
        st.markdown("<p style='font-size:0.9rem; font-weight:600; color:#0F172A; margin-bottom:0.3rem;'>1. Resume Bullet Points to Optimize</p>", unsafe_allow_html=True)
        
        default_sample_bullets = (
            "Worked on air quality analysis with Python and Pandas to find pollution trends\n"
            "Built a library catalog microservice API using MongoDB document storage\n"
            "Wrote SQL queries to extract weekly customer purchase statistics"
        )

        c_bullets = st.session_state.get("current_candidate_bullets", [])
        if "raw_bullet_input" not in st.session_state:
            if c_bullets:
                st.session_state["raw_bullet_input"] = "\n".join(c_bullets)
            else:
                st.session_state["raw_bullet_input"] = default_sample_bullets

        col_src1, col_src2 = st.columns([1, 1])
        with col_src1:
            if st.button(f"📥 Load from Resume ({c_name})", use_container_width=True):
                if c_bullets:
                    st.session_state["raw_bullet_input"] = "\n".join(c_bullets)
                    st.success(f"Loaded {len(c_bullets)} statements from {c_name}'s resume!")
                    st.rerun()
                else:
                    st.info(f"No bullet lines detected from {c_name}'s resume yet. Paste lines below.")
        with col_src2:
            if st.button("✨ Load Sample Bullets", use_container_width=True):
                st.session_state["raw_bullet_input"] = default_sample_bullets
                st.rerun()

        bullet_input_text = st.text_area(
            "Bullet points to optimize:",
            value=st.session_state.get("raw_bullet_input", default_sample_bullets),
            height=130,
            label_visibility="collapsed",
            help="Enter 1 to 5 bullet points from your resume or projects, one on each line."
        )

        opt_btn = st.button("⚡ Transform into ATS-Optimized STAR Bullets", type="primary", use_container_width=True)

    with col_tips:
        st.markdown("<p style='font-size:0.9rem; font-weight:600; color:#0F172A; margin-bottom:0.3rem;'>💡 How the ATS Engine Optimizes</p>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("""
            - **STAR Method:** Converts passive duties (*"Responsible for..."*) into active results (*Situation, Task, Action, Result*).
            - **Power Action Verbs:** Starts every line with high-impact verbs (*Architected, Engineered, Streamlined, Orchestrated*).
            - **Quantifiable Metrics:** Adds realistic benchmarks (*35% turnaround, 99.8% uptime, 100K+ records*).
            - **Target Keyword Infusion:** Naturally embeds matching technical terms from MongoDB job requirements.
            """)

    if opt_btn:
        lines = [line.strip() for line in bullet_input_text.split("\n") if line.strip()]
        if not lines:
            st.warning("Please enter at least one bullet point to optimize.")
        else:
            with st.spinner("Retrieving role patterns from MongoDB & applying STAR optimization..."):
                optimized_results = optimize_resume_bullets_rag(
                    bullet_texts=lines,
                    job_title=t_job["title"],
                    job_company=t_job["company"],
                    job_skills=t_job.get("required_skills", []),
                    missing_skills=act_res.get("missing_skills", []),
                    candidate_skills=c_skills,
                    api_key=gemini_key_input
                )
                st.session_state["optimized_bullets"] = optimized_results
                st.session_state["raw_bullet_input"] = bullet_input_text

    if "optimized_bullets" in st.session_state:
        st.markdown("---")
        st.markdown("#### 🚀 ATS-Optimized Bullet Points (Before vs. After)")

        bullets_data = st.session_state["optimized_bullets"]
        
        # Summary KPI Banner
        avg_before = int(sum(b.get("score_before", 50) for b in bullets_data) / max(len(bullets_data), 1))
        avg_after = int(sum(b.get("score_after", 90) for b in bullets_data) / max(len(bullets_data), 1))
        all_infused = set()
        for b in bullets_data:
            all_infused.update(b.get("keywords_infused", []))

        k_col1, k_col2, k_col3 = st.columns(3)
        with k_col1:
            st.metric("Avg ATS Score Before", f"{avg_before}/100")
        with k_col2:
            st.metric("Avg ATS Score After", f"{avg_after}/100", delta=f"+{avg_after - avg_before} pts")
        with k_col3:
            st.metric("Total Keywords Infused", len(all_infused))

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        action_col1, action_col2 = st.columns([1, 1])
        with action_col1:
            if st.button("🔄 Replace Input Box With Optimized Text", use_container_width=True):
                st.session_state["raw_bullet_input"] = "\n".join([b["optimized"] for b in bullets_data])
                st.success("Input box updated with ATS-optimized STAR lines!")
                st.rerun()
        with action_col2:
            if st.button("💾 Save to Candidate Profile in MongoDB ($set)", use_container_width=True):
                try:
                    save_optimized_bullets(user_id=user_id or 101, optimized_bullets=bullets_data)
                    st.session_state["db_saved_candidate"] = c_name
                    st.success(f"Persisted {len(bullets_data)} optimized bullets to MongoDB collection 'users' for {c_name} using $set!")
                except Exception:
                    st.info("Demonstrated MongoDB $set update operator (saved in session profile).")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        for i, b in enumerate(bullets_data, 1):
            with st.container(border=True):
                top_c1, top_c2 = st.columns([3, 1])
                with top_c1:
                    st.markdown(f"**Bullet #{i}** &nbsp;•&nbsp; Action Verb: `<span class='badge-dark'>{b.get('action_verb', 'Engineered')}</span>`", unsafe_allow_html=True)
                with top_c2:
                    score_b = b.get('score_before', 50)
                    score_a = b.get('score_after', 92)
                    st.markdown(f"<div style='text-align:right;'><span style='color:#64748B;'>Score:</span> <b>{score_b}</b> ➔ <b style='color:#166534;'>{score_a}/100</b></div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div style='margin-top:0.4rem; margin-bottom:0.4rem;'>
                    <div style='font-size:0.8rem; font-weight:600; color:#DC2626; text-transform:uppercase;'>Original Passive Line:</div>
                    <div style='background:#FEF2F2; border-left:3px solid #EF4444; padding:0.45rem 0.75rem; border-radius:4px; font-size:0.88rem; color:#991B1B;'>
                        <s>{b.get('original')}</s>
                    </div>
                </div>
                <div style='margin-top:0.6rem; margin-bottom:0.4rem;'>
                    <div style='font-size:0.8rem; font-weight:600; color:#166534; text-transform:uppercase;'>ATS-Optimized Achievement (STAR Method):</div>
                    <div style='background:#F0FDF4; border-left:3px solid #22C55E; padding:0.55rem 0.75rem; border-radius:4px; font-size:0.92rem; color:#14532D; font-weight:500;'>
                        {b.get('optimized')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Keyword badges and rationale
                bot_c1, bot_c2 = st.columns([1, 1])
                with bot_c1:
                    if b.get("keywords_infused"):
                        k_badges = "".join([f'<span class="badge-neutral">{k}</span>' for k in b['keywords_infused']])
                        st.markdown(f"**Keywords Infused:** {k_badges}", unsafe_allow_html=True)
                with bot_c2:
                    st.markdown(f"<span style='font-size:0.8rem; color:#475569;'><b>Why:</b> {b.get('improvement_rationale', 'Enhanced with active voice and measurable metrics.')}</span>", unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.85rem; font-weight:600; color:#0F172A; margin-bottom:0.3rem;'>📋 Copy Ready-to-Paste Resume Bullets:</p>", unsafe_allow_html=True)
        export_text = "\n".join([f"• {b.get('optimized')}" for b in bullets_data])
        st.code(export_text, language="text")


# =============================================================================
# TAB 3: AI CAREER COPILOT (RAG)
# =============================================================================
with tab_copilot:
    st.markdown("##### ✦ AI Career Copilot & Q&A (RAG Engine)")
    st.caption("Retrieval-Augmented Generation: Answers are grounded by retrieving curriculum modules and job patterns from the MongoDB vector store.")

    # Context setup
    c_name = st.session_state.get("current_candidate_name", "Candidate")
    c_skills = st.session_state.get("current_candidate_skills", ["Python", "SQL", "MongoDB"])
    t_job = st.session_state.get("current_target_job", {"title": "Data Analyst", "company": "ABC Technologies", "required_skills": ["Python", "SQL", "Power BI", "Excel", "Statistics"]})
    act_res = st.session_state.get("active_result", {"matched_skills": ["Python", "SQL"], "missing_skills": ["Power BI", "Excel", "Statistics"]})

    with st.container(border=True):
        st.markdown(f"**Active Candidate:** `{c_name}` &nbsp;|&nbsp; **Target Role:** `{t_job['title']} @ {t_job['company']}`")
        st.markdown(f"**Identified Gaps:** `{', '.join(act_res['missing_skills']) if act_res['missing_skills'] else 'None'}`")

    # Quick prompt buttons
    st.markdown("<p style='font-size:0.85rem; font-weight:600; color:#475569; margin-top:0.75rem; margin-bottom:0.3rem;'>Suggested Questions:</p>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3 = st.columns(3)
    
    suggested_q = None
    if q_col1.button("How can I prepare for technical interviews for this role?"):
        suggested_q = "How can I prepare for technical interviews for this role given my specific skill gaps?"
    if q_col2.button("Generate a 3-week daily study schedule"):
        suggested_q = "Generate a structured 3-week daily study schedule focusing on my missing skills."
    if q_col3.button("How do I explain my missing skills to an interviewer?"):
        suggested_q = "How can I best articulate and explain my skill gaps during an interview without looking underqualified?"

    custom_query = st.text_input("Ask Career Copilot a question:", value=suggested_q or "", placeholder="e.g. What specific topics in Docker and AWS should I learn first?")

    if st.button("Generate Grounded Advice (RAG)", type="primary"):
        if not custom_query.strip():
            st.warning("Please enter a question or click one of the suggestions above.")
        else:
            with st.spinner("Retrieving MongoDB knowledge vectors and synthesizing response with Gemini..."):
                answer_text, retrieved_sources = ask_career_copilot(
                    candidate_name=c_name,
                    candidate_skills=c_skills,
                    job_title=t_job["title"],
                    job_company=t_job["company"],
                    job_required_skills=t_job.get("required_skills", []),
                    matched_skills=act_res.get("matched_skills", []),
                    missing_skills=act_res.get("missing_skills", []),
                    user_query=custom_query,
                    api_key=gemini_key_input
                )

                st.markdown("---")
                st.markdown("#### 💡 Copilot Response")
                st.markdown(answer_text)

                with st.expander("🔍 View Retrieved Knowledge Chunks (from MongoDB Vector Store)"):
                    for idx, src in enumerate(retrieved_sources, 1):
                        st.markdown(f"**{idx}. [{src['category'].upper()}] {src['title']}** (Relevance: `{src['score']}%`)")
                        st.caption(src["content"])


# =============================================================================
# TAB 3: PERSONALIZED PROJECT GENERATOR (RAG)
# =============================================================================
with tab_projects:
    st.markdown("##### 🛠️ Personalized Project Generator")
    st.caption("Generates resume-ready project architectures combining your existing strengths with your missing competencies to prove hands-on mastery.")

    c_skills = st.session_state.get("current_candidate_skills", ["Python", "SQL", "MongoDB"])
    t_job = st.session_state.get("current_target_job", {"title": "Cloud Data Engineer", "company": "DataNova Systems"})
    act_res = st.session_state.get("active_result", {"missing_skills": ["AWS", "Docker", "Apache Spark"]})

    with st.container(border=True):
        st.markdown(f"**Role:** `{t_job['title']} @ {t_job['company']}`")
        st.markdown(f"**Existing Strengths:** `{', '.join(c_skills)}` &nbsp;|&nbsp; **Skill Gaps to Bridge:** `{', '.join(act_res['missing_skills'])}`")

    if st.button("Generate 3 Custom Portfolio Projects", type="primary"):
        with st.spinner("Retrieving architecture templates from MongoDB and generating project specs..."):
            projects = generate_personalized_projects_rag(
                candidate_skills=c_skills,
                job_title=t_job["title"],
                job_company=t_job["company"],
                missing_skills=act_res.get("missing_skills", []),
                api_key=gemini_key_input
            )
            st.session_state["rag_projects"] = projects

    if "rag_projects" in st.session_state:
        st.markdown("---")
        st.markdown("#### 📐 Recommended Portfolio Projects")
        for idx, p in enumerate(st.session_state["rag_projects"], 1):
            with st.container(border=True):
                st.markdown(f"### Project {idx}: {p['title']}")
                st.markdown(f"*{p['description']}*")
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.markdown("**Skills Bridged:**")
                    p_bridged = "".join([f'<span class="badge-gap">{s}</span>' for s in p.get('skills_bridged', [])])
                    st.markdown(p_bridged, unsafe_allow_html=True)
                with col_p2:
                    st.markdown("**Strengths Leveraged:**")
                    p_used = "".join([f'<span class="badge-match">{s}</span>' for s in p.get('existing_skills_used', [])])
                    st.markdown(p_used, unsafe_allow_html=True)

                st.markdown(f"**Architecture Flow:** `{p.get('architecture_summary', 'Distributed Pipeline')}`")
                st.markdown("**Resume Bullet Point:**")
                st.code(p.get("resume_bullet", "Developed and launched project."), language="text")


# =============================================================================
# TAB 4: VECTOR SEARCH EXPLORER (MONGODB VECTOR STORE)
# =============================================================================
with tab_vector:
    st.markdown("##### 🧬 MongoDB Vector Search Explorer")
    st.caption("Demonstrates dense vector search over documents stored directly in MongoDB collection: `knowledge_vectors`.")

    col_vs1, col_vs2 = st.columns([3, 1])
    with col_vs1:
        v_query = st.text_input("Enter Semantic Search Query:", value="containerization and distributed big data pipelines")
    with col_vs2:
        v_category = st.selectbox("Category Filter:", ["All Categories", "job", "learning_roadmap", "project_pattern"])

    filter_cat = None if v_category == "All Categories" else v_category
    
    if st.button("Execute Vector Search in MongoDB", type="primary"):
        with st.spinner("Computing query embedding and calculating cosine similarity across MongoDB vectors..."):
            v_results = search_vector_knowledge_base(
                query=v_query,
                top_k=5,
                category=filter_cat,
                api_key=gemini_key_input
            )

            st.markdown("---")
            st.markdown(f"**Top Ranked Vector Matches in MongoDB (`knowledge_vectors`):**")
            for res in v_results:
                with st.container(border=True):
                    col_r1, col_r2 = st.columns([4, 1])
                    with col_r1:
                        st.markdown(f"**[{res['category'].upper()}] {res['title']}**")
                        st.markdown(f"<p style='font-size:0.85rem; color:#475569;'>{res['content']}</p>", unsafe_allow_html=True)
                        if res.get("skills"):
                            b_str = "".join([f'<span class="badge-neutral">{s}</span>' for s in res['skills']])
                            st.markdown(b_str, unsafe_allow_html=True)
                    with col_r2:
                        st.metric("Similarity", f"{res['score']}%")


# =============================================================================
# TAB 5: JOB OPENINGS
# =============================================================================
with tab_jobs:
    st.markdown("##### Job Openings & Requirements Directory")

    job_col_list, job_col_form = st.columns([3, 2], gap="large")

    with job_col_list:
        all_skills_names = [s["name"] for s in get_all_skills()]
        filter_skills = st.multiselect("Filter by skill requirements:", all_skills_names, default=["Python", "SQL"])
        match_mode = st.radio("Filter logic:", ["Require ANY of these ($in)", "Require ALL of these ($all)"], horizontal=True)

        use_all = "ALL" in match_mode
        jobs_filtered = find_jobs_by_skills(filter_skills, match_all=use_all) if filter_skills else get_all_jobs()

        st.caption(f"Showing **{len(jobs_filtered)}** job postings:")
        for j in jobs_filtered:
            with st.container(border=True):
                st.markdown(f"<span style='font-size:1.05rem; font-weight:700; color:#0F172A;'>{j['title']}</span> &nbsp;•&nbsp; <span style='color:#64748B;'>{j['company']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-size:0.82rem; color:#64748B;'>📍 {j.get('location', 'N/A')} &nbsp;|&nbsp; ⏳ {j.get('experience_years', 1)}+ yrs</span>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:0.85rem; color:#334155; margin-top:0.4rem;'>{j.get('description', '')}</p>", unsafe_allow_html=True)
                badges_str = "".join([f'<span class="badge-dark">{s}</span>' for s in j.get('required_skills', [])])
                st.markdown(badges_str, unsafe_allow_html=True)

    with job_col_form:
        st.markdown("<p style='font-size:0.95rem; font-weight:700; color:#0F172A; margin-bottom:0.5rem;'>Add Job Posting</p>", unsafe_allow_html=True)
        with st.form("new_job_posting_form"):
            j_title = st.text_input("Title*", "AI Platform Engineer")
            j_company = st.text_input("Company*", "Apex Global Systems")
            j_loc = st.text_input("Location", "Bengaluru (Hybrid)")
            j_exp = st.number_input("Experience (Years)", min_value=0, max_value=15, value=2)
            j_desc = st.text_area("Description", "Engineer scalable intelligence pipelines and APIs.")
            j_req = st.multiselect("Required Skills*", all_skills_names, default=["Python", "Docker", "FastAPI"])

            submit_job = st.form_submit_button("Save Job Posting", type="primary")
            if submit_job:
                if not j_title or not j_req:
                    st.error("Title and Required Skills are required.")
                else:
                    new_id = get_next_id("jobs", "job_id", base_start=510)
                    insert_job({
                        "job_id": new_id,
                        "title": j_title,
                        "company": j_company,
                        "location": j_loc,
                        "experience_years": int(j_exp),
                        "description": j_desc,
                        "required_skills": j_req,
                        "created_at": datetime.utcnow()
                    })
                    st.success(f"Job posting '{j_title}' created successfully.")
                    st.rerun()


# =============================================================================
# TAB 6: MARKET ANALYTICS
# =============================================================================
with tab_analytics:
    st.markdown("##### Talent Supply, Demand & Competency Intelligence")

    chart_c1, chart_c2 = st.columns(2, gap="medium")

    with chart_c1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Top In-Demand Skills</p>", unsafe_allow_html=True)
        demanded_skills, dem_pipe = get_most_demanded_job_skills(limit=8)
        if demanded_skills:
            df_dem = pd.DataFrame(demanded_skills)
            fig_dem = px.bar(
                df_dem,
                x="skill",
                y="demand_frequency",
                labels={"skill": "Skill", "demand_frequency": "Job Postings"},
                color_discrete_sequence=["#0F172A"]
            )
            fig_dem.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=290,
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(family="Inter", color="#0F172A")
            )
            st.plotly_chart(fig_dem, use_container_width=True)

        with st.expander("Aggregation Pipeline"):
            st.code(json.dumps(dem_pipe, indent=2), language="json")

    with chart_c2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Most Frequent Skill Gaps</p>", unsafe_allow_html=True)
        missing_skills, miss_pipe = get_most_common_missing_skills(limit=8)
        if missing_skills:
            df_miss = pd.DataFrame(missing_skills)
            fig_miss = px.bar(
                df_miss,
                x="skill",
                y="gap_count",
                labels={"skill": "Skill", "gap_count": "Candidate Gaps"},
                color_discrete_sequence=["#475569"]
            )
            fig_miss.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=290,
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(family="Inter", color="#0F172A")
            )
            st.plotly_chart(fig_miss, use_container_width=True)

        with st.expander("Aggregation Pipeline"):
            st.code(json.dumps(miss_pipe, indent=2), language="json")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    chart_c3, chart_c4 = st.columns(2, gap="medium")

    with chart_c3:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Market Demand vs Candidate Supply</p>", unsafe_allow_html=True)
        gap_info = get_candidate_supply_vs_demand()
        if gap_info:
            df_gap = pd.DataFrame(gap_info)
            fig_gap = go.Figure()
            fig_gap.add_trace(go.Bar(name='Employer Demand', x=df_gap['skill'], y=df_gap['demand'], marker_color='#0F172A'))
            fig_gap.add_trace(go.Bar(name='Candidate Supply', x=df_gap['skill'], y=df_gap['supply'], marker_color='#94A3B8'))
            fig_gap.update_layout(
                barmode='group',
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=290,
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                font=dict(family="Inter", color="#0F172A")
            )
            st.plotly_chart(fig_gap, use_container_width=True)

    with chart_c4:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Role Compatibility Leaderboard</p>", unsafe_allow_html=True)
        leaderboard, lb_pipe = get_job_performance_breakdown()
        if leaderboard:
            df_lb = pd.DataFrame(leaderboard)
            st.dataframe(
                df_lb[["job_title", "company", "avg_match_score", "highest_score", "total_evaluations"]],
                column_config={
                    "job_title": "Role",
                    "company": "Company",
                    "avg_match_score": st.column_config.ProgressColumn("Avg Match", format="%.1f%%", min_value=0, max_value=100),
                    "highest_score": "Top Score %",
                    "total_evaluations": "Evaluations"
                },
                hide_index=True,
                use_container_width=True
            )

        with st.expander("Aggregation Pipeline ($lookup join)"):
            st.code(json.dumps(lb_pipe, indent=2), language="json")


# =============================================================================
# TAB 7: DATA ENGINE & QUERY LAB
# =============================================================================
with tab_console:
    st.markdown("##### Data Engine & Query Console")
    st.caption("Demonstrate live database transactions, array operators, and pipeline executions.")

    sub1, sub2, sub3, sub4 = st.tabs([
        "Live CRUD Operations",
        "Pipeline Inspector",
        "Collection Browser",
        "Architecture & Viva Reference"
    ])

    with sub1:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Interactive CRUD Playground</p>", unsafe_allow_html=True)
        crud_selection = st.selectbox(
            "Select Database Operation:",
            [
                "insert_one() — Insert New Candidate",
                "find_one() — Query Document by ID",
                "update_one() with $addToSet — Add Skill (Deduplication)",
                "update_one() with $pull — Remove Skill",
                "delete_one() — Delete Document"
            ]
        )

        if "insert_one" in crud_selection:
            st.code("""
db.users.insert_one({
    "user_id": 999,
    "name": "Alex Mercer",
    "email": "alex@example.com",
    "skills": ["Python", "SQL", "Pandas"]
})
            """, language="python")
            if st.button("Execute insert_one()"):
                delete_user(999)
                ins_res = insert_user({
                    "user_id": 999,
                    "name": "Alex Mercer",
                    "email": "alex@example.com",
                    "skills": ["Python", "SQL", "Pandas"]
                })
                st.success(f"Record created! ID: {ins_res.inserted_id}")
                st.json(get_user_by_id(999))

        elif "find_one" in crud_selection:
            st.code("""user = db.users.find_one({"user_id": 101})""", language="python")
            u_query_id = st.number_input("Target user_id:", min_value=101, max_value=999, value=101)
            if st.button("Execute find_one()"):
                record = get_user_by_id(int(u_query_id))
                if record:
                    record["_id"] = str(record["_id"])
                    st.json(record)
                else:
                    st.warning("No record found with that ID.")

        elif "$addToSet" in crud_selection:
            st.code("""
# $addToSet inserts only if not already present
db.users.update_one(
    {"user_id": 101},
    {"$addToSet": {"skills": "Kubernetes"}}
)
            """, language="python")
            new_skill_in = st.text_input("Skill to Add:", "Kubernetes")
            if st.button("Execute $addToSet"):
                update_user_skills(101, new_skill_in)
                rec = get_user_by_id(101)
                st.success(f"Updated skills for User 101: {rec['skills']}")

        elif "$pull" in crud_selection:
            st.code("""
db.users.update_one(
    {"user_id": 101},
    {"$pull": {"skills": "Kubernetes"}}
)
            """, language="python")
            pull_skill_in = st.text_input("Skill to Remove:", "Kubernetes")
            if st.button("Execute $pull"):
                pull_skill_from_user(101, pull_skill_in)
                rec = get_user_by_id(101)
                st.success(f"Updated skills for User 101: {rec['skills']}")

        elif "delete_one" in crud_selection:
            st.code("""db.users.delete_one({"user_id": 999})""", language="python")
            del_id_in = st.number_input("User ID to delete:", min_value=100, max_value=999, value=999)
            if st.button("Execute delete_one()"):
                res_del = delete_user(int(del_id_in))
                st.info(f"Deleted records count: {res_del.deleted_count}")

    with sub2:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Aggregation Pipeline Runner</p>", unsafe_allow_html=True)
        pipeline_choice = st.selectbox(
            "Select Pipeline:",
            [
                "Most Demanded Skills ($unwind, $group, $sort)",
                "Most Common Missing Skills ($unwind, $group, $sort)",
                "Job Performance Leaderboard ($lookup)",
                "Score Range Bucketing ($bucket)"
            ]
        )

        if "Demanded" in pipeline_choice:
            data, p_def = get_most_demanded_job_skills(limit=10)
        elif "Missing" in pipeline_choice:
            data, p_def = get_most_common_missing_skills(limit=10)
        elif "Leaderboard" in pipeline_choice:
            data, p_def = get_job_performance_breakdown()
        else:
            data, p_def = get_score_distribution_aggregation()

        st.code(json.dumps(p_def, indent=2), language="json")
        st.dataframe(pd.DataFrame(data), use_container_width=True)

    with sub3:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Collection Browser</p>", unsafe_allow_html=True)
        coll_target = st.selectbox("Collection:", ["users", "jobs", "resumes", "analyses", "skills", "recommendations", "knowledge_vectors"])
        try:
            db = get_database()
            raw_docs = list(db[coll_target].find().limit(5))
            count_docs = db[coll_target].count_documents({})
            st.caption(f"Showing first 5 of {count_docs} documents from live MongoDB:")
            for d in raw_docs:
                d["_id"] = str(d["_id"])
                if "created_at" in d:
                    d["created_at"] = str(d["created_at"])
                if "uploaded_at" in d:
                    d["uploaded_at"] = str(d["uploaded_at"])
                if "embedding" in d and isinstance(d["embedding"], list):
                    d["embedding"] = f"[{len(d['embedding'])} dense vector dimensions]"
                st.json(d)
        except Exception:
            from database import seed_data
            sample_map = {
                "users": seed_data.USERS_DATA,
                "jobs": seed_data.JOBS_DATA,
                "resumes": seed_data.RESUMES_DATA,
                "analyses": seed_data.ANALYSES_DATA,
                "skills": seed_data.SKILLS_DATA,
                "recommendations": seed_data.RECOMMENDATIONS_DATA,
                "knowledge_vectors": [{"vector_id": 1, "title": "Sample Vector", "category": "learning_roadmap"}]
            }
            sample_docs = sample_map.get(coll_target, [])
            st.caption(f"Demo Mode: Showing {len(sample_docs[:5])} sample records for `{coll_target}` (Database offline):")
            for d in sample_docs[:5]:
                st.json(d)

    with sub4:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Viva & Technical Examination Reference</p>", unsafe_allow_html=True)
        with st.expander("How does RAG (Retrieval-Augmented Generation) work with MongoDB in this project?", expanded=True):
            st.markdown("""
            **RAG Architecture:**
            1. **Vector Embedding:** Document chunks (curriculum roadmaps, job descriptions, project architectures) are converted into dense vector embeddings.
            2. **MongoDB Vector Storage:** Stored in the `knowledge_vectors` collection alongside rich metadata.
            3. **Semantic Retrieval:** User queries compute embedding vectors and perform cosine similarity search against stored MongoDB vectors to retrieve the most relevant knowledge chunks.
            4. **Augmented Prompt:** Candidate profile, job requirements, and retrieved knowledge chunks are injected into Google Gemini LLM to generate grounded career advice and tailored portfolio projects.
            """)

        with st.expander("Why a document database instead of a relational database for this use case?"):
            st.markdown("""
            **Technical Justification:**
            1. **Natural Array Representation:** Candidate and job skills exist as multi-valued attributes (`["Python", "SQL"]`). Relational databases require separate bridge/junction tables with foreign keys, leading to expensive multi-table joins.
            2. **Embedded Complex Data & Vectors:** Resumes contain variable numbers of nested projects, certifications, and high-dimensional vector embeddings that fit hierarchical JSON/BSON documents cleanly without rigid schema migrations.
            3. **High-Performance Aggregations:** `$unwind` and `$group` provide native, in-memory pipeline transformations directly on array elements.
            """)

        with st.expander("What is the distinction between $push and $addToSet?"):
            st.markdown("""
            - **`$push`**: Always appends the provided item to the array, regardless of whether it already exists (can create duplicates).
            - **`$addToSet`**: Adds the item **only if it does not already exist** in the target array, enforcing set uniqueness.
            """)


# -----------------------------------------------------------------------------
# MINIMALIST FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.8rem; padding-bottom: 1rem;">
    Skill Gap Analyzer &nbsp;•&nbsp; RAG-Powered Competency Intelligence Platform
</div>
""", unsafe_allow_html=True)
