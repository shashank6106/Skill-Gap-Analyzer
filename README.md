# ✦ Skill Gap Analyzer & Career Intelligence Platform (with RAG & MongoDB)

A full-stack enterprise competency platform powered by **Python**, **PyMongo**, **MongoDB**, **Google Gemini**, and a **Retrieval-Augmented Generation (RAG)** vector engine.

Analyzes PDF resumes against job descriptions, calculates direct and semantic skill gaps, retrieves relevant curriculum modules from MongoDB vector stores, and generates hyper-personalized career advice and portfolio project proposals.

---

## 🏛️ Technology Stack

```
Python
   │
   ├── PyMongo ───────────→ MongoDB (Core NoSQL Store: CRUD, Aggregations & Vector Embeddings)
   │
   ├── RAG Engine ────────→ Semantic vector retrieval from MongoDB + Google Gemini LLM
   │
   ├── PyPDF ─────────────→ Resume extraction (Text, Metadata, Contact Info)
   │
   ├── NLP & Regex ───────→ Taxonomy-based Skill extraction
   │
   ├── Scikit-learn ──────→ TF-IDF Semantic Cosine Similarity
   │
   └── Streamlit + Plotly → Minimalist Light & Dark Enterprise Web UI
```

---

## 🚀 Key Features

### 1. 📄 Skill Gap Analysis & Benchmarking
- Automated parsing of PDF resumes using `PyPDF`.
- Multi-dimensional scoring: **Direct Skill Overlap** (70%) + **Scikit-Learn TF-IDF Cosine Similarity** (30%).
- Real-time persistence of evaluation records to MongoDB collection: `analyses`.
- Side-by-side competency badges (Matched vs Missing Gaps) with dynamic priority roadmaps.

### 2. 📝 ATS Resume Bullet Point Optimizer (RAG Engine)
- Rewrites passive, weak resume statements into high-impact STAR framework achievements (*Situation, Task, Action, Result*).
- Naturally infuses target employer keywords retrieved from the MongoDB `jobs` collection.
- Displays an ATS Impact Score Before vs After (e.g., `48/100 ➔ 93/100`).
- Provides one-click persistence of optimized bullets to candidate profiles in MongoDB using the `$set` operator.

### 3. ✦ AI Career Copilot (RAG Engine)
- Contextual career guidance powered by **Google Gemini** (`gemini-2.5-flash`).
- Grounded in real-time knowledge retrieved from MongoDB collection: `knowledge_vectors`.
- Helps candidates prepare for technical interviews, design 3-week study plans, and articulate skill gaps.

### 3. 🛠️ Personalized Project Generator (RAG)
- Generates 3 tailored, resume-worthy project proposals designed to prove missing skills.
- Combines the candidate's *existing strengths* with their *target gaps* so projects are practical and realistic.
- Provides high-level architecture flows and ready-to-use resume bullet points.

### 4. 🧬 MongoDB Vector Search Explorer
- Live semantic search across jobs, curriculum modules, and project design patterns stored in MongoDB.
- Cosine similarity calculation over dense document vector embeddings.

### 5. 📊 Market Intelligence & Aggregation Analytics
- Live metrics directly aggregated via PyMongo pipelines:
  - Top Demanded Skills in Job Market (`$unwind` + `$group`).
  - Most Common Skill Gaps across candidate pool.
  - Candidate Supply vs Employer Demand Gap analysis.
  - Role Compatibility Leaderboard (`$lookup` join between `analyses` and `jobs`).

### 6. ⚡ Data Engine & Query Console (Viva Demonstration Lab)
- Interactive playground to execute live CRUD operations (`insert_one`, `find_one`, array `$addToSet` deduplication, `$pull`, `delete_one`).
- Raw aggregation pipeline inspector and BSON document browser.

---

## 🗄️ MongoDB Collections Architecture

**Database Name:** `skill_gap_analyzer`

| Collection | Description | Key Operators & Indexes |
| :--- | :--- | :--- |
| `users` | Candidate master profiles | `user_id` (unique), `$addToSet`, `$push`, `$pull` |
| `resumes` | Extracted resume documents & project subdocuments | Multikey index on `skills` array |
| `jobs` | Job postings with requirements & descriptions | Text index on `title`, Multikey index on `required_skills` |
| `skills` | Master catalog of canonical technical skills | Unique index on skill `name`, index on `category` |
| `analyses` | Evaluated skill gaps, scores, and matched skills | Index on `user_id`, `job_id`, `match_score` |
| `recommendations`| Targeted learning roadmaps & course links | Unique index on `skill` |
| `knowledge_vectors`| Vector embeddings of curriculum, jobs & project patterns | Unique index on `doc_id`, index on `category` |

---

## ⚡ Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Seed Database & Vector Knowledge Base
```bash
python database/seed_data.py
python -c "from engine.rag_engine import seed_vector_knowledge_base; print('Seeded vector embeddings:', seed_vector_knowledge_base(True))"
```

### 3. Run Web Dashboard
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

*(Optional: Enter your free Google Gemini API key in the sidebar for live conversational generation; works with high-quality local RAG synthesis if left blank!)*

---

## 🎓 Academic Viva & Technical Presentation

Read [MONGODB_VIVA_GUIDE.md](file:///MONGODB_VIVA_GUIDE.md) for full explanations of:
1. Why MongoDB fits unstructured resume and vector embedding data better than SQL.
2. How the RAG pipeline retrieves vector chunks from MongoDB and augments Gemini LLM generation.
3. The exact mechanics of `$unwind`, `$group`, `$sort`, and `$lookup`.
4. Difference between array operators `$push` and `$addToSet`.
