import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# COLOR PALETTE DEFINITION (Modern Tech Executive & Academic Theme)
# -----------------------------------------------------------------------------
BG_DARK = RGBColor(15, 23, 42)        # Slate 900 (Deep Navy Dark)
BG_CARD_DARK = RGBColor(30, 41, 59)   # Slate 800
BG_LIGHT = RGBColor(248, 250, 252)    # Slate 50 (Crisp Light Background)
CARD_BG = RGBColor(255, 255, 255)     # Pure White Card
CARD_BORDER = RGBColor(226, 232, 240) # Slate 200 Border
HEADER_BG = RGBColor(241, 245, 249)   # Slate 100

TEXT_DARK = RGBColor(15, 23, 42)      # Slate 900
TEXT_MUTED = RGBColor(100, 116, 139)  # Slate 500
TEXT_LIGHT = RGBColor(255, 255, 255)  # Pure White
TEXT_CYAN = RGBColor(56, 189, 248)    # Sky 400
TEXT_GREEN = RGBColor(52, 211, 153)   # Emerald 400

BRAND_PRIMARY = RGBColor(37, 99, 235) # Royal Blue 600
BRAND_TEAL = RGBColor(13, 148, 136)   # Teal 600
BRAND_CYAN = RGBColor(6, 182, 212)    # Cyan 500
BRAND_ORANGE = RGBColor(234, 88, 12)  # LPU University Orange 600
BRAND_GREEN = RGBColor(16, 185, 129)  # Emerald 500
BRAND_PURPLE = RGBColor(147, 51, 234) # Purple 600

CODE_BG = RGBColor(24, 32, 47)        # Dark monospaced code box
CODE_TEXT = RGBColor(226, 232, 240)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

