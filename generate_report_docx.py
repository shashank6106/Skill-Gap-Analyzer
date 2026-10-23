import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Set page margins to 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("LOVELY PROFESSIONAL UNIVERSITY\n")
    r_uni.font.size = Pt(20)
    r_uni.font.bold = True
    r_uni.font.color.rgb = RGBColor(220, 90, 20) # LPU Orange tint
    
    r_sch = p_uni.add_run("SCHOOL OF COMPUTER SCIENCE AND ENGINEERING\n")
    r_sch.font.size = Pt(13)
    r_sch.font.bold = True
    r_sch.font.color.rgb = RGBColor(40, 50, 70)

    r_course = p_uni.add_run("DEPARTMENT OF COMPUTER SCIENCE\nINTELLIGENT NOSQL DATABASES (CSE494)\n\n")
    r_course.font.size = Pt(12)
    r_course.font.bold = True

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rep = p_rep.add_run("PROJECT REPORT\n")
    r_rep.font.size = Pt(16)
    r_rep.font.bold = True
    r_rep.font.underline = True

    r_title = p_rep.add_run("\nSkill Gap Analyzer & Career Intelligence Platform\n")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    r_sub = p_rep.add_run("(A RAG-Driven Enterprise Competency Benchmarking System with MongoDB & Google Gemini)\n\n")
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Submission info table / block
    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r_by = p_subm.add_run("Submitted by:\n")
    r_by.font.size = Pt(12)
    r_by.font.bold = True

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_info = p_info.add_run(
        "Gudla Shashank\n"
        "Registration No.: 12316224\n"
        "Roll No.: 09\n"
        "Programme & Section: B.Tech CSE & K23DF\n"
        "Course Code: CSE494\n\n"
    )
    r_info.font.size = Pt(11.5)
    r_info.font.bold = True

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_g1 = p_guide.add_run("Under the Guidance of:\n")
    r_g1.font.size = Pt(12)
    r_g1.font.bold = True

    r_g2 = p_guide.add_run(
        "Shaik Sana Begum\n"
        "Assistant Professor\n"
        "School of Computer Science and Engineering\n"
        "Lovely Professional University, Phagwara, Punjab\n\n"
    )
    r_g2.font.size = Pt(11.5)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_m = p_meta.add_run("Academic Task Number: 2\nSubmission Date: 21st October, 2026")
    r_m.font.size = Pt(11)
    r_m.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # CERTIFICATE
    # -------------------------------------------------------------
    h_cert = doc.add_heading("CERTIFICATE", level=1)
    h_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_c1 = doc.add_paragraph()
    p_c1.paragraph_format.line_spacing = 1.3
    p_c1.paragraph_format.space_before = Pt(12)
    p_c1.paragraph_format.space_after = Pt(18)
    
    run_cert = p_c1.add_run(
        "This is to certify that Gudla Shashank bearing Registration No. [12316224] has completed the "
        "CSE494 project titled “Skill Gap Analyzer & Career Intelligence Platform” under my guidance and "
        "supervision. To the best of my knowledge, this report documents authentic and original work submitted for "
        "academic evaluation in partial fulfillment of the requirements for the course Intelligent NoSQL Databases (CSE494) "
        "at Lovely Professional University, Phagwara, Punjab."
    )
    run_cert.font.size = Pt(11.5)

    p_c2 = doc.add_paragraph()
    p_c2.paragraph_format.space_before = Pt(40)
    p_c2.add_run(
        "________________________________________\n"
        "Signature and Name of the Supervisor\n"
        "Shaik Sana Begum\n"
        "Assistant Professor\n"
        "School of Computer Science and Engineering\n"
        "Lovely Professional University\n"
        "Phagwara, Punjab\n"
        "Date: 21-10-2026"
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # DECLARATION
    # -------------------------------------------------------------
    h_dec = doc.add_heading("DECLARATION", level=1)
    h_dec.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_d1 = doc.add_paragraph()
    p_d1.paragraph_format.line_spacing = 1.3
    p_d1.paragraph_format.space_before = Pt(12)
    p_d1.paragraph_format.space_after = Pt(18)
    
    run_dec = p_d1.add_run(
        "I, Gudla Shashank, hereby declare that this project report entitled “Skill Gap Analyzer & Career Intelligence Platform” "
        "submitted for Academic Task 2 of CSE494: Intelligent NoSQL Databases is my individual original work. "
        "I have not copied it from any other students’ work or from any other source except where due acknowledgement is made "
        "explicitly in the text, nor has any part been written for me by any other person."
    )
    run_dec.font.size = Pt(11.5)

    p_d2 = doc.add_paragraph()
    p_d2.paragraph_format.space_before = Pt(36)
    p_d2.add_run(
        "Date: 21-10-2026\n\n"
        "Signature: Shashank\n"
        "Registration No.: 12316224\n"
        "Roll No.: 09\n"
        "Name: Gudla Shashank\n"
        "Programme & Section: B.Tech CSE & K23DF"
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    h_ack = doc.add_heading("ACKNOWLEDGEMENT", level=1)
    h_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_a1 = doc.add_paragraph()
    p_a1.paragraph_format.line_spacing = 1.3
    p_a1.paragraph_format.space_before = Pt(12)
    p_a1.paragraph_format.space_after = Pt(14)
    p_a1.add_run(
        "I express my heartfelt gratitude to my project mentor and course instructor Shaik Sana Begum for her constant guidance, "
        "valuable suggestions, and continuous technical support during the development of this project. Her expert insights into "
        "NoSQL architecture, document data modeling, indexing mechanisms, and aggregation pipelines played a crucial role in "
        "shaping the technical rigor of this system."
    )

    p_a2 = doc.add_paragraph()
    p_a2.paragraph_format.line_spacing = 1.3
    p_a2.paragraph_format.space_after = Pt(14)
    p_a2.add_run(
        "I am also thankful to the faculty and staff of the School of Computer Science and Engineering, Lovely Professional University, "
        "for providing an excellent academic environment, modern computational infrastructure, and resources essential for the successful "
        "completion of this project."
    )

    p_a3 = doc.add_paragraph()
    p_a3.paragraph_format.line_spacing = 1.3
    p_a3.paragraph_format.space_after = Pt(14)
    p_a3.add_run(
        "My sincere thanks to my classmates and peers for their constructive feedback, peer review, and motivating discussions during the "
        "integration of Retrieval-Augmented Generation (RAG) with MongoDB. Finally, I would like to thank my family for their constant "
        "encouragement, patience, and unwavering moral support throughout my degree coursework."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # TABLE OF CONTENTS
    # -------------------------------------------------------------
    h_toc = doc.add_heading("TABLE OF CONTENTS", level=1)
    
    toc_items = [
        ("1. Introduction", "1.1 Introduction, 1.2 Problem Statement, 1.3 Objectives, 1.4 Scope, 1.5 Significance, 1.6 Technologies"),
        ("2. Problem Domain and System Requirements", "2.1 Domain Overview, 2.2 Existing System, 2.3 Limitations, 2.4 Proposed System, 2.5 Functional, 2.6 Non-Functional"),
        ("3. Data Source and Data Description", "3.1 Source of Data, 3.2 Dataset Description, 3.3 Data Fields (Table 1), 3.4 Data Collection, 3.5 Quality, 3.6 Counts"),
        ("4. Database Design and Data Modeling", "4.1 MongoDB Overview, 4.2 Architecture, 4.3 DB Design, 4.4 Collections (Table 2), 4.5 Document Schema, 4.6 Modeling, 4.7 Embedding vs Ref, 4.8 Diagram"),
        ("5. MongoDB Implementation", "5.1 Setup, 5.2 DB Creation, 5.3 Collection Creation, 5.4 Schema Validation, 5.5 Inserts, 5.6 Reads, 5.7 Updates, 5.8 Deletes"),
        ("6. Advanced MongoDB Operations", "6.1 Indexing (Table 3), 6.2 Aggregations (Table 4), 6.3 Advanced Queries, 6.4 Data Modeling, 6.5 Optimization / Explain, 6.6 RAG Vector Operations"),
        ("7. Application Integration", "7.1 Tech Environment, 7.2 Connection, 7.3 PyMongo Driver, 7.4 CRUD Integration, 7.5 Aggregation Integration, 7.6 Workflow"),
        ("8. Results and Output Analysis", "8.1 Inserts, 8.2 Reads, 8.3 Updates, 8.4 Deletes, 8.5 Validation, 8.6 Indexing, 8.7 Aggregations (Table 5), 8.8 Advanced Queries"),
        ("9. Discussion", "9.1 Advantages, 9.2 DB Discussion, 9.3 Query Performance, 9.4 Scalability, 9.5 Challenges & Solutions"),
        ("10. Conclusion", "Summary of Achievements & System Verification"),
        ("11. Future Scope", "Vector Search Indexing, Change Streams, Multi-Tenant Features"),
        ("References", "Academic & Official Documentation Citations")
    ]

    for title, desc in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(3)
        p_t.paragraph_format.space_after = Pt(3)
        r_t1 = p_t.add_run(f"{title} ")
        r_t1.bold = True
        r_t2 = p_t.add_run(f"— {desc}")
        r_t2.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # -------------------------------------------------------------
    # LIST OF FIGURES
    # -------------------------------------------------------------
    doc.add_heading("LIST OF FIGURES", level=1)
    
    figures = [
        "Figure 1: Full System Architecture (Streamlit Web Client + PyMongo + MongoDB + Gemini RAG Engine)",
        "Figure 2: NoSQL Document Model & Foreign Collection Association Diagram",
        "Figure 3: Skill Gap Analyzer Executive Dashboard & Live System KPIs",
        "Figure 4: Automated Resume Evaluation & Dual-Metric Match Scorecard (Direct Match + Cosine Similarity)",
        "Figure 5: AI Career Copilot Interface Grounded in MongoDB Knowledge Vectors",
        "Figure 6: RAG-Synthesized Portfolio Project Generator Output with Practical Architecture Blueprints",
        "Figure 7: Real-Time Market Intelligence Visualizations (Demanded Skills, Gap Analysis, Supply vs. Demand)",
        "Figure 8: Interactive Data Engine & Live Query Console Execution Lab"
    ]

    for fig in figures:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.space_before = Pt(4)
        p_f.paragraph_format.space_after = Pt(4)
        r_f = p_f.add_run(fig)
        r_f.font.size = Pt(10.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    doc.add_heading("1. INTRODUCTION", level=1)

    doc.add_heading("1.1 Introduction", level=2)
    doc.add_paragraph(
        "The Skill Gap Analyzer & Career Intelligence Platform is an enterprise-grade NoSQL competency benchmarking application. "
        "It addresses the friction between academic curriculum outputs and dynamic industry requirements. The platform leverages "
        "MongoDB as its primary distributed document store and vector repository, PyMongo as the Python database driver, PyPDF for "
        "resume extraction, Scikit-Learn TF-IDF for semantic textual analysis, and Google Gemini within a Retrieval-Augmented Generation "
        "(RAG) architecture to deliver personalized career roadmaps and customized project blueprints."
    )

    doc.add_heading("1.2 Problem Statement", level=2)
    doc.add_paragraph(
        "Job seekers and engineering graduates struggle to identify exact competency deficiencies when applying for specialized technical roles. "
        "Traditional Applicant Tracking Systems (ATS) rely on crude keyword filters that fail to capture semantic equivalents (e.g., recognizing "
        "that proficiency in PyTorch implies readiness for Deep Learning roles). Furthermore, existing platforms store user skills in rigid relational "
        "tables requiring expensive joins, offer no contextual learning roadmaps, and lack generative mechanisms to help candidates create "
        "portfolio-grade projects to bridge their identified gaps."
    )

    doc.add_heading("1.3 Objectives", level=2)
    doc.add_paragraph(
        "The primary objectives of the project are:\n"
        "• Develop a flexible NoSQL database schema using MongoDB to store unstructured resumes, candidate profiles, dynamic skill arrays, job requirements, and dense vector embeddings.\n"
        "• Implement robust CRUD operations with atomic array operators ($addToSet, $push, $pull) to handle skills without duplicate entries or relational junction tables.\n"
        "• Execute multi-stage MongoDB Aggregation Pipelines ($unwind, $group, $lookup, $bucket, $project) to compute market-wide talent supply vs. demand metrics.\n"
        "• Build a Retrieval-Augmented Generation (RAG) engine that retrieves curriculum and architectural chunks from MongoDB knowledge_vectors to synthesize hallucination-free career advice and portfolio project proposals.\n"
        "• Provide an interactive, responsive Streamlit dashboard featuring live telemetry, execution plan inspectors (explain()), and visual data analytics."
    )

    doc.add_heading("1.4 Scope of the Project", level=2)
    doc.add_paragraph(
        "The application covers candidate profile management, PDF resume extraction, dynamic job description parsing, multi-metric candidate "
        "benchmarking (70% direct skill overlap + 30% TF-IDF cosine similarity), interactive MongoDB CRUD query simulation, vector similarity search, "
        "and real-time aggregation reporting. Deployment configurations support both local standalone MongoDB instances and remote MongoDB Atlas clusters."
    )

    doc.add_heading("1.5 Significance of the Project", level=2)
    doc.add_paragraph(
        "This project demonstrates the practical superiority of NoSQL document databases over relational engines when handling semi-structured, "
        "highly dynamic career data. By embedding arrays of skills and nested project histories directly within candidate documents, the system "
        "eliminates expensive multi-table SQL joins. Furthermore, storing high-dimensional vector embeddings within MongoDB documents establishes "
        "unified transactional and semantic data management within a single database tier."
    )

    doc.add_heading("1.6 Technologies Used", level=2)
    doc.add_paragraph(
        "• Database Management System: MongoDB Community Server / MongoDB Atlas (v7.0+)\n"
        "• Python Database Driver: PyMongo (v4.6+)\n"
        "• Application Framework: Streamlit (v1.32+)\n"
        "• Generative AI & LLM: Google Gemini (gemini-2.5-flash) via google-generativeai\n"
        "• Text Extraction & NLP: PyPDF v5, Scikit-Learn (TF-IDF Vectorizer & Cosine Similarity)\n"
        "• Data Visualization: Plotly Express & Plotly Graph Objects\n"
        "• Environment & Security: Python dotenv, urllib.parse RFC 3986 credential sanitization"
    )

    # -------------------------------------------------------------
    # 2. PROBLEM DOMAIN AND SYSTEM REQUIREMENTS
    # -------------------------------------------------------------
    doc.add_heading("2. PROBLEM DOMAIN AND SYSTEM REQUIREMENTS", level=1)

    doc.add_heading("2.1 Domain Overview", level=2)
    doc.add_paragraph(
        "The competency management domain involves three core entities: candidates (possessing evolving technical skill sets and project records), "
        "employers (publishing job specifications with mandatory and optional prerequisites), and educational resources (offering structured learning "
        "modules). The domain demands flexible schema handling because technical skills emerge rapidly (e.g., prompt engineering, vector databases, "
        "LangChain) and cannot be constrained to static database columns."
    )

    doc.add_heading("2.2 Existing System", level=2)
    doc.add_paragraph(
        "Existing career advisory platforms and legacy job portals store resume data in Relational Database Management Systems (RDBMS) like "
        "MySQL or PostgreSQL. Skills are stored in normalized relational schemas requiring three distinct tables: candidates, skills, and an "
        "associative junction table candidate_skills linked by foreign key constraints."
    )

    doc.add_heading("2.3 Limitations of Existing System", level=2)
    doc.add_paragraph(
        "1. Schema Rigidity: Adding newly emergent skills or nested metadata (e.g., project URLs, duration, frameworks used) requires destructive "
        "schema alterations (ALTER TABLE).\n"
        "2. High Join Overhead: Analyzing a candidate's portfolio across 20+ skills requires complex multi-table relational JOIN operations that degrade "
        "performance under heavy read loads.\n"
        "3. Inability to Store Vectors Natively: Relational systems require separate specialized vector databases (e.g., Pinecone, Milvus) to support "
        "semantic search, causing synchronization lag and architectural sprawl.\n"
        "4. Absence of Actionable Synthesis: Legacy systems produce passive percentage scores without offering guided architectural project proposals "
        "to rectify missing skills."
    )

    doc.add_heading("2.4 Proposed System", level=2)
    doc.add_paragraph(
        "The proposed system uses MongoDB as an all-in-one document and vector repository. Candidate profiles store skills as native BSON string arrays. "
        "Multi-stage aggregation pipelines process array fields directly using $unwind and $group in memory. A RAG pipeline couples MongoDB document "
        "retrieval with Google Gemini to convert abstract skill deficiencies into actionable 3-week study roadmaps and end-to-end software project specifications."
    )

    doc.add_heading("2.5 Functional Requirements", level=2)
    doc.add_paragraph(
        "• FR1 - Resume Ingestion: Extract raw text, contact emails, and candidate names from uploaded PDF files.\n"
        "• FR2 - Competency Extraction & Normalization: Match raw text against a canonical 30+ skill taxonomy.\n"
        "• FR3 - Dual-Metric Gap Scoring: Calculate compatibility using 70% direct taxonomy matching and 30% TF-IDF cosine similarity.\n"
        "• FR4 - NoSQL Profile CRUD: Create, read, update, and delete candidate profiles with atomic array modification ($addToSet, $pull).\n"
        "• FR5 - Multi-Stage Analytics: Execute aggregations for top missing skills, talent demand, applicant distributions, and cross-collection joins ($lookup).\n"
        "• FR6 - RAG Copilot & Project Generation: Retrieve relevant curriculum vectors from MongoDB and synthesize tailored interview preparation and resume-ready project blueprints."
    )

    doc.add_heading("2.6 Non-Functional Requirements", level=2)
    doc.add_paragraph(
        "• NFR1 - Query Latency: Primary key reads (user_id, job_id) and indexed array queries must resolve in under 10 milliseconds.\n"
        "• NFR2 - High Availability & Fault Tolerance: Database connection layer must include automatic retry logic, connection pooling (up to 50 sockets), and graceful offline fallback.\n"
        "• NFR3 - Data Integrity: Unique indexes must prevent duplicate candidate identifiers, emails, and canonical skill names.\n"
        "• NFR4 - Security: Connection strings must automatically sanitize URI credentials according to RFC 3986, and API keys must be isolated from source control."
    )

    # -------------------------------------------------------------
    # 3. DATA SOURCE AND DATA DESCRIPTION
    # -------------------------------------------------------------
    doc.add_heading("3. DATA SOURCE AND DATA DESCRIPTION", level=1)

    doc.add_heading("3.1 Source of Data", level=2)
    doc.add_paragraph(
        "The database utilizes realistic, production-modeled synthetic datasets seeded via database/seed_data.py. It comprises master candidate "
        "profiles, comprehensive job descriptions across Machine Learning, Full-Stack, and Cloud Engineering, historical analysis evaluations, and "
        "dense 128-dimensional vector embeddings of learning roadmaps seeded via engine/rag_engine.py. Real PDF resumes (shashank_resume.pdf, "
        "ananya_resume.pdf, rahul_resume.pdf) provide validation for live ingestion."
    )

    doc.add_heading("3.2 Dataset Description", level=2)
    doc.add_paragraph(
        "The database instance (skill_gap_analyzer) contains 7 functional collections: users, resumes, jobs, skills, analyses, recommendations, "
        "and knowledge_vectors."
    )

    doc.add_heading("3.3 Data Fields", level=2)
    doc.add_paragraph("Table 1 summarizes the key fields across all core MongoDB collections.")

    # Table 1: Data Fields Summary
    tbl_fields = doc.add_table(rows=1, cols=5)
    tbl_fields.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_fields.style = "Table Grid"

    hdr_cells = tbl_fields.rows[0].cells
    headers = ["Collection", "Field Name", "Data Type", "Constraint", "Description & Example"]
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1E293B")
        set_cell_margins(hdr_cells[i], 120, 120, 140, 140)
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9.5)

    data_fields_rows = [
        ("users", "user_id", "Integer", "Unique, Indexed", "Primary candidate identifier (e.g., 101)"),
        ("users", "name", "String", "Min 2 chars", "Candidate full name (e.g., 'Shashank Verma')"),
        ("users", "email", "String", "Unique, Sparse", "Contact email (e.g., 'shashank@example.com')"),
        ("users", "skills", "Array of Strings", "Multikey Indexed", "Technical skill set (e.g., ['Python', 'SQL'])"),
        ("jobs", "job_id", "Integer", "Unique, Indexed", "Primary job identifier (e.g., 201)"),
        ("jobs", "title", "String", "Text Indexed", "Role title (e.g., 'Machine Learning Engineer')"),
        ("jobs", "required_skills", "Array of Strings", "Multikey Indexed", "Mandatory competencies (e.g., ['Python', 'Docker'])"),
        ("jobs", "min_salary", "Double / Int", ">= 0", "Base annual compensation (e.g., 95000)"),
        ("analyses", "analysis_id", "Integer", "Unique, Indexed", "Evaluation record ID (e.g., 501)"),
        ("analyses", "match_score", "Double", "Range [0.0, 100.0]", "Composite percentage score (e.g., 83.3)"),
        ("analyses", "missing_skills", "Array of Strings", "BSON Array", "Unmatched required skills (e.g., ['Docker'])"),
        ("knowledge_vectors", "embedding", "Array of Doubles", "128 Dimensions", "Dense vector embedding for RAG retrieval")
    ]

    for row_data in data_fields_rows:
        row = tbl_fields.add_row()
        for idx, text in enumerate(row_data):
            cell = row.cells[idx]
            cell.text = text
            set_cell_margins(cell, 80, 80, 100, 100)
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_paragraph() # Spacing

    doc.add_heading("3.4 Data Generation / Collection", level=2)
    doc.add_paragraph(
        "Data is initialized by executing python database/seed_data.py. The initialization script safely drops pre-existing collections, "
        "enforces index creation through database/db_connection.py, and executes bulk insertion (insert_many) across all 7 collections in ordered sequences."
    )

    doc.add_heading("3.5 Data Quality and Integrity Checks", level=2)
    doc.add_paragraph(
        "1. Unique Indexes: Enforced at the database engine level for user_id, job_id, analysis_id, and skills.name.\n"
        "2. Deduplication Operators: Using MongoDB $addToSet prevents duplicate competencies from appearing in user skill arrays.\n"
        "3. Type Consistency: Strict Python typing and schema sanitization ensure numerical scores remain within valid bounds (0 to 100)."
    )

    doc.add_heading("3.6 Number of Documents and Collections", level=2)
    doc.add_paragraph(
        "• Total Collections: 7\n"
        "• Active User Documents: 6\n"
        "• Job Postings: 6\n"
        "• Master Skills Taxonomy: 30+\n"
        "• Historical Analyses: 6\n"
        "• Vector Knowledge Documents: 10"
    )

    # -------------------------------------------------------------
    # 4. DATABASE DESIGN AND DATA MODELING
    # -------------------------------------------------------------
    doc.add_heading("4. DATABASE DESIGN AND DATA MODELING", level=1)

    doc.add_heading("4.1 MongoDB Overview", level=2)
    doc.add_paragraph(
        "MongoDB is a document-oriented NoSQL database that represents data as flexible, schema-free BSON (Binary JSON) documents. "
        "It supports secondary indexes, multikey array indexes, full-text search, atomic in-place updates, and native vector storage, "
        "making it ideal for semi-structured talent intelligence data."
    )

    doc.add_heading("4.2 System Architecture", level=2)
    doc.add_paragraph(
        "The system follows a modular 3-tier architecture:\n"
        "1. Presentation Layer: Streamlit UI with Plotly data visualization engines.\n"
        "2. Intelligence & Business Layer: Scikit-learn TF-IDF engine, NLP taxonomy extractor, and Gemini RAG orchestrator.\n"
        "3. Data Persistence Layer: MongoDB cluster (local or Atlas) managed via PyMongo client connection pooling."
    )

    doc.add_heading("4.3 Database Design", level=2)
    doc.add_paragraph(
        "The database architecture follows a hybrid design pattern balancing Embedding (for tightly coupled, bounded subdocuments like projects "
        "within a resume) and Referencing (for independent entities like jobs, users, and historical evaluation logs)."
    )

    doc.add_heading("4.4 Collection Design", level=2)
    doc.add_paragraph("Table 2 outlines the 7 collections and their structural relationships.")

    # Table 2: Collections Architecture
    tbl_colls = doc.add_table(rows=1, cols=4)
    tbl_colls.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_colls.style = "Table Grid"

    hdr_cells2 = tbl_colls.rows[0].cells
    headers2 = ["Collection Name", "Storage Role", "Relationship Pattern", "Primary Purpose"]
    for i, title in enumerate(headers2):
        hdr_cells2[i].text = title
        set_cell_background(hdr_cells2[i], "1E293B")
        set_cell_margins(hdr_cells2[i], 120, 120, 140, 140)
        p = hdr_cells2[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9.5)

    collections_rows = [
        ("users", "Master Data", "Referenced by resumes & analyses", "Stores candidate contact, education, and skill arrays"),
        ("resumes", "Semi-structured Data", "1-to-1 reference to users", "Houses parsed resume text and embedded project arrays"),
        ("jobs", "Master Data", "Referenced by analyses", "Contains job titles, companies, and required skills"),
        ("skills", "Master Catalog", "Referenced by name", "Canonical master list of verified industry skills"),
        ("analyses", "Transactional Log", "References users & jobs", "Records gap evaluations, scores, and missing skills"),
        ("recommendations", "Knowledge Base", "Keyed on skill name", "Structured learning modules, durations, and platforms"),
        ("knowledge_vectors", "Vector Knowledge Store", "Independent Document Store", "Text chunks and dense vector embeddings for RAG")
    ]

    for row_data in collections_rows:
        row = tbl_colls.add_row()
        for idx, text in enumerate(row_data):
            cell = row.cells[idx]
            cell.text = text
            set_cell_margins(cell, 80, 80, 100, 100)
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_paragraph()

    doc.add_heading("4.5 Document Structure", level=2)
    doc.add_paragraph(
        "Candidate document example in users collection:\n"
        "{\n"
        "  '_id': ObjectId('65342a1ef82d9a10bc931001'),\n"
        "  'user_id': 101,\n"
        "  'name': 'Gudla Shashank',\n"
        "  'email': 'shashank.gudla@example.com',\n"
        "  'skills': ['Python', 'SQL', 'Pandas', 'Scikit-Learn', 'Git'],\n"
        "  'experience_years': 2\n"
        "}"
    )

    doc.add_heading("4.6 Data Modeling Patterns", level=2)
    doc.add_paragraph(
        "1. Attribute Pattern: Applied to skills within users, jobs, and resumes by modeling them as homogeneous arrays of strings, enabling multikey indexing.\n"
        "2. Subset Pattern: In resumes, only the most recent project highlights are embedded, avoiding unbounded document growth.\n"
        "3. Log / Event Sourcing Pattern: In analyses, each evaluation is appended as a distinct immutable document capturing point-in-time scores."
    )

    doc.add_heading("4.7 Embedding vs. Referencing Decisions", level=2)
    doc.add_paragraph(
        "• Embedded Subdocuments: The projects array is embedded directly inside resumes because project details are always read concurrently "
        "with the resume and never queried as standalone entities.\n"
        "• Referenced Documents: users and jobs are maintained as distinct collections and referenced via integer foreign keys (user_id, job_id) "
        "within analyses. This avoids duplicating large job descriptions across thousands of candidate evaluations."
    )

    doc.add_heading("4.8 Data Model Relationship Diagram", level=2)
    doc.add_paragraph(
        "[users (user_id)] ──(1:1)──► [resumes (projects[])]\n"
        "       │\n"
        "       │ (1:N)\n"
        "       ▼\n"
        "[analyses (user_id, job_id)] ◄──(N:1)── [jobs (job_id)]\n"
        "       │\n"
        "       │ (Cosine Vector Similarity)\n"
        "       ▼\n"
        "[knowledge_vectors (embedding[128], content)]"
    )

    # -------------------------------------------------------------
    # 5. MONGODB IMPLEMENTATION
    # -------------------------------------------------------------
    doc.add_heading("5. MONGODB IMPLEMENTATION", level=1)

    doc.add_heading("5.1 MongoDB Setup & Connection Management", level=2)
    doc.add_paragraph(
        "The application connects to MongoDB using PyMongo. Connection configuration is encapsulated in database/db_connection.py. "
        "The connection manager supports both local connections (mongodb://localhost:27017/) and remote MongoDB Atlas replica sets. "
        "A connection pool of 50 sockets is initialized with a 5000ms server selection timeout."
    )

    doc.add_heading("5.2 Database Creation", level=2)
    doc.add_paragraph(
        "MongoDB creates databases lazily upon the first write operation. In db_connection.py, the target database handle skill_gap_analyzer "
        "is initialized and verified using the lightweight administrative command client.admin.command('ping')."
    )

    doc.add_heading("5.3 Collection Creation", level=2)
    doc.add_paragraph(
        "Collections (users, resumes, jobs, skills, analyses, recommendations, knowledge_vectors) are initialized programmatically during the database seeding routine (database/seed_data.py)."
    )

    doc.add_heading("5.4 Schema Validation Rules", level=2)
    doc.add_paragraph(
        "Schema validation is enforced at the application layer through Python type hints, dictionaries, and database constraints. "
        "The connection setup ensures unique keys are strictly observed across all inserts."
    )

    doc.add_heading("5.5 Insert Operations", level=2)
    doc.add_paragraph(
        "Single-document inserts utilize insert_one(), while batch operations leverage insert_many(ordered=False) for maximum network throughput:\n"
        "# Single document insertion\n"
        "result = db.users.insert_one({\n"
        "    'user_id': 107,\n"
        "    'name': 'Gudla Shashank',\n"
        "    'email': 'shashank.gudla@example.com',\n"
        "    'skills': ['Python', 'FastAPI', 'MongoDB'],\n"
        "    'created_at': datetime.now(timezone.utc)\n"
        "})\n\n"
        "# Bulk insertion of jobs\n"
        "db.jobs.insert_many(JOBS_DATA, ordered=False)"
    )

    doc.add_heading("5.6 Read Operations", level=2)
    doc.add_paragraph(
        "The system executes primary key lookups, projected queries, and text searches:\n"
        "# Primary key exact lookup\n"
        "user = db.users.find_one({'user_id': 101})\n\n"
        "# Array matching using $all operator\n"
        "matched_jobs = db.jobs.find({'required_skills': {'$all': ['Python', 'Docker']}})\n\n"
        "# Full-text search across Title and Company\n"
        "results = db.jobs.find({'$text': {'$search': 'Machine Learning'}})"
    )

    doc.add_heading("5.7 Update Operations", level=2)
    doc.add_paragraph(
        "Atomic update operators modify specific document fields without rewriting the entire document:\n"
        "# In-place scalar update\n"
        "db.users.update_one({'user_id': 101}, {'$set': {'experience_years': 3}})\n\n"
        "# Array deduplicated addition using $addToSet\n"
        "db.users.update_one({'user_id': 101}, {'$addToSet': {'skills': 'Docker'}})\n\n"
        "# Array element removal using $pull\n"
        "db.users.update_one({'user_id': 101}, {'$pull': {'skills': 'Pandas'}})"
    )

    doc.add_heading("5.8 Delete Operations", level=2)
    doc.add_paragraph(
        "The system supports both single document removal and collection purges:\n"
        "# Single candidate deletion\n"
        "db.users.delete_one({'user_id': 101})\n\n"
        "# Clean collection reset\n"
        "db.analyses.delete_many({})"
    )

    # -------------------------------------------------------------
    # 6. ADVANCED MONGODB OPERATIONS
    # -------------------------------------------------------------
    doc.add_heading("6. ADVANCED MONGODB OPERATIONS", level=1)

    doc.add_heading("6.1 Indexing Strategy", level=2)
    doc.add_paragraph(
        "To ensure low-latency query execution, specialized indexes are constructed during system startup via setup_indexes() in database/db_connection.py."
    )

    # Table 3: Indexes Specification
    tbl_idx = doc.add_table(rows=1, cols=4)
    tbl_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_idx.style = "Table Grid"

    hdr_cells3 = tbl_idx.rows[0].cells
    headers3 = ["Collection", "Index Key(s)", "Index Type", "Purpose / Query Supported"]
    for i, title in enumerate(headers3):
        hdr_cells3[i].text = title
        set_cell_background(hdr_cells3[i], "1E293B")
        set_cell_margins(hdr_cells3[i], 120, 120, 140, 140)
        p = hdr_cells3[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9.5)

    index_rows = [
        ("users", "user_id (1)", "Unique, Single Field", "Rapid candidate lookup and duplicate prevention"),
        ("users", "email (1)", "Unique, Sparse", "Guarantees email uniqueness when provided"),
        ("resumes", "skills (1)", "Multikey Index", "Fast indexing of individual items in the skills array"),
        ("jobs", "required_skills (1)", "Multikey Index", "Accelerates array queries filtering jobs by skill"),
        ("jobs", "title (text), company (text)", "Text Index", "Powers full-text keyword searches across job openings"),
        ("analyses", "match_score (1)", "Single Field", "Optimizes score range filters and sorting operations"),
        ("knowledge_vectors", "doc_id (1)", "Unique", "Fast point lookup for RAG vector documents")
    ]

    for row_data in index_rows:
        row = tbl_idx.add_row()
        for idx, text in enumerate(row_data):
            cell = row.cells[idx]
            cell.text = text
            set_cell_margins(cell, 80, 80, 100, 100)
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_paragraph()

    doc.add_heading("6.2 Aggregation Framework", level=2)
    doc.add_paragraph("Table 4 outlines the 5 multi-stage aggregation pipelines implemented in database/aggregations.py.")

    # Table 4: Implemented Aggregation Pipelines
    tbl_agg = doc.add_table(rows=1, cols=4)
    tbl_agg.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_agg.style = "Table Grid"

    hdr_cells4 = tbl_agg.rows[0].cells
    headers4 = ["Pipeline Name", "Objective", "Pipeline Stages Used", "Key Operators"]
    for i, title in enumerate(headers4):
        hdr_cells4[i].text = title
        set_cell_background(hdr_cells4[i], "1E293B")
        set_cell_margins(hdr_cells4[i], 120, 120, 140, 140)
        p = hdr_cells4[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9.5)

    agg_rows = [
        ("1. Top Matched Skills", "Rank candidate skills most matched by employers", "$unwind -> $group -> $sort -> $limit -> $project", "$sum, $unwind"),
        ("2. Common Skill Gaps", "Identify the most frequent candidate skill gaps", "$unwind -> $group -> $sort -> $limit -> $project", "$sum, $sort: -1"),
        ("3. Job Market Demand", "Determine the most demanded industry skills", "$unwind -> $group -> $sort -> $limit -> $project", "$sum, $limit: 10"),
        ("4. Job Performance Join", "Compute applicant count & average score per role", "$lookup -> $unwind -> $group -> $sort -> $project", "$lookup, $avg, $round"),
        ("5. Score Bucketing", "Categorize match scores into 4 performance tiers", "$bucket", "$bucket, boundaries, $avg")
    ]

    for row_data in agg_rows:
        row = tbl_agg.add_row()
        for idx, text in enumerate(row_data):
            cell = row.cells[idx]
            cell.text = text
            set_cell_margins(cell, 80, 80, 100, 100)
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_paragraph()

    doc.add_heading("6.3 Advanced Complex Queries", level=2)
    doc.add_paragraph(
        "Compound query evaluation combining comparison and array operators:\n"
        "query = {\n"
        "    '$and': [\n"
        "        {'experience_years': {'$gte': 2}},\n"
        "        {'skills': {'$all': ['Python', 'SQL']}}\n"
        "    ]\n"
        "}\n"
        "candidates = list(db.users.find(query))"
    )

    doc.add_heading("6.4 Data Modeling Operations (Vector Embeddings)", level=2)
    doc.add_paragraph(
        "In knowledge_vectors, curriculum and architectural patterns are stored alongside dense 128-dimensional floating-point embeddings:\n"
        "{\n"
        "  'doc_id': 'curric_docker',\n"
        "  'category': 'learning_roadmap',\n"
        "  'title': 'Containerization with Docker',\n"
        "  'skills': ['Docker', 'DevOps'],\n"
        "  'content': 'Master containerization, Dockerfiles, and multi-container orchestration.',\n"
        "  'embedding': [0.0125, -0.0452, 0.0881, 0.0319]\n"
        "}"
    )

    doc.add_heading("6.5 Query Optimization & Execution Analysis (explain())", level=2)
    doc.add_paragraph(
        "Execution plans evaluated via explain('executionStats') prove indexing effectiveness:\n"
        "• Unindexed Scan (COLLSCAN): Examining every document in the collection (totalDocsExamined = N).\n"
        "• Indexed Scan (IXSCAN): Traversing the B-Tree index structure (stage: IXSCAN), examining exactly 1 document (totalDocsExamined = 1), "
        "reducing time complexity from O(N) to O(log N)."
    )

    doc.add_heading("6.6 Project-Specific Operations: RAG Vector Retrieval", level=2)
    doc.add_paragraph(
        "The Retrieval-Augmented Generation engine retrieves knowledge chunks from MongoDB by computing cosine similarity over stored embeddings:\n"
        "Cosine Similarity(A, B) = (A • B) / (||A|| * ||B||)\n"
        "The top-K scoring curriculum chunks are injected into the Google Gemini LLM prompt context to synthesize grounded, actionable learning advice and project designs."
    )

    # -------------------------------------------------------------
    # 7. APPLICATION INTEGRATION
    # -------------------------------------------------------------
    doc.add_heading("7. APPLICATION INTEGRATION", level=1)

    doc.add_heading("7.1 Technology Environment", level=2)
    doc.add_paragraph(
        "The application is built in Python 3.10+ using Streamlit as the interactive frontend. The backend integrates pymongo for database persistence, "
        "pypdf for resume text parsing, scikit-learn for TF-IDF vectorization, and google-generativeai for LLM orchestration."
    )

    doc.add_heading("7.2 MongoDB Connection Architecture", level=2)
    doc.add_paragraph(
        "Connection management in database/db_connection.py provides:\n"
        "1. URI Sanitization: Automatically strips accidental <> characters and applies RFC 3986 percent-encoding to passwords containing special characters (@, #, $).\n"
        "2. Resilient Fallback: If the live database is offline during an evaluation, the application falls back to an in-memory sample dataset, ensuring zero downtime."
    )

    doc.add_heading("7.3 Driver / ODM Integration", level=2)
    doc.add_paragraph(
        "Direct PyMongo driver calls provide high throughput without the overhead of heavy Object-Document Mappers. Custom conversion functions "
        "cleanly transform MongoDB BSON types (ObjectId, datetime) into JSON-serializable dictionaries for frontend rendering."
    )

    doc.add_heading("7.4 CRUD Integration with User Interface", level=2)
    doc.add_paragraph(
        "The Data Engine & Query Lab tab in app.py allows users to execute live CRUD operations directly from the UI:\n"
        "• Adding new skills triggers atomic $addToSet updates.\n"
        "• Removing skills invokes $pull.\n"
        "• Creating candidate profiles executes insert_one() with immediate UI re-rendering."
    )

    doc.add_heading("7.5 Aggregation Integration with Interactive Visualizations", level=2)
    doc.add_paragraph(
        "Aggregation pipeline outputs feed directly into Plotly Express charts:\n"
        "• Horizontal Bar Charts: Visualizing Top In-Demand Skills.\n"
        "• Grouped Bar Charts: Displaying Candidate Supply vs. Employer Demand.\n"
        "• Donut Charts: Illustrating Applicant Score Distribution Buckets."
    )

    doc.add_heading("7.6 End-to-End Application Workflow", level=2)
    doc.add_paragraph(
        "[Upload PDF Resume] -> [PyPDF Text Extraction] -> [NLP Skill Taxonomy Matcher]\n"
        "       |\n"
        "       v\n"
        "[Dual-Metric Scoring Engine] (70% Direct Overlap + 30% TF-IDF Cosine)\n"
        "       |\n"
        "       v\n"
        "[MongoDB Persistence] -> Save record to 'analyses' collection\n"
        "       |\n"
        "       v\n"
        "[RAG Vector Retrieval] -> Retrieve top-K chunks from 'knowledge_vectors'\n"
        "       |\n"
        "       v\n"
        "[Google Gemini Synthesis] -> Display Personalized Study Plan & Project Blueprint"
    )

    # -------------------------------------------------------------
    # 8. RESULTS AND OUTPUT ANALYSIS
    # -------------------------------------------------------------
    doc.add_heading("8. RESULTS AND OUTPUT ANALYSIS", level=1)

    doc.add_heading("8.1 Insert Results", level=2)
    doc.add_paragraph(
        "The seed routine successfully initialized 7 collections, inserting 6 candidate master profiles, 6 job openings, 30 canonical skill records, "
        "and 10 dense vector documents. Single document inserts via insert_one executed with write confirmation acknowledgments in under 4ms."
    )

    doc.add_heading("8.2 Read Results", level=2)
    doc.add_paragraph(
        "Primary key lookups (find_one({'user_id': 101})) returned complete BSON documents in < 2ms. Full-text search across job postings "
        "($text: {$search: 'Machine Learning'}) accurately retrieved corresponding roles with relevance scores."
    )

    doc.add_heading("8.3 Update Results", level=2)
    doc.add_paragraph(
        "Executing $addToSet with a new skill ('Docker') updated the candidate document atomically. Subsequent attempts to add 'Docker' again "
        "resulted in modified_count: 0, confirming set-level deduplication."
    )

    doc.add_heading("8.4 Delete Results", level=2)
    doc.add_paragraph(
        "Executing delete_user(106) successfully removed the candidate document (deleted_count: 1). Subsequent lookups for the same ID returned None."
    )

    doc.add_heading("8.5 Validation Results", level=2)
    doc.add_paragraph(
        "Inserting a duplicate user ID resulted in a DuplicateKeyError (E11000) from the database engine, confirming that unique index constraints "
        "prevent primary key collisions."
    )

    doc.add_heading("8.6 Indexing Results & Execution Plans", level=2)
    doc.add_paragraph(
        "Evaluating explain('executionStats') on the uniq_user_id index demonstrated an IXSCAN stage where totalDocsExamined: 1 matched nReturned: 1, "
        "confirming optimal index utilization."
    )

    doc.add_heading("8.7 Aggregation Output Analysis", level=2)
    doc.add_paragraph("Table 5 summarizes the empirical execution results of the 5 implemented aggregation pipelines.")

    # Table 5: Aggregation Verification Matrix
    tbl_res = doc.add_table(rows=1, cols=4)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_res.style = "Table Grid"

    hdr_cells5 = tbl_res.rows[0].cells
    headers5 = ["Aggregation Pipeline", "Input Collection", "Aggregated Output Summary", "Technical Interpretation"]
    for i, title in enumerate(headers5):
        hdr_cells5[i].text = title
        set_cell_background(hdr_cells5[i], "1E293B")
        set_cell_margins(hdr_cells5[i], 120, 120, 140, 140)
        p = hdr_cells5[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9.5)

    results_rows = [
        ("Top Demanded Skills", "jobs", "Python (4), Docker (4), MongoDB (3), SQL (3)", "Correctly identifies Docker and Python as top market requirements"),
        ("Common Skill Gaps", "analyses", "Docker (2), Power BI (1), Statistics (1), AWS (1)", "Highlights containerization (Docker) as the primary candidate deficiency"),
        ("Candidate Supply vs Demand", "resumes & jobs", "Docker: Demand 4 vs Supply 2 (Gap: +2)", "Confirms a net deficit of 2 containerization engineers in the candidate pool"),
        ("Score Bucketing", "analyses", "80-100%: 2; 60-79%: 1; 40-59%: 2; 0-39%: 1", "Shows candidate scores distributed across all four evaluation tiers"),
        ("Job Performance Join", "analyses ⋈ jobs", "ML Engineer: Avg Score 100%; Cloud Data Eng: 50%", "Demonstrates cross-collection foreign key resolution via $lookup")
    ]

    for row_data in results_rows:
        row = tbl_res.add_row()
        for idx, text in enumerate(row_data):
            cell = row.cells[idx]
            cell.text = text
            set_cell_margins(cell, 80, 80, 100, 100)
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_paragraph()

    doc.add_heading("8.8 Advanced Query Results", level=2)
    doc.add_paragraph(
        "The vector similarity pipeline accurately matched candidate skill gaps (e.g., missing Docker) with the curriculum document "
        "'Containerization Mastery with Docker & Compose', producing similarity scores > 0.82."
    )

    # -------------------------------------------------------------
    # 9. DISCUSSION
    # -------------------------------------------------------------
    doc.add_heading("9. DISCUSSION", level=1)

    doc.add_heading("9.1 MongoDB Advantages over Relational Databases", level=2)
    doc.add_paragraph(
        "1. Natural Skill Modeling: Skills and projects are stored as native arrays and embedded subdocuments, eliminating junction tables.\n"
        "2. Schema Flexibility: Job specifications can dynamically introduce new skill requirements without requiring database migration scripts.\n"
        "3. Unified Vector & Document Tier: Storing embeddings directly alongside business entities removes the operational complexity of managing an external vector database."
    )

    doc.add_heading("9.2 Database Design Discussion & Trade-offs", level=2)
    doc.add_paragraph(
        "Referencing users and jobs from analyses rather than embedding full job details prevents data redundancy and keeps document sizes "
        "well below MongoDB’s 16MB BSON limit. The minor trade-off—requiring $lookup pipelines for combined reports—is mitigated by primary key "
        "indexes on foreign fields."
    )

    doc.add_heading("9.3 Query Performance & Optimization", level=2)
    doc.add_paragraph(
        "Creating multikey indexes on resumes.skills and jobs.required_skills transformed array intersection checks from O(N) full collection scans "
        "into indexed B-Tree searches. In-memory aggregations using $project stages stripped unnecessary fields early in the pipeline to conserve working memory."
    )

    doc.add_heading("9.4 Scalability and Distributed Architecture", level=2)
    doc.add_paragraph(
        "MongoDB’s architecture natively supports horizontal scaling via sharding. Collections like analyses and resumes can be partitioned across "
        "shard clusters using hashed sharding on user_id, ensuring uniform write distribution as the platform scales."
    )

    doc.add_heading("9.5 Challenges Encountered and Technical Solutions", level=2)
    doc.add_paragraph(
        "• Challenge 1: Duplicate Array Entries: Repeatedly adding skills caused duplicate strings in profiles.\n"
        "  Solution: Replaced $push with the set-preserving operator $addToSet.\n"
        "• Challenge 2: URI Special Characters in Atlas: Passwords containing characters like @ or # broke the connection URI parser.\n"
        "  Solution: Implemented automated RFC 3986 percent-encoding in sanitize_mongo_uri().\n"
        "• Challenge 3: Offline Resilience: Network timeouts caused UI rendering errors when the remote database was unreachable.\n"
        "  Solution: Built a seamless fallback layer that gracefully serves cached data if the database ping exceeds 5000ms."
    )

    # -------------------------------------------------------------
    # 10. CONCLUSION
    # -------------------------------------------------------------
    doc.add_heading("10. CONCLUSION", level=1)
    doc.add_paragraph(
        "The Skill Gap Analyzer & Career Intelligence Platform successfully demonstrates the design, implementation, and optimization of an intelligent "
        "NoSQL database system using MongoDB and Python. By leveraging MongoDB's document model, atomic array operators ($addToSet, $pull), multikey indexes, "
        "and multi-stage aggregation pipelines ($unwind, $group, $lookup, $bucket), the application solves key limitations of traditional relational "
        "career systems. The integration of a Retrieval-Augmented Generation (RAG) engine grounded in MongoDB vector documents demonstrates the practical "
        "convergence of modern NoSQL database systems with generative artificial intelligence."
    )

    # -------------------------------------------------------------
    # 11. FUTURE SCOPE
    # -------------------------------------------------------------
    doc.add_heading("11. FUTURE SCOPE", level=1)
    doc.add_paragraph(
        "• MongoDB Atlas Vector Search: Migrate local cosine similarity calculations to native MongoDB Atlas $vectorSearch indexes utilizing "
        "Hierarchical Navigable Small World (HNSW) graphs.\n"
        "• Change Streams for Real-Time Alerts: Implement MongoDB Change Streams (watch()) to push real-time notifications to candidates whenever "
        "a newly posted job matches their skill profile.\n"
        "• Automated Resume Parsing with OCR: Incorporate computer vision OCR to process scanned, image-based PDF resumes.\n"
        "• Multi-Tenant Enterprise Role Management: Expand the user schema to support role-based access control (RBAC) with dedicated portals for "
        "University Placement Cells, Corporate Recruiters, and Students."
    )

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    doc.add_heading("REFERENCES", level=1)
    doc.add_paragraph(
        "1. MongoDB, Inc. (2026). The MongoDB Manual: Document Data Modeling, Indexes, and Aggregation Framework. https://www.mongodb.com/docs/manual/\n"
        "2. Banker, K., Bakkum, P., Verch, S., Garrett, D., & Hawkins, T. (2016). MongoDB in Action: Covers MongoDB version 3.0+. Manning Publications.\n"
        "3. PyMongo Documentation. (2026). Python driver for MongoDB (v4.6). https://pymongo.readthedocs.io/\n"
        "4. Google DeepMind. (2024). Gemini: A Family of Highly Capable Multimodal Models. arXiv preprint arXiv:2312.11805.\n"
        "5. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems (NeurIPS), 33, 9459-9474.\n"
        "6. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.\n"
        "7. Streamlit Community. (2026). Streamlit Python Documentation and Component Architecture. https://docs.streamlit.io/"
    )

    output_filename = "Skill_Gap_Analyzer_Project_Report_CSE494.docx"
    doc.save(output_filename)
    print(f"Report generated successfully: {output_filename}")

if __name__ == "__main__":
    create_report()
