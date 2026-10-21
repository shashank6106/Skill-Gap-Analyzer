"""
Skill Gap Analyzer
Minimalist Light & Dark Enterprise Edition.
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
    insert_analysis, get_all_skills, get_next_id
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
    /* Global Typography & Spacing */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Clean Minimalist Header */
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
        display: flex;
        align-items: center;
        gap: 0.5rem;
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
        letter-spacing: 0.02em;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
    }

    /* Minimalist Stat Cards (Light and Dark combination) */
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

    /* Minimalist Skill Badges */
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

    /* Score Card Component */
    .score-container {
        background: #0F172A;
        color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
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

    /* Roadmap Item */
    .roadmap-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 3px solid #0F172A;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
    }
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
    .priority-tag-normal {
        background-color: #64748B;
        color: #FFFFFF;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Sidebar Clean Styling */
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
# SIDEBAR: MINIMALIST CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-title">SKILL GAP ANALYZER</div>
        <div class="sidebar-sub">Competency & Workforce Analytics</div>
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
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Local Database Connected</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Engine Offline: {conn_msg}")

    st.markdown("<p style='font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:0.5rem;'>Database Management</p>", unsafe_allow_html=True)
    if st.button("Reset / Reload Dataset", use_container_width=True):
        with st.spinner("Reloading dataset collections..."):
            seed_database(drop_existing=True)
            st.success("Dataset refreshed successfully.")
            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:0.5rem;'>System Specifications</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.8;">
        • Core: Python 3.14<br>
        • Database Driver: PyMongo<br>
        • Text Parsing: PyPDF v5<br>
        • Extraction: NLP Taxonomy<br>
        • Similarity: Scikit-Learn TF-IDF<br>
        • UI: Streamlit & Plotly
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
        <div class="app-tagline">Precision talent benchmarking, automated skill extraction, and personalized learning roadmaps</div>
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
tab_analysis, tab_jobs, tab_analytics, tab_console = st.tabs([
    "Skill Gap Analysis",
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

        elif profile_mode == "Select Existing Candidate":
            users = get_all_users()
            user_map = {f"{u['name']} (ID: {u['user_id']})": u for u in users}
            selected_u_label = st.selectbox("Select Candidate Record:", list(user_map.keys()))
            if selected_u_label:
                u_obj = user_map[selected_u_label]
                user_id = u_obj["user_id"]
                extracted_name = u_obj["name"]
                extracted_email = u_obj.get("email", "")
                extracted_skills = u_obj.get("skills", [])
                raw_text = f"Candidate {extracted_name}. Core skills: {', '.join(extracted_skills)}."

        else: # Upload PDF
            uploaded = st.file_uploader("Upload Resume Document (PDF)", type=["pdf"], label_visibility="collapsed")
            if uploaded is not None:
                parsed = parse_resume_content(uploaded.read(), filename=uploaded.name)
                raw_text = parsed["raw_text"]
                extracted_name = parsed["parsed_name"]
                extracted_email = parsed["email"]
                extracted_skills = extract_skills_from_text(raw_text)

        with st.container(border=True):
            st.markdown(f"**Name:** {extracted_name} &nbsp;|&nbsp; **Contact:** {extracted_email or 'Not specified'}")
            st.markdown("<p style='font-size:0.8rem; font-weight:600; color:#64748B; margin-top:0.5rem; margin-bottom:0.25rem;'>DETECTED SKILLS</p>", unsafe_allow_html=True)
            if extracted_skills:
                badges_html = "".join([f'<span class="badge-neutral">{s}</span>' for s in extracted_skills])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.caption("No skills extracted yet.")

    with col_target:
        st.markdown("<p style='font-size:0.9rem; font-weight:600; color:#0F172A; margin-bottom:0.4rem;'>2. Target Job Role</p>", unsafe_allow_html=True)
        jobs = get_all_jobs()
        job_map = {f"{j['title']} — {j['company']}": j for j in jobs}
        selected_job_key = st.selectbox("Select Target Opening:", list(job_map.keys()))
        selected_job = job_map[selected_job_key]

        with st.container(border=True):
            st.markdown(f"**Role:** {selected_job['title']}")
            st.markdown(f"**Company:** {selected_job['company']} &nbsp;|&nbsp; **Experience Required:** {selected_job.get('experience_years', 1)}+ years")
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
                <div class="roadmap-card">
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
        else:
            st.info("No gaps identified. Candidate is fully qualified for this position.")


# =============================================================================
# TAB 2: JOB OPENINGS
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
# TAB 3: MARKET ANALYTICS
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
# TAB 4: DATA ENGINE & QUERY LAB
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
        db = get_database()
        coll_target = st.selectbox("Collection:", ["users", "jobs", "resumes", "analyses", "skills", "recommendations"])
        raw_docs = list(db[coll_target].find().limit(5))
        st.caption(f"Showing first 5 of {db[coll_target].count_documents({})} documents:")
        for d in raw_docs:
            d["_id"] = str(d["_id"])
            if "created_at" in d:
                d["created_at"] = str(d["created_at"])
            if "uploaded_at" in d:
                d["uploaded_at"] = str(d["uploaded_at"])
            st.json(d)

    with sub4:
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A;'>Viva & Technical Examination Reference</p>", unsafe_allow_html=True)
        with st.expander("Why a document database instead of a relational database for this use case?", expanded=True):
            st.markdown("""
            **Technical Justification:**
            1. **Natural Array Representation:** Candidate and job skills exist as multi-valued attributes (`["Python", "SQL"]`). Relational databases require separate bridge/junction tables with foreign keys, leading to expensive multi-table joins.
            2. **Embedded Complex Data:** Resumes contain variable numbers of nested projects, certifications, and dynamic fields that fit hierarchical JSON/BSON documents cleanly without rigid schema migrations.
            3. **High-Performance Aggregations:** `$unwind` and `$group` provide native, in-memory pipeline transformations directly on array elements.
            """)

        with st.expander("What is the distinction between $push and $addToSet?"):
            st.markdown("""
            - **`$push`**: Always appends the provided item to the array, regardless of whether it already exists (can create duplicates).
            - **`$addToSet`**: Adds the item **only if it does not already exist** in the target array, enforcing set uniqueness.
            """)

        with st.expander("What role does $lookup perform in document architectures?"):
            st.markdown("""
            `$lookup` provides left-outer equality join capabilities between collections. In this project, it joins the `analyses` collection with the `jobs` collection on `job_id` to aggregate company information and compute role-level applicant fit metrics.
            """)


# -----------------------------------------------------------------------------
# MINIMALIST FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.8rem; padding-bottom: 1rem;">
    Skill Gap Analyzer &nbsp;•&nbsp; Talent Competency Benchmarking Platform
</div>
""", unsafe_allow_html=True)