def add_run_to_p(p, text, font_name=FONT_BODY, font_size=Pt(10), bold=False, color_rgb=None):
    r = p.add_run()
    r.text = text
    if font_name:
        r.font.name = font_name
    if font_size:
        r.font.size = font_size
    r.font.bold = bold
    if color_rgb:
        r.font.color.rgb = color_rgb
    return r

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen standard
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category="CSE494: INTELLIGENT NOSQL DATABASES", is_dark=False):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = FONT_HEADING
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEXT_CYAN if is_dark else BRAND_ORANGE

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.733), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_DARK

    def add_footer(slide, current_slide, total_slides=18, is_dark=False):
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(51, 65, 85) if is_dark else CARD_BORDER
        line.line.color.rgb = RGBColor(51, 65, 85) if is_dark else CARD_BORDER

        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(9.0), Inches(0.35))
        tf_foot = foot_box.text_frame
        tf_foot.word_wrap = True
        tf_foot.margin_left = tf_foot.margin_top = tf_foot.margin_right = tf_foot.margin_bottom = 0
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Gudla Shashank (12316224 | Roll 9 | K23DF) • Skill Gap Analyzer & Career Intelligence Platform • LPU"
        p_foot.font.name = FONT_BODY
        p_foot.font.size = Pt(9.5)
        p_foot.font.color.rgb = RGBColor(148, 163, 184) if is_dark else TEXT_MUTED

        num_box = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.033), Inches(0.35))
        tf_num = num_box.text_frame
        tf_num.word_wrap = True
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{current_slide} / {total_slides}"
        p_num.font.name = FONT_BODY
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = TEXT_CYAN if is_dark else BRAND_PRIMARY

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Deep Dark Executive Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.06))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = BRAND_ORANGE
    accent_bar.line.fill.background()

    uni_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.7))
    tf_u = uni_box.text_frame
    p_u1 = tf_u.paragraphs[0]
    p_u1.text = "LOVELY PROFESSIONAL UNIVERSITY  •  SCHOOL OF COMPUTER SCIENCE & ENGINEERING"
    p_u1.font.name = FONT_HEADING
    p_u1.font.size = Pt(11)
    p_u1.font.bold = True
    p_u1.font.color.rgb = RGBColor(251, 146, 60)

    p_u2 = tf_u.add_paragraph()
    p_u2.text = "INTELLIGENT NOSQL DATABASES (CSE494) — ACADEMIC TASK 2 PRESENTATION"
    p_u2.font.name = FONT_HEADING
    p_u2.font.size = Pt(10)
    p_u2.font.color.rgb = RGBColor(148, 163, 184)

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.5))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "Skill Gap Analyzer & Career Intelligence Platform"
    p_t1.font.name = FONT_HEADING
    p_t1.font.size = Pt(32)
    p_t1.font.bold = True
    p_t1.font.color.rgb = TEXT_LIGHT

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "A RAG-Driven Enterprise Competency Benchmarking System with MongoDB & Google Gemini"
    p_t2.font.name = FONT_HEADING
    p_t2.font.size = Pt(16)
    p_t2.font.color.rgb = TEXT_CYAN

    badges = [
        ("MongoDB Distributed Document & Vector Engine", BRAND_PRIMARY),
        ("Atomic Array Modifiers ($addToSet, $pull)", BRAND_TEAL),
        ("Gemini RAG Synthesis & Cosine Similarity", BRAND_PURPLE)
    ]
    for i, (b_text, b_color) in enumerate(badges):
        b_x = Inches(0.8 + i * 3.95)
        add_card(s1, b_x, Inches(3.6), Inches(3.8), Inches(0.5), bg_color=BG_CARD_DARK, border_color=b_color)
        b_box = s1.shapes.add_textbox(b_x, Inches(3.6), Inches(3.8), Inches(0.5))
        tf_b = b_box.text_frame
        tf_b.margin_top = Inches(0.1)
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        p_b.text = b_text
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(10.5)
        p_b.font.bold = True
        p_b.font.color.rgb = TEXT_LIGHT

    add_card(s1, Inches(0.8), Inches(4.5), Inches(5.7), Inches(2.1), bg_color=BG_CARD_DARK, border_color=RGBColor(51, 65, 85))
    tb_c1 = s1.shapes.add_textbox(Inches(1.0), Inches(4.6), Inches(5.3), Inches(1.9))
    tf_c1 = tb_c1.text_frame
    p1 = tf_c1.paragraphs[0]
    p1.text = "SUBMITTED BY"
    p1.font.bold = True
    p1.font.size = Pt(11)
    p1.font.color.rgb = TEXT_CYAN
    
    items_c1 = [
        ("Name:", "Gudla Shashank"),
        ("Registration No.:", "12316224"),
        ("Roll No. & Section:", "Roll No. 9  |  Section K23DF"),
        ("Degree Programme:", "B.Tech Computer Science & Engineering")
    ]
    for label, val in items_c1:
        p = tf_c1.add_paragraph()
        add_run_to_p(p, f"{label} ", bold=True, font_size=Pt(10.5), color_rgb=RGBColor(148, 163, 184))
        add_run_to_p(p, val, bold=True, font_size=Pt(10.5), color_rgb=TEXT_LIGHT)

    add_card(s1, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.1), bg_color=BG_CARD_DARK, border_color=RGBColor(51, 65, 85))
    tb_c2 = s1.shapes.add_textbox(Inches(7.0), Inches(4.6), Inches(5.3), Inches(1.9))
    tf_c2 = tb_c2.text_frame
    p2 = tf_c2.paragraphs[0]
    p2.text = "UNDER THE GUIDANCE OF"
    p2.font.bold = True
    p2.font.size = Pt(11)
    p2.font.color.rgb = RGBColor(251, 146, 60)

    items_c2 = [
        ("Supervisor:", "Shaik Sana Begum"),
        ("Designation:", "Assistant Professor"),
        ("Department:", "School of Computer Science & Engineering"),
        ("Institution:", "Lovely Professional University, Phagwara, Punjab")
    ]
    for label, val in items_c2:
        p = tf_c2.add_paragraph()
        add_run_to_p(p, f"{label} ", bold=True, font_size=Pt(10.5), color_rgb=RGBColor(148, 163, 184))
        add_run_to_p(p, val, bold=True, font_size=Pt(10.5), color_rgb=TEXT_LIGHT)

    set_speaker_notes(s1, 
        "Good morning / afternoon respected supervisor Shaik Sana Begum and evaluators. "
        "I am Gudla Shashank, Reg. No. 12316224 from B.Tech CSE, section K23DF. "
        "Today, I am proud to present my Academic Task 2 project for CSE494 Intelligent NoSQL Databases: "
        "'Skill Gap Analyzer & Career Intelligence Platform'. "
        "This project showcases high-performance MongoDB document data modeling, "
        "multikey indexing, multi-stage aggregation pipelines, and Retrieval-Augmented Generation (RAG) powered by Google Gemini."
    )

    # =========================================================================
    # SLIDE 2: PROJECT OVERVIEW & EXECUTIVE SUMMARY
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary & System Architecture Vision")
    add_footer(s2, 2)

    kpis = [
        ("7 Collections", "Zero Relational Joins", BRAND_PRIMARY),
        ("5 Aggregations", "$unwind, $group, $lookup", BRAND_TEAL),
        ("128-Dim Vectors", "RAG Cosine Knowledge Store", BRAND_PURPLE),
        ("< 10ms", "Indexed IXSCAN Latency", BRAND_GREEN)
    ]
    for i, (val, sub, col) in enumerate(kpis):
        x = Inches(0.8 + i * 2.98)
        add_card(s2, x, Inches(1.5), Inches(2.8), Inches(1.0), bg_color=HEADER_BG, border_color=col)
        tb = s2.shapes.add_textbox(x, Inches(1.55), Inches(2.8), Inches(0.9))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = val
        p.font.bold = True
        p.font.size = Pt(18)
        p.font.color.rgb = col
        p_sub = tf.add_paragraph()
        p_sub.alignment = PP_ALIGN.CENTER
        p_sub.text = sub
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = TEXT_MUTED

    add_card(s2, Inches(0.8), Inches(2.7), Inches(5.75), Inches(4.1))
    tb_left = s2.shapes.add_textbox(Inches(1.0), Inches(2.85), Inches(5.35), Inches(3.8))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Target Problem & Core Solution"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_PRIMARY

    bullets_l = [
        ("Bridging the Industry Gap:", "Engineering graduates often struggle to identify exact competency deficiencies required for modern software and data science roles."),
        ("Semi-Structured Ingestion:", "Extracts raw text and nested projects from PDF resumes directly into schema-flexible BSON documents."),
        ("Dual-Metric Scoring:", "Combines 70% exact taxonomy matching with 30% Scikit-Learn TF-IDF cosine similarity for realistic compatibility assessment."),
        ("Unified Storage & Intelligence:", "Unifies candidate demographics, job postings, transactional gap evaluations, and dense vector embeddings within a single MongoDB cluster.")
    ]
    for b_title, b_desc in bullets_l:
        p = tf_l.add_paragraph()
        p.space_before = Pt(8)
        add_run_to_p(p, f"• {b_title} ", bold=True, font_size=Pt(10.5), color_rgb=TEXT_DARK)
        add_run_to_p(p, b_desc, bold=False, font_size=Pt(10.5), color_rgb=TEXT_MUTED)

    add_card(s2, Inches(6.8), Inches(2.7), Inches(5.75), Inches(4.1))
    tb_right = s2.shapes.add_textbox(Inches(7.0), Inches(2.85), Inches(5.35), Inches(3.8))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Key Technological Pillars"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_TEAL

    bullets_r = [
        ("Atomic NoSQL Manipulation:", "Leverages $addToSet and $pull for set-level skill updates without relational junction tables or duplicate records."),
        ("Multi-Stage Pipeline Analytics:", "Runs 5 in-memory aggregation pipelines computing market demand, applicant tier distributions ($bucket), and cross-collection joins ($lookup)."),
        ("Embedded Knowledge Vectors:", "Stores 128-dimensional curriculum embeddings in MongoDB knowledge_vectors for fast point-lookup and vector similarity."),
        ("Actionable Generative AI (RAG):", "Instead of passive rejection emails, Google Gemini retrieves curriculum chunks from MongoDB to generate tailored 3-week roadmaps and project blueprints.")
    ]
    for b_title, b_desc in bullets_r:
        p = tf_r.add_paragraph()
        p.space_before = Pt(8)
        add_run_to_p(p, f"• {b_title} ", bold=True, font_size=Pt(10.5), color_rgb=TEXT_DARK)
        add_run_to_p(p, b_desc, bold=False, font_size=Pt(10.5), color_rgb=TEXT_MUTED)

    set_speaker_notes(s2,
        "In this executive summary, we outline why this platform was created. "
        "Traditional career platforms fail because they treat candidate competencies as static database columns. "
        "Our platform addresses this by leveraging MongoDB 7.0 as an intelligent document and vector store. "
        "We achieved 7 functional collections, sub-10ms response times with multikey indexing, "
        "and an integrated RAG copilot that turns skill gaps into concrete engineering projects."
    )

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & PROJECT OBJECTIVES
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Problem Statement & Core Project Objectives")
    add_footer(s3, 3)

    add_card(s3, Inches(0.8), Inches(1.5), Inches(5.75), Inches(5.3))
    tb_p = s3.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.35), Inches(4.9))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    p.text = "Limitations of Existing Relational ATS Platforms"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_ORANGE

    prob_items = [
        ("Crude ATS Keyword Matching:", "Existing Applicant Tracking Systems use naive exact-string matching, failing to capture semantic synonyms (e.g., PyTorch implies Deep Learning competence)."),
        ("Relational Schema Rigidity:", "SQL engines require destructive ALTER TABLE statements whenever emerging tech stacks (e.g., Vector DBs, LangChain, Kubernetes) are added."),
        ("Expensive Multi-Table Relational JOINs:", "Querying 20+ skills and embedded project histories requires 3-way table joins across candidates, skills, and junction tables, degrading read throughput."),
        ("Absence of Actionable Guidance:", "Job portals merely display a rejection or percentage score without providing guided architectural blueprints to bridge the deficit."),
        ("Vector Sprawl:", "Traditional architectures require external specialized vector databases (Pinecone, Milvus), creating dual-database synchronization headaches.")
    ]
    for p_title, p_desc in prob_items:
        p = tf_p.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, f"[!] {p_title} ", bold=True, font_size=Pt(9.5), color_rgb=RGBColor(185, 28, 28))
        add_run_to_p(p, p_desc, bold=False, font_size=Pt(9), color_rgb=TEXT_DARK)

    add_card(s3, Inches(6.8), Inches(1.5), Inches(5.75), Inches(5.3))
    tb_o = s3.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.35), Inches(4.9))
    tf_o = tb_o.text_frame
    tf_o.word_wrap = True
    p = tf_o.paragraphs[0]
    p.text = "Proposed System & Technical Objectives"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_GREEN

    obj_items = [
        ("Dynamic NoSQL Schema:", "Design a flexible MongoDB document model capable of storing semi-structured PDF resumes, user profiles, and dynamic skill arrays without schema migrations."),
        ("Atomic Array Modifiers:", "Implement atomic array updates using $addToSet, $push, and $pull to prevent duplicate entries and eliminate junction tables."),
        ("Multi-Stage Pipeline Analytics:", "Formulate 5 advanced MongoDB Aggregation pipelines ($unwind, $group, $lookup, $bucket, $project) to compute talent supply vs. demand in real-time."),
        ("Retrieval-Augmented Generation (RAG):", "Store 128-dimensional curriculum embeddings in MongoDB and retrieve top-K semantic chunks to ground Google Gemini 2.5 Flash responses."),
        ("Interactive Streamlit Telemetry:", "Build an executive web interface with live MongoDB CRUD simulators, explain('executionStats') query inspector, and visual market graphs.")
    ]
    for o_title, o_desc in obj_items:
        p = tf_o.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, f"[+] {o_title} ", bold=True, font_size=Pt(9.5), color_rgb=BRAND_GREEN)
        add_run_to_p(p, o_desc, bold=False, font_size=Pt(9), color_rgb=TEXT_DARK)

    set_speaker_notes(s3,
        "Here we articulate the core academic and technical problem. "
        "In a relational database, storing skills for candidates requires a junction table candidate_skills. "
        "Every time you want to inspect a candidate's profile and projects, you must execute multiple joins. "
        "Our project objectives for CSE494 directly solve this using MongoDB's document model, "
        "atomic array operations, and multi-stage aggregation pipelines."
    )

    # =========================================================================
    # SLIDE 4: WHY MONGODB? (SQL vs. NoSQL TECHNICAL COMPARISON)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Why MongoDB? Relational (SQL) vs. NoSQL Document Store")
    add_footer(s4, 4)

    rows = [
        ("Feature / Paradigm", "Relational Database (MySQL / PostgreSQL)", "MongoDB (Document Store) — OUR PLATFORM"),
        ("Data Structure", "Rigid tables, fixed column schemas, relational constraints", "Semi-structured BSON documents with dynamic, flexible fields"),
        ("Array of Skills", "Requires junction table (candidate_skills) + expensive JOINs", "Native BSON Array (e.g. \"skills\": [\"Python\", \"Docker\"])"),
        ("Nested Project History", "1-to-N normalized foreign key tables requiring joins", "Embedded subdocuments inside resumes collection"),
        ("Array Modification", "Multiple DELETE + INSERT statements with race conditions", "Atomic in-place modifiers: $addToSet, $push, $pull"),
        ("Vector Embeddings (RAG)", "Requires external vector DB (Pinecone/Milvus), data sprawl", "Stores float vectors directly inside knowledge_vectors"),
        ("Aggregation / Analytics", "Multi-table JOIN + GROUP BY; slow on text arrays", "Fast in-memory pipelines: $unwind, $group, $lookup, $bucket"),
        ("Query Performance", "Index scan degrades with multi-table joins", "Multikey B-Tree indexes on array fields (<2ms latency)")
    ]

    t_shape = s4.shapes.add_table(len(rows), 3, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    table = t_shape.table
    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(4.733)

    for r_idx, row in enumerate(rows):
        for c_idx, cell in enumerate(row):
            tc = table.cell(r_idx, c_idx)
            tc.text = cell
            p = tc.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5) if r_idx > 0 else Pt(10.5)
            
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT
                tc.fill.solid()
                tc.fill.fore_color.rgb = BRAND_PRIMARY if c_idx == 2 else BG_DARK
            else:
                tc.fill.solid()
                if c_idx == 0:
                    tc.fill.fore_color.rgb = HEADER_BG
                    p.font.bold = True
                    p.font.color.rgb = TEXT_DARK
                elif c_idx == 1:
                    tc.fill.fore_color.rgb = RGBColor(254, 242, 242) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
                    p.font.color.rgb = RGBColor(127, 29, 29)
                else:
                    tc.fill.fore_color.rgb = RGBColor(240, 253, 250) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
                    p.font.color.rgb = RGBColor(19, 78, 74)
                    p.font.bold = True

    set_speaker_notes(s4,
        "Professors frequently ask during viva: 'Why did you choose MongoDB over SQL for this project?' "
        "This slide gives the definitive answer. "
        "In SQL, modeling an array of skills requires an associative entity with foreign keys, leading to query complexity. "
        "In MongoDB, skills are stored as native BSON arrays. "
        "Furthermore, projects are embedded directly as subdocuments, and vector embeddings are stored inside documents, "
        "avoiding the complexity of managing a separate vector database."
    )

    # =========================================================================
    # SLIDE 5: SYSTEM ARCHITECTURE & END-TO-END PIPELINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "End-to-End System Architecture & Data Flow")
    add_footer(s5, 5)

    tiers = [
        ("1. Presentation Tier", "Streamlit Web UI", [
            "• Interactive Skill Gap Lab",
            "• Real-time PDF Upload & Parse",
            "• AI Copilot & Blueprint View",
            "• Plotly Executive Visualizations",
            "• MongoDB Query & CRUD Console"
        ], BRAND_PRIMARY),
        ("2. Application Driver", "PyMongo & Preprocessing", [
            "• Connection Pooling (50 sockets)",
            "• RFC 3986 URI Sanitizer",
            "• PyPDF Text Extractor",
            "• Scikit-Learn TF-IDF Matcher",
            "• Resilient Offline Fallback"
        ], BRAND_TEAL),
        ("3. Database Tier", "MongoDB 7.0 / Atlas", [
            "• 7 Specialized Collections",
            "• Multikey Array Indexing",
            "• Full-Text Search Indexes",
            "• 5 Aggregation Pipelines",
            "• Atomic Update Operators"
        ], BRAND_GREEN),
        ("4. AI & Vector Engine", "RAG & Google Gemini", [
            "• knowledge_vectors Collection",
            "• 128-Dim Vector Embeddings",
            "• Dot-Product / Cosine Similarity",
            "• Context Grounding Prompt",
            "• Gemini 2.5 Flash Synthesis"
        ], BRAND_PURPLE)
    ]

    for i, (t_title, t_sub, t_bullets, t_col) in enumerate(tiers):
        x = Inches(0.8 + i * 2.98)
        add_card(s5, x, Inches(1.5), Inches(2.8), Inches(3.7), bg_color=CARD_BG, border_color=t_col)
        
        add_card(s5, x, Inches(1.5), Inches(2.8), Inches(0.7), bg_color=t_col, border_color=None)
        tb_h = s5.shapes.add_textbox(x, Inches(1.5), Inches(2.8), Inches(0.7))
        tf_h = tb_h.text_frame
        p_h1 = tf_h.paragraphs[0]
        p_h1.alignment = PP_ALIGN.CENTER
        p_h1.text = t_title
        p_h1.font.bold = True
        p_h1.font.size = Pt(10.5)
        p_h1.font.color.rgb = TEXT_LIGHT
        p_h2 = tf_h.add_paragraph()
        p_h2.alignment = PP_ALIGN.CENTER
        p_h2.text = t_sub
        p_h2.font.size = Pt(9)
        p_h2.font.color.rgb = TEXT_LIGHT

        tb_b = s5.shapes.add_textbox(x + Inches(0.1), Inches(2.25), Inches(2.6), Inches(2.8))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for b_idx, bullet in enumerate(t_bullets):
            p = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p.space_before = Pt(4)
            p.text = bullet
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_DARK

    add_card(s5, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.4), bg_color=HEADER_BG, border_color=CARD_BORDER)
    tb_flow = s5.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.333), Inches(1.3))
    tf_flow = tb_flow.text_frame
    p_ft = tf_flow.paragraphs[0]
    p_ft.text = "Live Execution Flow (From Resume Upload to AI Blueprint Generation):"
    p_ft.font.bold = True
    p_ft.font.size = Pt(11)
    p_ft.font.color.rgb = BRAND_PRIMARY

    p_steps = tf_flow.add_paragraph()
    p_steps.space_before = Pt(3)
    steps_txt = (
        "[1. Upload PDF Resume] -> [2. PyPDF Extraction & Normalization] -> "
        "[3. Dual-Metric Gap Scoring (70% Skill + 30% TF-IDF)] -> "
        "[4. MongoDB Persistence (analyses collection)] -> "
        "[5. Vector Retrieval (knowledge_vectors Cosine Sim)] -> "
        "[6. Google Gemini Grounded Synthesis (3-Week Plan & Project)]"
    )
    p_steps.text = steps_txt
    p_steps.font.name = FONT_CODE
    p_steps.font.size = Pt(9.5)
    p_steps.font.bold = True
    p_steps.font.color.rgb = BRAND_TEAL

    set_speaker_notes(s5,
        "Here is the system architecture diagram. "
        "The architecture is divided into four clean tiers: "
        "1. Streamlit Presentation tier, 2. PyMongo application tier with URI sanitization and connection pooling, "
        "3. MongoDB Database tier with 7 collections, and 4. The AI intelligence tier combining TF-IDF and Gemini RAG. "
        "The bottom workflow illustrates the continuous pipeline from resume ingestion to grounded AI synthesis."
    )

    # =========================================================================
    # SLIDE 6: DATABASE & COLLECTION ARCHITECTURE (7 COLLECTIONS)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Database Architecture: 7 Functional Collections")
    add_footer(s6, 6)

    c_data = [
        ("Collection", "Type / Role", "Relationship Pattern", "Primary Key / Indexes", "Stored Entities & Purpose"),
        ("users", "Master Data", "Referenced by resumes & analyses", "user_id (Unique), email (Sparse)", "Candidate demographics, education, experience, skill string array"),
        ("resumes", "Semi-Structured", "1-to-1 Reference to users", "resume_id, skills (Multikey)", "Parsed resume text, extracted skills, embedded projects array"),
        ("jobs", "Master Catalog", "Referenced by analyses", "job_id (Unique), required_skills (Multikey)", "Job openings, roles, minimum salary, text index on title/company"),
        ("skills", "Canonical Catalog", "Referenced by name", "skill_id (Unique), name (Unique)", "30+ standardized tech skills categorized by discipline"),
        ("analyses", "Transactional Log", "References users & jobs", "analysis_id, match_score", "Historical gap evaluations, matched skills, missing skills, scores"),
        ("recommendations", "Knowledge Base", "Keyed on skill name", "rec_id, skill_name", "Targeted courses, duration, learning platforms, priority tiers"),
        ("knowledge_vectors", "Dense Vector Store", "Stand-alone Knowledge Bank", "doc_id (Unique), category", "Curriculum chunks + 128-dim dense embeddings for RAG retrieval")
    ]

    t6_shape = s6.shapes.add_table(len(c_data), 5, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.3))
    t6 = t6_shape.table
    t6.columns[0].width = Inches(1.8)
    t6.columns[1].width = Inches(1.6)
    t6.columns[2].width = Inches(2.2)
    t6.columns[3].width = Inches(2.3)
    t6.columns[4].width = Inches(3.833)

    for r_idx, row in enumerate(c_data):
        for c_idx, cell in enumerate(row):
            tc = t6.cell(r_idx, c_idx)
            tc.text = cell
            p = tc.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5) if r_idx > 0 else Pt(9.5)
            
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT
                tc.fill.solid()
                tc.fill.fore_color.rgb = BRAND_PRIMARY
            else:
                tc.fill.solid()
                if c_idx == 0:
                    tc.fill.fore_color.rgb = HEADER_BG
                    p.font.bold = True
                    p.font.color.rgb = BRAND_PRIMARY
                else:
                    tc.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_idx % 2 == 0 else RGBColor(248, 250, 252)
                    p.font.color.rgb = TEXT_DARK

    add_card(s6, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.9), bg_color=RGBColor(240, 253, 250), border_color=BRAND_TEAL)
    tb_des = s6.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.333), Inches(0.8))
    tf_des = tb_des.text_frame
    p_dh = tf_des.paragraphs[0]
    p_dh.text = "Architectural Decision: Embedding vs. Referencing Strategy"
    p_dh.font.bold = True
    p_dh.font.size = Pt(10.5)
    p_dh.font.color.rgb = BRAND_TEAL

    p_db = tf_des.add_paragraph()
    p_db.text = (
        "• EMBEDDING: Projects are embedded inside resumes because they are always loaded together and have a bounded 1-to-few relationship.\n"
        "• REFERENCING: jobs and users are referenced via integer IDs inside analyses to avoid duplicating large job specs across thousands of evaluations."
    )
    p_db.font.size = Pt(9)
    p_db.font.color.rgb = TEXT_DARK

    set_speaker_notes(s6,
        "Here are our 7 collections in MongoDB. Notice how each collection serves a specific role. "
        "Explain to the examiner that we made very conscious data modeling choices: "
        "we embedded project arrays inside resumes because projects are bounded and accessed with resumes, "
        "while referencing users and jobs from analyses to maintain 16MB document safety and avoid data redundancy."
    )

    # =========================================================================
    # SLIDE 7: DOCUMENT DATA MODELING & SCHEMA DESIGN
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Document Data Modeling: BSON Schemas & Design Patterns")
    add_footer(s7, 7)

    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.75), Inches(5.3), bg_color=CODE_BG, border_color=None)
    tb_code1 = s7.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.35), Inches(5.1))
    tf_c1 = tb_code1.text_frame
    tf_c1.word_wrap = True
    
    p = tf_c1.paragraphs[0]
    p.text = "// Document in 'users' collection (Native Array)"
    p.font.name = FONT_CODE
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_CYAN

    code_u = (
        "{\n"
        '  "_id": ObjectId("65342a1ef82d9a10bc931001"),\n'
        '  "user_id": 101,\n'
        '  "name": "Shashank Verma",\n'
        '  "email": "shashank.verma@example.com",\n'
        '  "experience_years": 2,\n'
        '  "skills": ["Python", "SQL", "Pandas", "Scikit-Learn"],\n'
        '  "created_at": ISODate("2026-10-21T10:00:00Z")\n'
        "}\n\n"
        "// Document in 'resumes' collection (Embedded Subdocuments)\n"
        "{\n"
        '  "resume_id": 301,\n'
        '  "user_id": 101,\n'
        '  "filename": "shashank_resume.pdf",\n'
        '  "projects": [\n'
        "    {\n"
        '      "name": "Customer Churn Predictor",\n'
        '      "tools": ["Python", "Scikit-Learn", "Pandas"],\n'
        '      "description": "Random Forest pipeline with 89% recall."\n'
        "    }\n"
        "  ]\n"
        "}"
    )
    p2 = tf_c1.add_paragraph()
    p2.text = code_u
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8)
    p2.font.color.rgb = CODE_TEXT

    add_card(s7, Inches(6.8), Inches(1.5), Inches(5.75), Inches(5.3))
    tb_pat = s7.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.35), Inches(4.9))
    tf_pat = tb_pat.text_frame
    tf_pat.word_wrap = True
    
    p = tf_pat.paragraphs[0]
    p.text = "MongoDB Design Patterns Applied"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_PRIMARY

    patterns = [
        ("Attribute Pattern (Skills Array):", "Modeling candidate and job skills as homogeneous BSON string arrays allows efficient Multikey B-Tree indexing without intermediate tables."),
        ("Subset Pattern (Project Highlights):", "Resumes embed only the most relevant recent projects (top 3-5), preventing unbounded document growth and guaranteeing fast document serialization."),
        ("Log / Event Sourcing Pattern (Analyses):", "Evaluations are stored as immutable point-in-time documents in analyses with timestamps, supporting longitudinal candidate progress tracking."),
        ("Schema Flexibility in Practice:", "Different candidates can possess completely distinct project properties (e.g. GitHub URL, live demo link, team size) without requiring ALTER TABLE modifications."),
        ("BSON Vector Document Pattern:", "The knowledge_vectors collection stores dense 128-float arrays directly in each curriculum chunk, allowing single-query document + vector retrieval.")
    ]
    for pat_title, pat_desc in patterns:
        p = tf_pat.add_paragraph()
        p.space_before = Pt(8)
        add_run_to_p(p, f"• {pat_title} ", bold=True, font_size=Pt(10), color_rgb=TEXT_DARK)
        add_run_to_p(p, pat_desc, bold=False, font_size=Pt(9.5), color_rgb=TEXT_MUTED)

    set_speaker_notes(s7,
        "Here we show the actual BSON document structure. "
        "Highlight to the examiner that we implemented established MongoDB design patterns: "
        "The Attribute Pattern for skill arrays, the Subset Pattern for projects inside resumes, "
        "and the Event Sourcing Pattern for analysis evaluation logs. "
        "This adheres directly to MongoDB official data modeling best practices."
    )

    # =========================================================================
    # SLIDE 8: CORE MONGODB IMPLEMENTATION — CRUD OPERATIONS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "MongoDB CRUD Implementation & Atomic Array Modifiers")
    add_footer(s8, 8)

    crud_ops = [
        ("CREATE (Insert Operations)", BRAND_PRIMARY, [
            "# Single document insertion",
            "db.users.insert_one({",
            '  "user_id": 107, "name": "Priya",',
            '  "skills": ["Python", "FastAPI"]',
            "})",
            "",
            "# Bulk insertion for jobs",
            "db.jobs.insert_many(",
            "  JOBS_DATA, ordered=False",
            ")"
        ]),
        ("READ (Query & Array Match)", BRAND_TEAL, [
            "# Exact Primary Key lookup",
            'db.users.find_one({"user_id": 101})',
            "",
            "# Multikey Array matching ($all)",
            "db.jobs.find({",
            '  "required_skills": {',
            '    "$all": ["Python", "Docker"]',
            "  }",
            "})"
        ]),
        ("UPDATE (Atomic Array Modifiers)", BRAND_ORANGE, [
            "# Deduplicated array append ($addToSet)",
            'db.users.update_one({"user_id": 101},',
            '  {"$addToSet": {"skills": "Docker"}}',
            ")",
            "",
            "# Atomic element removal ($pull)",
            'db.users.update_one({"user_id": 101},',
            '  {"$pull": {"skills": "Pandas"}}',
            ")"
        ]),
        ("DELETE & RESET", RGBColor(220, 38, 38), [
            "# Single document deletion",
            'db.users.delete_one({"user_id": 101})',
            "",
            "# Clean collection purge",
            "db.analyses.delete_many({})",
            "",
            "# Execution acknowledgment verified",
            "assert res.acknowledged == True"
        ])
    ]

    for i, (title, color, code_lines) in enumerate(crud_ops):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(1.5 + (i // 2) * 2.7)
        add_card(s8, x, y, Inches(5.75), Inches(2.5), bg_color=CARD_BG, border_color=color)
        
        add_card(s8, x, y, Inches(5.75), Inches(0.45), bg_color=color, border_color=None)
        tb_h = s8.shapes.add_textbox(x, y, Inches(5.75), Inches(0.45))
        tf_h = tb_h.text_frame
        p = tf_h.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = title
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT

        tb_c = s8.shapes.add_textbox(x + Inches(0.15), y + Inches(0.5), Inches(5.45), Inches(1.9))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        for line_idx, line in enumerate(code_lines):
            p = tf_c.paragraphs[0] if line_idx == 0 else tf_c.add_paragraph()
            p.text = line
            p.font.name = FONT_CODE
            p.font.size = Pt(8.5)
            if line.startswith("#"):
                p.font.color.rgb = TEXT_MUTED
                p.font.bold = True
            elif "$" in line:
                p.font.color.rgb = BRAND_PRIMARY
                p.font.bold = True
            else:
                p.font.color.rgb = TEXT_DARK

    set_speaker_notes(s8,
        "Examiners always test candidate understanding of array operations. "
        "Point out $addToSet: if a user clicks 'Add Skill: Docker', $addToSet checks if 'Docker' exists in the array; "
        "if already present, it makes no changes, returning modified_count: 0. "
        "This guarantees mathematical set semantics at the database engine level without needing application loops. "
        "Similarly, $pull removes items atomically in one database trip."
    )

    # =========================================================================
    # SLIDE 9: INDEXING STRATEGY & QUERY OPTIMIZATION (explain())
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Indexing Strategy & Performance Analysis (explain())")
    add_footer(s9, 9)

    add_card(s9, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.3))
    tb_it = s9.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.6), Inches(4.9))
    tf_it = tb_it.text_frame
    tf_it.word_wrap = True
    p = tf_it.paragraphs[0]
    p.text = "Implemented MongoDB Indexes"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_PRIMARY

    idx_items = [
        ("users.user_id", "Unique Single-Field", "Guarantees primary candidate uniqueness; point lookups in <2ms."),
        ("users.email", "Unique Sparse Index", "Enforces email uniqueness while permitting documents without an email field."),
        ("resumes.skills", "Multikey B-Tree Index", "Indexes each individual string in the skills array for rapid subset matching."),
        ("jobs.required_skills", "Multikey B-Tree Index", "Accelerates array queries evaluating required competencies using $all."),
        ("jobs.title & company", "Full-Text Index", "Enables text score sorting and keyword queries ($text: {$search: 'ML'})."),
        ("knowledge_vectors.doc_id", "Unique Index", "Powers O(1) point retrieval of RAG curriculum documents.")
    ]
    for idx_name, idx_type, idx_purpose in idx_items:
        p = tf_it.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, f"• {idx_name} ", bold=True, font_size=Pt(9.5), color_rgb=BRAND_PRIMARY)
        add_run_to_p(p, f"[{idx_type}]: ", bold=True, font_size=Pt(9), color_rgb=BRAND_TEAL)
        add_run_to_p(p, idx_purpose, bold=False, font_size=Pt(9), color_rgb=TEXT_MUTED)

    add_card(s9, Inches(7.0), Inches(1.5), Inches(5.533), Inches(5.3), bg_color=CARD_BG, border_color=BRAND_ORANGE)
    tb_exp = s9.shapes.add_textbox(Inches(7.2), Inches(1.65), Inches(5.133), Inches(4.9))
    tf_exp = tb_exp.text_frame
    tf_exp.word_wrap = True
    p = tf_exp.paragraphs[0]
    p.text = "Execution Plan: COLLSCAN vs. IXSCAN"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_ORANGE

    p = tf_exp.add_paragraph()
    p.space_before = Pt(6)
    p.text = "Analysis via explain('executionStats'):"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DARK

    p_code = tf_exp.add_paragraph()
    p_code.space_before = Pt(4)
    p_code.text = (
        "// UNINDEXED SCAN (Without index):\n"
        'stage: "COLLSCAN"\n'
        "totalDocsExamined: N (Evaluates all documents)\n"
        "executionTimeMillis: ~35 ms\n"
        "Complexity: O(N) Linear Collection Scan\n\n"
        "// INDEXED SCAN (With uniq_user_id):\n"
        'stage: "IXSCAN" -> "FETCH"\n'
        "indexName: 'uniq_user_id'\n"
        "totalDocsExamined: 1\n"
        "nReturned: 1\n"
        "executionTimeMillis: < 1 ms\n"
        "Complexity: O(log N) B-Tree Traversal"
    )
    p_code.font.name = FONT_CODE
    p_code.font.size = Pt(8.5)
    p_code.font.color.rgb = BRAND_PRIMARY

    p_conc = tf_exp.add_paragraph()
    p_conc.space_before = Pt(6)
    p_conc.text = "Impact: Reduced query evaluation time by 97.1%, eliminating disk-thrashing collection scans under high concurrency."
    p_conc.font.bold = True
    p_conc.font.size = Pt(9.5)
    p_conc.font.color.rgb = BRAND_GREEN

    set_speaker_notes(s9,
        "Query optimization is a critical topic in CSE494. "
        "Here we show our indexing strategy, specifically highlighting Multikey Indexes on array fields. "
        "When explaining query execution stats: an unindexed query triggers a COLLSCAN, examining all documents in O(N) time. "
        "With our unique and multikey indexes, MongoDB traverses an efficient B-Tree index structure via IXSCAN, "
        "examining exactly 1 document in logarithmic time, completing in under 1 millisecond."
    )

    # =========================================================================
    # SLIDE 10: ADVANCED MONGODB AGGREGATION FRAMEWORK (5 PIPELINES)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Advanced MongoDB Aggregation Framework (5 Pipelines)")
    add_footer(s10, 10)

    pipelines = [
        ("Pipeline Name", "Input Collection", "Pipeline Stages Executed", "Key Operators", "Business / Analytical Value"),
        ("1. Top Matched Skills", "resumes", "$unwind -> $group -> $sort -> $limit -> $project", "$sum, $unwind", "Ranks technical competencies most prevalent across candidate profiles"),
        ("2. Common Skill Gaps", "analyses", "$unwind -> $group -> $sort -> $limit -> $project", "$sum, $sort: -1", "Identifies the highest-frequency missing skills across all evaluations"),
        ("3. Job Market Demand", "jobs", "$unwind -> $group -> $sort -> $limit -> $project", "$sum, $limit: 10", "Determines top industry skills required across current employer job postings"),
        ("4. Job Performance Join", "analyses + jobs", "$lookup -> $unwind -> $group -> $sort -> $project", "$lookup, $avg, $round", "Joins analyses with jobs to calculate candidate volume & average score per role"),
        ("5. Score Bucketing", "analyses", "$bucket (boundaries: [0, 40, 60, 80, 101])", "$bucket, $avg, $sum", "Categorizes candidate scores into 4 tiers: Low, Moderate, High, Exceptional")
    ]

    t10_shape = s10.shapes.add_table(len(pipelines), 5, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.0))
    t10 = t10_shape.table
    t10.columns[0].width = Inches(2.2)
    t10.columns[1].width = Inches(1.6)
    t10.columns[2].width = Inches(3.2)
    t10.columns[3].width = Inches(1.8)
    t10.columns[4].width = Inches(2.933)

    for r_idx, row in enumerate(pipelines):
        for c_idx, cell in enumerate(row):
            tc = t10.cell(r_idx, c_idx)
            tc.text = cell
            p = tc.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5) if r_idx > 0 else Pt(9.5)
            
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT
                tc.fill.solid()
                tc.fill.fore_color.rgb = BRAND_PRIMARY
            else:
                tc.fill.solid()
                if c_idx == 0:
                    tc.fill.fore_color.rgb = HEADER_BG
                    p.font.bold = True
                    p.font.color.rgb = BRAND_PRIMARY
                else:
                    tc.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_idx % 2 == 0 else RGBColor(248, 250, 252)
                    p.font.color.rgb = TEXT_DARK

    add_card(s10, Inches(0.8), Inches(5.65), Inches(11.733), Inches(1.2), bg_color=HEADER_BG, border_color=BRAND_TEAL)
    tb_agg = s10.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.333), Inches(1.1))
    tf_agg = tb_agg.text_frame
    p = tf_agg.paragraphs[0]
    p.text = "Why MongoDB Aggregations Outperform Application-Level Python Loops:"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = BRAND_TEAL

    p_body = tf_agg.add_paragraph()
    p_body.text = (
        "• Native C++ Engine Execution: All unwinding, grouping, and averaging execute inside the MongoDB database engine in native C++.\n"
        "• Network Bandwidth Conservation: Instead of sending 10,000 documents over TCP for Python processing, only the compact 10-line aggregated result is transmitted.\n"
        "• Pipeline Memory Limit Handling: Operates well within MongoDB's 100MB RAM stage limit with selective indexing."
    )
    p_body.font.size = Pt(9)
    p_body.font.color.rgb = TEXT_DARK

    set_speaker_notes(s10,
        "Here are the five aggregation pipelines implemented in database/aggregations.py. "
        "Emphasize to the professor that these pipelines execute in native C++ inside the MongoDB engine. "
        "Instead of fetching 10,000 resume documents over the network and running slow Python for-loops, "
        "MongoDB's aggregation framework calculates talent supply and demand in-place, returning only the summary to the client."
    )

    # =========================================================================
    # SLIDE 11: DEEP DIVE: CROSS-COLLECTION FOREIGN JOIN ($lookup)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Deep Dive: Cross-Collection Foreign Join ($lookup)")
    add_footer(s11, 11)

    add_card(s11, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.3), bg_color=CODE_BG, border_color=None)
    tb_lcode = s11.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.6), Inches(5.1))
    tf_lc = tb_lcode.text_frame
    tf_lc.word_wrap = True
    
    p = tf_lc.paragraphs[0]
    p.text = "# database/aggregations.py (Pipeline 4: $lookup Join)"
    p.font.name = FONT_CODE
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_CYAN

    code_lookup = (
        "pipeline = [\n"
        "  {\n"
        '    "$lookup": {\n'
        '      "from": "jobs",\n'
        '      "localField": "job_id",\n'
        '      "foreignField": "job_id",\n'
        '      "as": "job_details"\n'
        "    }\n"
        "  },\n"
        '  {"$unwind": "$job_details"},\n'
        "  {\n"
        '    "$group": {\n'
        '      "_id": "$job_id",\n'
        '      "job_title": {"$first": "$job_details.title"},\n'
        '      "company": {"$first": "$job_details.company"},\n'
        '      "avg_score": {"$avg": "$match_score"},\n'
        '      "total_candidates": {"$sum": 1}\n'
        "    }\n"
        "  },\n"
        '  {"$sort": {"avg_score": -1}},\n'
        "  {\n"
        '    "$project": {\n'
        '      "_id": 0, "job_id": "$_id",\n'
        '      "job_title": 1, "company": 1,\n'
        '      "avg_score": {"$round": ["$avg_score", 1]},\n'
        '      "total_candidates": 1\n'
        "    }\n"
        "  }\n"
        "]"
    )
    p2 = tf_lc.add_paragraph()
    p2.text = code_lookup
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8)
    p2.font.color.rgb = CODE_TEXT

    add_card(s11, Inches(7.0), Inches(1.5), Inches(5.533), Inches(5.3))
    tb_stages = s11.shapes.add_textbox(Inches(7.2), Inches(1.65), Inches(5.133), Inches(4.9))
    tf_st = tb_stages.text_frame
    tf_st.word_wrap = True
    
    p = tf_st.paragraphs[0]
    p.text = "Stage-by-Stage Join Mechanics"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_PRIMARY

    stage_items = [
        ("1. $lookup Stage (Left Outer Join):", "Correlates documents in analyses with matching job_id documents in the jobs collection, creating a nested array job_details."),
        ("2. $unwind Stage (Array Flattening):", "Flattens the single-element job_details array into top-level document fields so scalar operators can access title and company."),
        ("3. $group Stage (Multi-Metric Aggregation):", "Groups documents by target job ID. Calculates $avg match score, $sum total evaluations, and retains company metadata using $first."),
        ("4. $sort Stage (Ranking):", "Sorts the aggregated job roles in descending order of average score (avg_score: -1)."),
        ("5. $project & $round Stage (Data Shaping):", "Shapes the final output document, suppressing _id and applying $round to limit floating-point averages to 1 decimal place.")
    ]
    for st_title, st_desc in stage_items:
        p = tf_st.add_paragraph()
        p.space_before = Pt(7)
        add_run_to_p(p, f"• {st_title} ", bold=True, font_size=Pt(9.5), color_rgb=BRAND_PRIMARY)
        add_run_to_p(p, st_desc, bold=False, font_size=Pt(9), color_rgb=TEXT_MUTED)

    set_speaker_notes(s11,
        "Examiners love to ask about $lookup: 'Can MongoDB perform joins like SQL?' "
        "The answer is YES, via the $lookup aggregation stage. "
        "In our project, analyses stores evaluations, but doesn't store the full job title or company name. "
        "Our $lookup stage joins with the jobs collection on job_id, unwinds the array, "
        "and aggregates the average candidate performance per job posting without having to duplicate data."
    )

    # =========================================================================
    # SLIDE 12: RETRIEVAL-AUGMENTED GENERATION (RAG) WITH MONGODB & GEMINI
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "RAG Architecture: MongoDB Vector Store + Google Gemini")
    add_footer(s12, 12)

    rag_steps = [
        ("Step 1: RETRIEVE", "MongoDB Vector Store", [
            "• Collection: knowledge_vectors",
            "• Dense 128-dim float embeddings",
            "• Candidate gap skills converted to query vector",
            "• Computes Cosine Similarity against stored curriculum chunks",
            "• Top-K relevant docs fetched"
        ], BRAND_PRIMARY),
        ("Step 2: AUGMENT", "Contextual Prompt Assembly", [
            "• Candidate Profile (skills, exp)",
            "• Employer Job Spec & gaps",
            "• Retrieved MongoDB Curriculum & Project Architectures",
            "• Injected into strictly structured system prompt",
            "• Eliminates LLM hallucination"
        ], BRAND_TEAL),
        ("Step 3: GENERATE", "Google Gemini 2.5 Flash", [
            "• Synthesizes 3-Week Study Plan",
            "• Week-by-week hourly milestones",
            "• Production-grade Project Blueprint",
            "• Recommended tech stack & DB schema",
            "• Resume-ready bullet points"
        ], BRAND_PURPLE)
    ]

    for i, (r_title, r_sub, r_bullets, r_col) in enumerate(rag_steps):
        x = Inches(0.8 + i * 3.98)
        add_card(s12, x, Inches(1.5), Inches(3.8), Inches(3.8), bg_color=CARD_BG, border_color=r_col)
        
        add_card(s12, x, Inches(1.5), Inches(3.8), Inches(0.7), bg_color=r_col, border_color=None)
        tb_h = s12.shapes.add_textbox(x, Inches(1.5), Inches(3.8), Inches(0.7))
        tf_h = tb_h.text_frame
        p_h1 = tf_h.paragraphs[0]
        p_h1.alignment = PP_ALIGN.CENTER
        p_h1.text = r_title
        p_h1.font.bold = True
        p_h1.font.size = Pt(11)
        p_h1.font.color.rgb = TEXT_LIGHT
        p_h2 = tf_h.add_paragraph()
        p_h2.alignment = PP_ALIGN.CENTER
        p_h2.text = r_sub
        p_h2.font.size = Pt(9.5)
        p_h2.font.color.rgb = TEXT_LIGHT

        tb_b = s12.shapes.add_textbox(x + Inches(0.15), Inches(2.25), Inches(3.5), Inches(2.9))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for b_idx, bullet in enumerate(r_bullets):
            p = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p.space_before = Pt(4)
            p.text = bullet
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK

    add_card(s12, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.3), bg_color=HEADER_BG, border_color=CARD_BORDER)
    tb_mat = s12.shapes.add_textbox(Inches(1.0), Inches(5.55), Inches(11.333), Inches(1.2))
    tf_mat = tb_mat.text_frame
    p_mh = tf_mat.paragraphs[0]
    p_mh.text = "Mathematical Formulation: Dual-Metric Benchmarking & Vector Retrieval"
    p_mh.font.bold = True
    p_mh.font.size = Pt(10.5)
    p_mh.font.color.rgb = BRAND_PRIMARY

    p_mb = tf_mat.add_paragraph()
    p_mb.text = (
        "• Composite Score = 0.70 * (Direct Taxonomy Overlap) + 0.30 * (TF-IDF Cosine Similarity)\n"
        "• Vector Retrieval Cosine Similarity = (A • B) / (||A|| * ||B||)  over 128-dimensional embeddings in knowledge_vectors."
    )
    p_mb.font.name = FONT_CODE
    p_mb.font.size = Pt(9.5)
    p_mb.font.color.rgb = BRAND_TEAL

    set_speaker_notes(s12,
        "Here is our AI architecture. RAG stands for Retrieval-Augmented Generation. "
        "Normally, LLMs like Gemini hallucinate generic advice. "
        "In our system, we store verified curriculum modules and project patterns in MongoDB's knowledge_vectors collection. "
        "When a gap is identified (e.g. Docker and AWS), we retrieve the top matching curriculum chunks using cosine similarity, "
        "inject them into Gemini's prompt, and Gemini generates a mathematically grounded 3-week study roadmap and project architecture."
    )

    # =========================================================================
    # SLIDE 13: CORE APPLICATION MODULES & USER INTERFACE
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Application Modules & Streamlit User Experience")
    add_footer(s13, 13)

    modules = [
        ("1. Skill Gap Lab & PDF Ingestion", BRAND_PRIMARY, [
            "• Direct drag-and-drop resume PDF upload",
            "• PyPDF text extraction & email regex identification",
            "• Automatic matching against 30+ canonical skills",
            "• Matched vs. Missing skill visual badges",
            "• Composite compatibility radar & progress bars"
        ]),
        ("2. AI Career Copilot & Project Generator", BRAND_PURPLE, [
            "• Grounded Google Gemini 2.5 Flash orchestration",
            "• Generates tailored 3-week study roadmap",
            "• Custom end-to-end portfolio project blueprints",
            "• Architecture diagram text & recommended DB schemas",
            "• Resume-ready bullet points for portfolio enhancement"
        ]),
        ("3. Market Analytics Dashboard", BRAND_TEAL, [
            "• Live Plotly interactive horizontal & donut charts",
            "• Top demanded skills across active job postings",
            "• Candidate supply vs. employer demand deficit chart",
            "• Score distribution across 4 performance tiers",
            "• Instant PDF export of gap evaluation reports"
        ]),
        ("4. Interactive Data Engine & Query Lab", BRAND_ORANGE, [
            "• Live MongoDB collection browser & document viewer",
            "• Real-time CRUD simulator ($addToSet, $pull, insert_one)",
            "• MongoDB explain('executionStats') query inspector",
            "• Live raw JSON schema viewer with formatted indentation",
            "• Database ping & connection health monitor"
        ])
    ]

    for i, (m_title, m_color, m_bullets) in enumerate(modules):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(1.5 + (i // 2) * 2.7)
        add_card(s13, x, y, Inches(5.75), Inches(2.5), bg_color=CARD_BG, border_color=m_color)
        
        add_card(s13, x, y, Inches(5.75), Inches(0.45), bg_color=m_color, border_color=None)
        tb_mh = s13.shapes.add_textbox(x, y, Inches(5.75), Inches(0.45))
        tf_mh = tb_mh.text_frame
        p = tf_mh.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = m_title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT

        tb_mb = s13.shapes.add_textbox(x + Inches(0.15), y + Inches(0.5), Inches(5.45), Inches(1.9))
        tf_mb = tb_mb.text_frame
        tf_mb.word_wrap = True
        for b_idx, bullet in enumerate(m_bullets):
            p = tf_mb.paragraphs[0] if b_idx == 0 else tf_mb.add_paragraph()
            p.space_before = Pt(3)
            p.text = bullet
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_DARK

    set_speaker_notes(s13,
        "This slide reviews the four core interactive modules in our Streamlit web application. "
        "Module 1 parses resumes and calculates gap scores. "
        "Module 2 is our Gemini-powered AI Career Copilot. "
        "Module 3 displays live analytics powered by our aggregation pipelines. "
        "And Module 4 is our interactive Data Engine Lab, where professors can inspect live MongoDB documents, "
        "test CRUD operations, and view explain() execution plans right from the UI."
    )

    # =========================================================================
    # SLIDE 14: RESULTS, EXPERIMENTAL ANALYSIS & VERIFICATION
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Results & Experimental Output Verification")
    add_footer(s14, 14)

    res_data = [
        ("Metric / Test Case", "Evaluated Collection", "Empirical Output Summary", "System Verification & Finding"),
        ("Top Demanded Skills", "jobs", "Python (4), Docker (4), MongoDB (3), SQL (3)", "Docker and Python identified as primary industry requisites"),
        ("Common Skill Gaps", "analyses", "Docker (2), Power BI (1), Statistics (1), AWS (1)", "Containerization identified as the highest candidate deficiency"),
        ("Talent Supply vs Demand", "resumes + jobs", "Docker: Demand 4 vs Supply 2 (Gap: +2)", "Net deficit of 2 containerization engineers verified"),
        ("Score Bucketing Tiers", "analyses", "80-100%: 2 | 60-79%: 1 | 40-59%: 2 | 0-39%: 1", "Evenly distributed candidate performance across 4 tiers"),
        ("Foreign Join ($lookup)", "analyses + jobs", "ML Engineer: Avg 100% | Cloud Data Eng: 50%", "Multi-collection aggregation verified without data redundancy"),
        ("Atomic $addToSet Test", "users", "Duplicate 'Docker' insertion resulted in modified_count: 0", "Database-level array set deduplication confirmed"),
        ("Unique Key Constraint", "users", "Inserting existing user_id 101 raised DuplicateKeyError (E11000)", "Integrity constraint prevented primary key collision")
    ]

    t14_shape = s14.shapes.add_table(len(res_data), 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.3))
    t14 = t14_shape.table
    t14.columns[0].width = Inches(2.2)
    t14.columns[1].width = Inches(1.8)
    t14.columns[2].width = Inches(4.2)
    t14.columns[3].width = Inches(3.533)

    for r_idx, row in enumerate(res_data):
        for c_idx, cell in enumerate(row):
            tc = t14.cell(r_idx, c_idx)
            tc.text = cell
            p = tc.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5) if r_idx > 0 else Pt(9.5)
            
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_LIGHT
                tc.fill.solid()
                tc.fill.fore_color.rgb = BRAND_PRIMARY
            else:
                tc.fill.solid()
                if c_idx == 0:
                    tc.fill.fore_color.rgb = HEADER_BG
                    p.font.bold = True
                    p.font.color.rgb = BRAND_PRIMARY
                else:
                    tc.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_idx % 2 == 0 else RGBColor(248, 250, 252)
                    p.font.color.rgb = TEXT_DARK

    add_card(s14, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.9), bg_color=RGBColor(240, 253, 250), border_color=BRAND_GREEN)
    tb_stat = s14.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.333), Inches(0.8))
    tf_stat = tb_stat.text_frame
    p = tf_stat.paragraphs[0]
    p.text = "Verified Latency Benchmarks:"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = BRAND_GREEN

    p_body = tf_stat.add_paragraph()
    p_body.text = "• Primary Indexed Read (find_one): < 1.8 ms  |  • Atomic Array Update ($addToSet): < 3.2 ms  |  • Multi-Stage Aggregation: < 11.5 ms  |  • All operations verified under local & Atlas replica sets."
    p_body.font.name = FONT_CODE
    p_body.font.size = Pt(9)
    p_body.font.color.rgb = TEXT_DARK

    set_speaker_notes(s14,
        "Here are our empirical results and verification matrix. "
        "We tested all five aggregation pipelines and CRUD operations. "
        "Top demand is Docker and Python; top skill gap is Docker with a deficit of 2 engineers. "
        "We verified that $addToSet prevents duplicates, and unique indexes throw DuplicateKeyError E11000 on collisions. "
        "Latency across indexed operations was measured under 2 milliseconds."
    )

    # =========================================================================
    # SLIDE 15: CHALLENGES ENCOUNTERED & TECHNICAL SOLUTIONS
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Challenges Encountered & Engineering Solutions")
    add_footer(s15, 15)

    challenges = [
        ("1. Duplicate Array Entries", [
            "Problem: Repeatedly appending candidate skills using $push caused duplicate strings in profiles.",
            "Solution: Replaced $push with the set-preserving atomic operator $addToSet, ensuring mathematical set uniqueness at the database layer without manual code checks."
        ], BRAND_ORANGE),
        ("2. MongoDB Atlas URI Special Characters", [
            "Problem: Passwords containing reserved characters like @ or # broke PyMongo's URI parser.",
            "Solution: Built an automated RFC 3986 percent-encoding sanitizer in sanitize_mongo_uri() (database/db_connection.py) to reliably quote credentials."
        ], BRAND_PRIMARY),
        ("3. Remote Database Latency & Offline Fallback", [
            "Problem: Network timeouts during remote Atlas connection spikes risked crashing the UI.",
            "Solution: Implemented a resilient fallback layer with a 5000ms server selection timeout, falling back seamlessly to cached in-memory structures if MongoDB is unreachable."
        ], BRAND_TEAL),
        ("4. Aggregation Pipeline Memory Limits", [
            "Problem: $unwind on large candidate skill arrays risked exceeding MongoDB's 100MB RAM limit per pipeline stage.",
            "Solution: Positioned selective $project stages early in the pipeline to prune unnecessary fields and built Multikey indexes to feed sorted data directly into $group."
        ], BRAND_PURPLE)
    ]

    for i, (c_title, c_details, c_color) in enumerate(challenges):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(1.5 + (i // 2) * 2.7)
        add_card(s15, x, y, Inches(5.75), Inches(2.5), bg_color=CARD_BG, border_color=c_color)
        
        add_card(s15, x, y, Inches(5.75), Inches(0.45), bg_color=c_color, border_color=None)
        tb_ch = s15.shapes.add_textbox(x, y, Inches(5.75), Inches(0.45))
        tf_ch = tb_ch.text_frame
        p = tf_ch.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = c_title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT

        tb_cb = s15.shapes.add_textbox(x + Inches(0.15), y + Inches(0.5), Inches(5.45), Inches(1.9))
        tf_cb = tb_cb.text_frame
        tf_cb.word_wrap = True
        for d_idx, detail in enumerate(c_details):
            p = tf_cb.paragraphs[0] if d_idx == 0 else tf_cb.add_paragraph()
            p.space_before = Pt(4)
            p.text = detail
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_DARK

    set_speaker_notes(s15,
        "Every strong engineering project addresses real technical challenges. "
        "During development, we faced array duplication which we solved with $addToSet, "
        "Atlas URI connection parsing issues which we solved with RFC 3986 percent encoding, "
        "network timeout resilience which we solved with connection pooling and offline fallback, "
        "and aggregation memory limits which we solved by projecting fields early in pipeline stages."
    )

    # =========================================================================
    # SLIDE 16: FUTURE SCOPE & SCALABILITY ROADMAP
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Future Scope & Scalability Roadmap")
    add_footer(s16, 16)

    future_items = [
        ("1. MongoDB Atlas Native Vector Search", BRAND_PRIMARY, [
            "• Migrate local cosine similarity calculation to native MongoDB Atlas $vectorSearch.",
            "• Utilize Hierarchical Navigable Small World (HNSW) index trees for approximate nearest neighbor retrieval.",
            "• Scale to 1,000,000+ vector documents with sub-10ms semantic similarity queries."
        ]),
        ("2. Real-Time Change Streams", BRAND_TEAL, [
            "• Implement MongoDB Change Streams (db.collection.watch()) via websockets.",
            "• Push instantaneous notifications to candidates whenever a newly posted job matches their skill profile.",
            "• Trigger automatic re-aggregation when candidate skill arrays are updated."
        ]),
        ("3. Multimodal OCR Resume Ingestion", BRAND_PURPLE, [
            "• Incorporate computer vision OCR (Gemini Vision / Tesseract) for scanned, image-based PDF resumes.",
            "• Extract tabular experience sections and portfolio images directly into embedded BSON subdocuments.",
            "• Verify GitHub repository URLs using automated web crawlers."
        ]),
        ("4. Enterprise Multi-Tenant RBAC", BRAND_ORANGE, [
            "• Expand schema with Role-Based Access Control (RBAC).",
            "• Distinct authenticated portals for University Placement Cells (TPO), Corporate Recruiters, and Students.",
            "• Implement MongoDB Client-Side Field Level Encryption (CSFLE) for sensitive contact details."
        ])
    ]

    for i, (f_title, f_col, f_bullets) in enumerate(future_items):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(1.5 + (i // 2) * 2.7)
        add_card(s16, x, y, Inches(5.75), Inches(2.5), bg_color=CARD_BG, border_color=f_col)
        
        add_card(s16, x, y, Inches(5.75), Inches(0.45), bg_color=f_col, border_color=None)
        tb_fh = s16.shapes.add_textbox(x, y, Inches(5.75), Inches(0.45))
        tf_fh = tb_fh.text_frame
        p = tf_fh.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = f_title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT

        tb_fb = s16.shapes.add_textbox(x + Inches(0.15), y + Inches(0.5), Inches(5.45), Inches(1.9))
        tf_fb = tb_fb.text_frame
        tf_fb.word_wrap = True
        for b_idx, bullet in enumerate(f_bullets):
            p = tf_fb.paragraphs[0] if b_idx == 0 else tf_fb.add_paragraph()
            p.space_before = Pt(4)
            p.text = bullet
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK

    set_speaker_notes(s16,
        "Looking forward, there are several exciting scalability paths: "
        "First, moving to native MongoDB Atlas Vector Search with HNSW indexing for million-vector scaling. "
        "Second, using MongoDB Change Streams for real-time socket alerts when jobs match a user. "
        "Third, multimodal OCR parsing for scanned resumes. "
        "And fourth, enterprise multi-tenancy for university placement cells."
    )

    # =========================================================================
    # SLIDE 17: CONCLUSION & KEY LEARNINGS
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Conclusion & Academic Key Learnings")
    add_footer(s17, 17)

    add_card(s17, Inches(0.8), Inches(1.5), Inches(5.75), Inches(5.3))
    tb_c_l = s17.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.35), Inches(4.9))
    tf_cl = tb_c_l.text_frame
    tf_cl.word_wrap = True
    
    p = tf_cl.paragraphs[0]
    p.text = "Summary of Project Outcomes"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_PRIMARY

    outcomes = [
        ("NoSQL Paradigm Validation:", "Demonstrated that MongoDB's document model is fundamentally superior to relational tables for semi-structured talent data, eliminating junction tables and JOIN overhead."),
        ("High-Performance Engineering:", "Constructed multikey B-tree indexes reducing array query evaluation from O(N) collection scans to sub-2ms logarithmic indexed lookups."),
        ("Multi-Stage Pipeline Mastery:", "Successfully formulated 5 complex pipelines leveraging $unwind, $group, $lookup, and $bucket to derive live market supply vs. demand metrics."),
        ("Modern AI & NoSQL Convergence:", "Pioneered the storage of high-dimensional vector embeddings within MongoDB documents to power a grounded RAG copilot with Google Gemini."),
        ("Production-Grade Full-Stack Delivery:", "Built an end-to-end interactive Streamlit web system featuring live telemetry, query inspection, and automated PDF reporting.")
    ]
    for o_title, o_desc in outcomes:
        p = tf_cl.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, f"[+] {o_title} ", bold=True, font_size=Pt(10), color_rgb=BRAND_PRIMARY)
        add_run_to_p(p, o_desc, bold=False, font_size=Pt(9.5), color_rgb=TEXT_MUTED)

    add_card(s17, Inches(6.8), Inches(1.5), Inches(5.75), Inches(5.3))
    tb_c_r = s17.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.35), Inches(4.9))
    tf_cr = tb_c_r.text_frame
    tf_cr.word_wrap = True
    
    p = tf_cr.paragraphs[0]
    p.text = "CSE494 Course Alignment & Competencies"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = BRAND_TEAL

    skills_learned = [
        ("Document Schema Architecture:", "Mastered BSON modeling, embedding vs. referencing design decisions, and document validation rules."),
        ("Atomic Operators:", "Mastered in-place array modification using $addToSet, $push, and $pull without race conditions."),
        ("Aggregation Framework:", "Formulated multi-stage pipelines incorporating foreign collection joins ($lookup) and numerical categorization ($bucket)."),
        ("Query Optimization & Profiling:", "Evaluated execution plans using explain('executionStats') to verify IXSCAN stages and optimize memory."),
        ("Driver & Production Integration:", "Engineered connection pooling, RFC 3986 URI sanitization, and graceful degradation in Python via PyMongo.")
    ]
    for s_title, s_desc in skills_learned:
        p = tf_cr.add_paragraph()
        p.space_before = Pt(6)
        add_run_to_p(p, f"[*] {s_title} ", bold=True, font_size=Pt(10), color_rgb=BRAND_TEAL)
        add_run_to_p(p, s_desc, bold=False, font_size=Pt(9.5), color_rgb=TEXT_MUTED)

    set_speaker_notes(s17,
        "In conclusion, the Skill Gap Analyzer and Career Intelligence Platform "
        "fully satisfies and exceeds the requirements for CSE494 Intelligent NoSQL Databases. "
        "It proves that MongoDB combined with modern Generative AI solves a genuine real-world problem "
        "with exceptional speed, natural document modeling, and zero schema migration friction."
    )

    # =========================================================================
    # SLIDE 18: VIVA Q&A & THANK YOU SLIDE (Dark Executive Theme)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    bg18 = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg18.fill.solid()
    bg18.fill.fore_color.rgb = BG_DARK
    bg18.line.fill.background()

    bar18 = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.06))
    bar18.fill.solid()
    bar18.fill.fore_color.rgb = BRAND_ORANGE
    bar18.line.fill.background()

    tb_ty = s18.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(1.2))
    tf_ty = tb_ty.text_frame
    p = tf_ty.paragraphs[0]
    p.text = "Thank You! Questions & Viva Discussion"
    p.font.name = FONT_HEADING
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    p_sub = tf_ty.add_paragraph()
    p_sub.text = "Open for questions, practical demonstrations, and technical viva evaluation."
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = TEXT_CYAN

    viva_cards = [
        ("Q: Why $addToSet over $push?", [
            "$addToSet guarantees set uniqueness.",
            "Adding a pre-existing skill returns modified_count: 0.",
            "Prevents duplicate strings in array without Python loops."
        ], BRAND_PRIMARY),
        ("Q: How does $lookup work?", [
            "Performs Left Outer Equality Join.",
            "Correlates analyses.job_id with jobs.job_id.",
            "Followed by $unwind and $group for role-level aggregates."
        ], BRAND_TEAL),
        ("Q: What is a Multikey Index?", [
            "Indexes each element in an array field.",
            "Applied to resumes.skills and jobs.required_skills.",
            "Converts array checks from COLLSCAN to logarithmic IXSCAN."
        ], BRAND_ORANGE),
        ("Q: How does RAG use MongoDB?", [
            "knowledge_vectors stores dense 128-float arrays.",
            "Cosine similarity matches candidate gaps to curriculum.",
            "Injected into Gemini prompt for zero-hallucination blueprints."
        ], BRAND_PURPLE)
    ]

    for i, (q_title, q_bullets, q_color) in enumerate(viva_cards):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(2.2 + (i // 2) * 2.3)
        add_card(s18, x, y, Inches(5.75), Inches(2.1), bg_color=BG_CARD_DARK, border_color=q_color)
        
        tb_vh = s18.shapes.add_textbox(x + Inches(0.15), y + Inches(0.1), Inches(5.45), Inches(0.4))
        tf_vh = tb_vh.text_frame
        p = tf_vh.paragraphs[0]
        p.text = q_title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = q_color

        tb_vb = s18.shapes.add_textbox(x + Inches(0.15), y + Inches(0.45), Inches(5.45), Inches(1.5))
        tf_vb = tb_vb.text_frame
        tf_vb.word_wrap = True
        for b_idx, bullet in enumerate(q_bullets):
            p = tf_vb.paragraphs[0] if b_idx == 0 else tf_vb.add_paragraph()
            p.space_before = Pt(2)
            p.text = f"• {bullet}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_LIGHT

    tb_foot18 = s18.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.733), Inches(0.5))
    tf_f18 = tb_foot18.text_frame
    p = tf_f18.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Gudla Shashank • Reg. No: 12316224 • Roll No: 9 • Section: K23DF • Supervisor: Shaik Sana Begum • LPU"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(148, 163, 184)

    set_speaker_notes(s18,
        "Thank you respected supervisor and evaluators for your time and guidance. "
        "I am now ready for questions, live code walkthrough, and practical evaluation of the MongoDB database and Streamlit application."
    )

    output_path = os.path.abspath("Skill_Gap_Analyzer_Presentation_CSE494.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")
    return output_path

if __name__ == "__main__":
    create_presentation()
