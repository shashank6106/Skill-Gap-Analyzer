# 🎯 Skill Gap Analyzer using MongoDB & PyMongo

A full-stack, NoSQL-centric application built to analyze resumes against job descriptions, calculate skill gaps, recommend priority learning roadmaps, and perform real-time market analytics using **MongoDB**, **PyMongo**, and **Python**.

---

## 🏗️ Technology Stack

```
Python
   │
   ├── PyMongo ───────────→ MongoDB (Core Database: CRUD, Indexing, Aggregations)
   │
   ├── PyPDF ─────────────→ Resume extraction (Text, Metadata, Contact Info)
   │
   ├── NLP & Regex ───────→ Taxonomy-based Skill & Project extraction
   │
   ├── Scikit-learn ──────→ TF-IDF Semantic Cosine Similarity
   │
   └── Streamlit + Plotly → Interactive Dashboard & Viva Demo Lab
```

---

## 🗄️ MongoDB Database Architecture

**Database Name:** `skill_gap_analyzer`

### Collections Overview:

| Collection | Description | Key Operators & Indexes |
| :--- | :--- | :--- |
| `users` | Candidate master profiles | `user_id` (unique), `$addToSet`, `$push`, `$pull` |
| `resumes` | Extracted resume documents & project subdocuments | Multikey index on `skills` array |
| `jobs` | Job postings with requirements & descriptions | Text index on `title`, Multikey index on `required_skills` |
| `skills` | Master catalog of canonical technical skills | Unique index on skill `name`, index on `category` |
| `analyses` | Evaluated skill gaps, scores, and matched skills | Index on `user_id`, `job_id`, `match_score` |
| `recommendations`| Targeted learning roadmaps & course links | Unique index on `skill` |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- MongoDB Server running locally (`mongodb://localhost:27017/`) or MongoDB Atlas URI

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize & Seed MongoDB
Populate the database with realistic initial users, jobs, skills, recommendations, and sample analyses:
```bash
python database/seed_data.py
```

### 4. Run the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Terminal Viva Demonstration (`cli_demo.py`)

For instant terminal demonstrations during your lab or viva exam, run:
```bash
python cli_demo.py
```
This script steps through:
1. Live MongoDB connection verification
2. PyMongo `insert_one()`
3. PyMongo `find_one()`
4. Array operator `$addToSet` (demonstrating deduplication)
5. Array operator `$pull`
6. Query operators `$in`, `$all`, `$gte`, `$lte`
7. Aggregation Pipeline 1: Most Demanded Job Skills (`$unwind` + `$group` + `$sort`)
8. Aggregation Pipeline 2: Most Common Missing Skills (`$unwind` + `$group`)
9. Aggregation Pipeline 3: Job Leaderboard with `$lookup` (Foreign Join)
10. PyMongo `delete_one()` cleanup

---

## 🌟 Application Features

### Tab 1: 📄 Resume Analyzer & Skill Gap Report
- Upload any candidate resume (PDF) or pick from pre-loaded samples (`shashank_resume.pdf`, `ananya_resume.pdf`, `rahul_resume.pdf`).
- Automated extraction of contact details, education, and technical skills using `PyPDF` and NLP taxonomy matching.
- Select target job opening directly from MongoDB.
- One-click analysis calculating:
  - **Direct Skill Overlap:** Exact matched skills vs missing skills.
  - **Scikit-Learn TF-IDF Cosine Similarity:** Semantic comparison between resume text and job description.
  - **Hybrid Match Score:** Weighted combination (70% direct skills + 30% semantic text).
- Document automatically saved to MongoDB `analyses` collection via `insert_analysis()`.
- Interactive Match Score Gauge, Matched/Missing skill badges, and targeted course recommendations loaded from MongoDB `recommendations`.

### Tab 2: 💼 Job Market & Requirement Management
- Filter job openings using MongoDB array operators:
  - `$in`: Jobs requiring ANY selected skill.
  - `$all`: Jobs requiring ALL selected skills.
- Add new job openings live into MongoDB using `jobs.insert_one()`.

### Tab 3: 📊 MongoDB Aggregation Analytics Dashboard
- Live metrics directly aggregated via PyMongo:
  - Total Users, Resumes, Jobs, Analyses, and Average Match Score.
  - Top Demanded Skills in Job Market (`$unwind` + `$group`).
  - Most Common Skill Gaps across candidate pool.
  - Candidate Supply vs Employer Demand Gap analysis.
  - Job Match Performance Leaderboard (`$lookup` join between `analyses` and `jobs`).
- "View Pipeline" expanders showing the exact PyMongo aggregation code behind every chart.

### Tab 4: 🔌 PyMongo & NoSQL Viva Demo Lab
- **Live CRUD Playground:** Execute `insert_one()`, `find_one()`, `update_one()` with `$addToSet`, `$pull`, and `delete_one()`.
- **Pipeline Inspector:** Execute any aggregation pipeline live and view JSON definition and table results.
- **Collection Inspector:** View raw BSON/JSON documents across any of the 6 collections.
- **Viva Q&A Reference:** Instant answers to common NoSQL exam questions.

---

## 📂 Project Directory Structure

```
Skill Gap Analyzer/
│
├── database/
│   ├── __init__.py           # Package exports
│   ├── db_connection.py      # PyMongo client, connection test, index setup
│   ├── crud.py               # Complete CRUD methods ($addToSet, $pull, $in, $gte, etc.)
│   ├── aggregations.py       # MongoDB Aggregation pipelines ($unwind, $group, $lookup)
│   └── seed_data.py          # Seeder script for initial data
│
├── engine/
│   ├── __init__.py
│   ├── resume_parser.py      # PyPDF text and metadata extractor
│   ├── skill_extractor.py    # NLP taxonomy & regex skill extractor
│   └── matcher.py            # Overlap calculation, TF-IDF cosine similarity, recommendations
│
├── sample_resumes/           # Ready-to-upload PDF resumes for testing
│   ├── shashank_resume.pdf
│   ├── ananya_resume.pdf
│   └── rahul_resume.pdf
│
├── utils/
│   ├── __init__.py
│   └── pdf_generator.py      # Programmatic PDF generator
│
├── app.py                    # Complete Streamlit interactive web dashboard
├── cli_demo.py               # Standalone terminal demo for quick viva presentation
├── requirements.txt          # Python library dependencies
├── .env.example              # Environment variables template
├── .env                      # Local MongoDB connection configuration
├── README.md                 # Project documentation
└── MONGODB_VIVA_GUIDE.md     # Detailed MongoDB NoSQL viva Q&A and pipeline guide
```

---

## 🎓 For Academic / Evaluation Submission

Read [MONGODB_VIVA_GUIDE.md](file:///MONGODB_VIVA_GUIDE.md) for full explanations of:
1. Why MongoDB fits unstructured resume/skill data better than SQL.
2. The exact mechanics of `$unwind`, `$group`, `$sort`, and `$lookup`.
3. The vital difference between `$push` and `$addToSet`.
4. Index types used: Single field, Multikey (arrays), Compound, and Full-Text search.
