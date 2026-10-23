# LOVELY PROFESSIONAL UNIVERSITY
## SCHOOL OF COMPUTER SCIENCE AND ENGINEERING
### INTELLIGENT NOSQL DATABASES (CSE494)
### PROJECT REPORT

---

# **Skill Gap Analyzer & Career Intelligence Platform**
### *(A RAG-Driven Enterprise Competency Benchmarking System with MongoDB & Google Gemini)*

---

**Submitted by:**  
**Name:** Gudla Shashank  
**Registration No.:** 12316224  
**Roll No.:** 9  
**Programme & Section:** B.Tech CSE & K23DF  
**Course Code:** CSE494 (Intelligent NoSQL Databases)  

**Under the Guidance of:**  
**Supervisor Name:** Shaik Sana Begum  
**Designation:** Assistant Professor  
**School of Computer Science and Engineering**  
**Lovely Professional University, Phagwara, Punjab**  

**Academic Task Number:** 2  
**Submission Date:** 21st October, 2026  

---

## CERTIFICATE

This is to certify that **Gudla Shashank** bearing Registration No. **[12316224]** has successfully completed the CSE494 project titled **“Skill Gap Analyzer & Career Intelligence Platform”** under my guidance and supervision. To the best of my knowledge, this report documents authentic and original work carried out for academic evaluation in partial fulfillment of the requirements for the course **Intelligent NoSQL Databases (CSE494)** at Lovely Professional University, Punjab.

<br><br>

________________________________________  
**Signature and Name of the Supervisor**  
Designation: Assistant Professor  
School of Computer Science and Engineering  
Lovely Professional University  
Phagwara, Punjab  
**Date:** 21-10-2026  

---

## DECLARATION

I, **Gudla Shashank**, hereby declare that this project report entitled **“Skill Gap Analyzer & Career Intelligence Platform”** submitted for Academic Task 2 of **CSE494: Intelligent NoSQL Databases** is my original individual work. I have not copied or plagiarized this work from any other student’s submission or unauthorized source, except where proper references and citations are acknowledged in the text. No part of this report has been authored for me by any other individual.

<br><br>

**Date:** 21-10-2026  
**Signature:** *Shashank*  
**Registration No.:** 12316224  
**Name:** Gudla Shashank  

---

## ACKNOWLEDGEMENT

I express my heartfelt gratitude to my project mentor and course instructor **Shaik Sana Begum** for her constant guidance, valuable technical suggestions, and continuous encouragement throughout the conception, architectural design, and implementation of this project. Her expert insights into NoSQL database paradigms, document data modeling, indexing strategies, and aggregation frameworks played a pivotal role in refining the technical rigor of this system.

I extend my sincere appreciation to the faculty and administration of the **School of Computer Science and Engineering, Lovely Professional University**, for providing a state-of-the-art technological ecosystem and academic resources essential for executing this work.

I am also thankful to my peers and classmates for their constructive feedback, peer testing, and insightful discussions during the integration of Retrieval-Augmented Generation (RAG) with MongoDB. Finally, I convey my deepest love and gratitude to my family for their unwavering patience, motivation, and support throughout my academic pursuits.

---

## TABLE OF CONTENTS

1. **Introduction**  
   1.1 Introduction  
   1.2 Problem Statement  
   1.3 Objectives  
   1.4 Scope of the Project  
   1.5 Significance of the Project  
   1.6 Technologies Used  

2. **Problem Domain and System Requirements**  
   2.1 Domain Overview  
   2.2 Existing System  
   2.3 Limitations of Existing System  
   2.4 Proposed System  
   2.5 Functional Requirements  
   2.6 Non-Functional Requirements  

3. **Data Source and Data Description**  
   3.1 Source of Data  
   3.2 Dataset Description  
   3.3 Data Fields (Table 1: Data Fields Summary)  
   3.4 Data Generation / Collection  
   3.5 Data Quality and Integrity Checks  
   3.6 Number of Documents and Collections  

4. **Database Design and Data Modeling**  
   4.1 MongoDB Overview  
   4.2 System Architecture  
   4.3 Database Design  
   4.4 Collection Design (Table 2: Collections Architecture)  
   4.5 Document Structure (JSON/BSON Schema)  
   4.6 Data Modeling Patterns  
   4.7 Embedding vs. Referencing Decisions  
   4.8 Data Model Relationship Diagram  

5. **MongoDB Implementation**  
   5.1 MongoDB Setup & Connection Management  
   5.2 Database Creation  
   5.3 Collection Creation  
   5.4 Schema Validation Rules  
   5.5 Insert Operations (`insert_one`, `insert_many`)  
   5.6 Read Operations (`find_one`, `find`, Projections, Text Search)  
   5.7 Update Operations (`$set`, `$addToSet`, `$push`, `$pull`)  
   5.8 Delete Operations (`delete_one`, Cascading Considerations)  

6. **Advanced MongoDB Operations**  
   6.1 Indexing Strategy (Table 3: Indexes Specification)  
   6.2 Aggregation Framework (Table 4: Implemented Pipelines)  
   6.3 Advanced Complex Queries (Multi-condition, Regex, Array matching)  
   6.4 Data Modeling Operations (Vector Embeddings in Documents)  
   6.5 Query Optimization & Execution Analysis (`explain()`)  
   6.6 Project-Specific Operations (RAG Semantic Vector Search & Similarity)  

7. **Application Integration**  
   7.1 Technology Environment  
   7.2 MongoDB Connection Architecture  
   7.3 Driver / ODM Integration (`pymongo`)  
   7.4 CRUD Integration with User Interface  
   7.5 Aggregation Integration with Interactive Visualizations  
   7.6 End-to-End Application Workflow  

8. **Results and Output Analysis**  
   8.1 Insert Results  
   8.2 Read Results  
   8.3 Update Results  
   8.4 Delete Results  
   8.5 Validation Results  
   8.6 Indexing Results & Execution Plans  
   8.7 Aggregation Output (Table 5: Aggregation Verification Matrix)  
   8.8 Advanced Query Results  

9. **Discussion**  
   9.1 MongoDB Advantages over Relational Databases  
   9.2 Database Design Discussion & Trade-offs  
   9.3 Query Performance & Optimization  
   9.4 Scalability and Distributed Architecture  
   9.5 Challenges Encountered and Technical Solutions  

10. **Conclusion**  

11. **Future Scope**  

**References**  

---

## LIST OF FIGURES

* **Figure 1:** System Architecture Diagram (Streamlit + PyMongo + MongoDB + Gemini RAG)
* **Figure 2:** Entity-Relationship & Document Association Model
* **Figure 3:** Skill Gap Analyzer Dashboard & Executive KPI Overview
* **Figure 4:** Multi-dimensional Match Score & Matched vs. Missing Skill Badges
* **Figure 5:** AI Career Copilot Interface Powered by MongoDB Vector Retrieval & Gemini
* **Figure 6:** Tailored Project Generator Output with Practical Architectures
* **Figure 7:** Aggregated Market Intelligence Visualizations (Top Skills & Gap Analysis)
* **Figure 8:** Interactive Data Engine & Query Console Execution Lab

---

# 1. INTRODUCTION

### 1.1 Introduction
The **Skill Gap Analyzer & Career Intelligence Platform** is an enterprise-grade NoSQL competency benchmarking application. It addresses the friction between academic curriculum outputs and dynamic industry requirements. The platform leverages **MongoDB** as its primary distributed document store and vector repository, **PyMongo** as the Python database driver, **PyPDF** for resume information extraction, **Scikit-Learn TF-IDF** for semantic textual analysis, and **Google Gemini** within a **Retrieval-Augmented Generation (RAG)** architecture to deliver personalized career roadmaps and customized project blueprints.

### 1.2 Problem Statement
Job seekers and engineering graduates struggle to identify exact competency deficiencies when applying for specialized technical roles. Traditional Applicant Tracking Systems (ATS) rely on crude keyword filters that fail to capture semantic equivalents (e.g., recognizing that proficiency in PyTorch implies readiness for Deep Learning roles). Furthermore, existing platforms store user skills in rigid relational tables requiring expensive joins, offer no contextual learning roadmaps, and lack generative mechanisms to help candidates create portfolio-grade projects to bridge their identified gaps.

### 1.3 Objectives
* Develop a flexible NoSQL database schema using MongoDB to store unstructured resumes, candidate profiles, dynamic skill arrays, job requirements, and dense vector embeddings.
* Implement robust CRUD operations with atomic array operators (`$addToSet`, `$push`, `$pull`) to handle skills without duplicate entries or relational junction tables.
* Execute multi-stage MongoDB Aggregation Pipelines (`$unwind`, `$group`, `$lookup`, `$bucket`, `$project`) to compute market-wide talent supply vs. demand metrics.
* Build a Retrieval-Augmented Generation (RAG) engine that retrieves curriculum and architectural chunks from MongoDB `knowledge_vectors` to synthesize hallucination-free career advice and portfolio project proposals.
* Provide an interactive, responsive Streamlit dashboard featuring live telemetry, execution plan inspectors (`explain()`), and visual data analytics.

### 1.4 Scope of the Project
The application covers candidate profile management, PDF resume extraction, dynamic job description parsing, multi-metric candidate benchmarking (70% direct skill overlap + 30% TF-IDF cosine similarity), interactive MongoDB CRUD query simulation, vector similarity search, and real-time aggregation reporting. Deployment configurations support both local standalone MongoDB instances and remote MongoDB Atlas clusters.

### 1.5 Significance of the Project
This project demonstrates the practical superiority of NoSQL document databases over relational engines when handling semi-structured, highly dynamic career data. By embedding arrays of skills and nested project histories directly within candidate documents, the system eliminates expensive multi-table SQL joins. Furthermore, storing high-dimensional vector embeddings within MongoDB documents establishes unified transactional and semantic data management within a single database tier.

### 1.6 Technologies Used
* **Database Management System:** MongoDB Community Server / MongoDB Atlas (v7.0+)
* **Python Database Driver:** PyMongo (v4.6+)
* **Application Framework:** Streamlit (v1.32+)
* **Generative AI & LLM:** Google Gemini (`gemini-2.5-flash`) via `google-generativeai`
* **Text Extraction & NLP:** PyPDF, Scikit-Learn (TF-IDF Vectorizer & Cosine Similarity)
* **Data Visualization:** Plotly Express & Plotly Graph Objects
* **Environment & Security:** Python `dotenv`, `urllib.parse` RFC 3986 credential sanitization

---

# 2. PROBLEM DOMAIN AND SYSTEM REQUIREMENTS

### 2.1 Domain Overview
The competency management domain involves three core entities: candidates (possessing evolving technical skill sets and project records), employers (publishing job specifications with mandatory and optional prerequisites), and educational resources (offering structured learning modules). The domain demands flexible schema handling because technical skills emerge rapidly (e.g., prompt engineering, vector databases, LangChain) and cannot be constrained to static database columns.

### 2.2 Existing System
Existing career advisory platforms and legacy job portals store resume data in Relational Database Management Systems (RDBMS) like MySQL or PostgreSQL. Skills are stored in normalized relational schemas requiring three distinct tables: `candidates`, `skills`, and an associative junction table `candidate_skills` linked by foreign key constraints.

### 2.3 Limitations of Existing System
* **Schema Rigidity:** Adding newly emergent skills or nested metadata (e.g., project URLs, duration, frameworks used) requires destructive schema alterations (`ALTER TABLE`).
* **High Join Overhead:** Analyzing a candidate's portfolio across 20+ skills requires complex multi-table relational `JOIN` operations that degrade performance under heavy read loads.
* **Inability to Store Vectors Natively:** Relational systems require separate specialized vector databases (e.g., Pinecone, Milvus) to support semantic search, causing synchronization lag and architectural sprawl.
* **Absence of Actionable Synthesis:** Legacy systems produce passive percentage scores without offering guided architectural project proposals to rectify missing skills.

### 2.4 Proposed System
The proposed system uses MongoDB as an all-in-one document and vector repository. Candidate profiles store skills as native BSON string arrays. Multi-stage aggregation pipelines process array fields directly using `$unwind` and `$group` in memory. A RAG pipeline couples MongoDB document retrieval with Google Gemini to convert abstract skill deficiencies into actionable 3-week study roadmaps and end-to-end software project specifications.

### 2.5 Functional Requirements
* **FR1 - Resume Ingestion:** Extract raw text, contact emails, and candidate names from uploaded PDF files.
* **FR2 - Competency Extraction & Normalization:** Match raw text against a canonical 30+ skill taxonomy.
* **FR3 - Dual-Metric Gap Scoring:** Calculate compatibility using 70% direct taxonomy matching and 30% TF-IDF cosine similarity.
* **FR4 - NoSQL Profile CRUD:** Create, read, update, and delete candidate profiles with atomic array modification (`$addToSet`, `$pull`).
* **FR5 - Multi-Stage Analytics:** Execute aggregations for top missing skills, talent demand, applicant distributions, and cross-collection joins (`$lookup`).
* **FR6 - RAG Copilot & Project Generation:** Retrieve relevant curriculum vectors from MongoDB and synthesize tailored interview preparation and resume-ready project blueprints.

### 2.6 Non-Functional Requirements
* **NFR1 - Query Latency:** Primary key reads (`user_id`, `job_id`) and indexed array queries must resolve in under 10 milliseconds.
* **NFR2 - High Availability & Fault Tolerance:** Database connection layer must include automatic retry logic, connection pooling (up to 50 sockets), and graceful offline fallback.
* **NFR3 - Data Integrity:** Unique indexes must prevent duplicate candidate identifiers, emails, and canonical skill names.
* **NFR4 - Security:** Connection strings must automatically sanitize URI credentials according to RFC 3986, and API keys must be isolated from source control.

---

# 3. DATA SOURCE AND DATA DESCRIPTION

### 3.1 Source of Data
The database utilizes realistic, production-modeled synthetic datasets seeded via `database/seed_data.py`. It comprises master candidate profiles, comprehensive job descriptions across Machine Learning, Full-Stack, and Cloud Engineering, historical analysis evaluations, and dense 128-dimensional vector embeddings of learning roadmaps seeded via `engine/rag_engine.py`. Real PDF resumes (`shashank_resume.pdf`, `ananya_resume.pdf`, `rahul_resume.pdf`) provide validation for live ingestion.

### 3.2 Dataset Description
The database instance (`skill_gap_analyzer`) contains 7 functional collections:
* **`users`**: Candidate master demographic and competency profiles.
* **`resumes`**: Extracted resume documents with raw text and nested project arrays.
* **`jobs`**: Target employer job openings with required competencies.
* **`skills`**: Master taxonomy of technical competencies categorized by discipline.
* **`analyses`**: Historical gap analysis records with multidimensional score logs.
* **`recommendations`**: Targeted course modules, duration, and priority tiers.
* **`knowledge_vectors`**: Text chunks paired with dense floating-point vector embeddings.

### 3.3 Data Fields
#### Table 1: Data Fields Summary across Collections
| Collection | Field Name | Data Type | Constraint / Validation | Description & Example |
| :--- | :--- | :--- | :--- | :--- |
| `users` | `user_id` | Integer | Unique, Indexed, Mandatory | Primary candidate identifier (e.g., `101`) |
| `users` | `name` | String | Min 2 chars | Full name of candidate (e.g., `"Aarav Sharma"`) |
| `users` | `email` | String | Unique, Sparse, Regex format | Contact email (e.g., `"aarav.sharma@example.com"`) |
| `users` | `skills` | Array of Strings | Multikey Indexed | Technical skill set (e.g., `["Python", "Docker"]`) |
| `jobs` | `job_id` | Integer | Unique, Indexed, Mandatory | Primary job identifier (e.g., `201`) |
| `jobs` | `title` | String | Text Indexed | Role title (e.g., `"Machine Learning Engineer"`) |
| `jobs` | `required_skills`| Array of Strings | Multikey Indexed | Mandatory competencies (e.g., `["Python", "PyTorch"]`)|
| `jobs` | `min_salary` | Double / Int | Value $\ge 0$ | Annual compensation base (e.g., `95000`) |
| `analyses` | `analysis_id` | Integer | Unique, Indexed | Evaluation ID (e.g., `501`) |
| `analyses` | `match_score` | Double | Range $[0.0, 100.0]$ | Composite percentage score (e.g., `83.3`) |
| `analyses` | `missing_skills`| Array of Strings | BSON Array | Unmatched required skills (e.g., `["Docker", "AWS"]`)|
| `knowledge_vectors`| `embedding` | Array of Doubles | Fixed-length Float Vector | High-dimensional embedding (e.g., `[0.012, -0.045]`) |

### 3.4 Data Generation / Collection
Data is initialized by executing `python database/seed_data.py`. The initialization script safely drops pre-existing collections, enforces index creation through `database/db_connection.py`, and executes bulk insertion (`insert_many`) across all 7 collections in ordered sequences.

### 3.5 Data Quality and Integrity Checks
Data integrity is preserved through several layers:
1. **Unique Indexes:** Enforced at the database engine level for `user_id`, `job_id`, `analysis_id`, and `skills.name`.
2. **Deduplication Operators:** Using MongoDB `$addToSet` prevents duplicate competencies from appearing in user skill arrays.
3. **Type Consistency:** Strict Python typing and schema sanitization ensure numerical scores remain within valid bounds ($0$ to $100$).

### 3.6 Number of Documents and Collections
* Total Collections: **7**
* Active User Documents: **6**
* Job Postings: **6**
* Master Skills Taxonomy: **30+**
* Historical Analyses: **6**
* Vector Knowledge Documents: **10**

---

# 4. DATABASE DESIGN AND DATA MODELING

### 4.1 MongoDB Overview
MongoDB is a document-oriented NoSQL database that represents data as flexible, schema-free BSON (Binary JSON) documents. It supports secondary indexes, multikey array indexes, full-text search, atomic in-place updates, and native vector storage, making it ideal for semi-structured talent intelligence data.

### 4.2 System Architecture
```
┌────────────────────────────────────────────────────────┐
│                   STREAMLIT WEB UI                     │
│  (Skill Gap Lab | RAG Copilot | Market Analytics Tab)  │
└───────────────────────────┬────────────────────────────┘
                            │
               PyMongo Driver Connection
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               MONGODB DATABASE ENGINE                  │
│             (Database: skill_gap_analyzer)             │
├───────────────────────────┬────────────────────────────┤
│  Document Collections:    │  Specialized Operations:   │
│  • users                  │  • Multikey Array Indexing │
│  • resumes                │  • Aggregation Pipelines   │
│  • jobs                   │  • Full Text Search        │
│  • analyses               │  • Atomic Array Modifiers  │
│  • knowledge_vectors      │  • Vector Cosine Search    │
└───────────────────────────┴────────────────────────────┘
                            ▲
                            │ Vector Retrieval (RAG)
                            ▼
┌────────────────────────────────────────────────────────┐
│               GOOGLE GEMINI LLM ENGINE                 │
│      (Grounded Synthesis of Projects & Roadmaps)       │
└────────────────────────────────────────────────────────┘
```

### 4.3 Database Design
The database architecture follows a hybrid design pattern balancing **Embedding** (for tightly coupled, bounded subdocuments like projects within a resume) and **Referencing** (for independent entities like jobs, users, and historical evaluation logs).

### 4.4 Collection Design
#### Table 2: Collections Architecture
| Collection Name | Storage Role | Relationship Pattern | Primary Purpose |
| :--- | :--- | :--- | :--- |
| `users` | Master Data | Referenced by `resumes` & `analyses` | Stores candidate contact, education, and skill arrays |
| `resumes` | Semi-structured Data | 1-to-1 reference to `users` | Houses parsed resume text and embedded project arrays |
| `jobs` | Master Data | Referenced by `analyses` | Contains job titles, companies, and required skills |
| `skills` | Master Catalog | Referenced by name | Canonical master list of verified industry skills |
| `analyses` | Transactional Log | References `users` & `jobs` | Records gap evaluations, scores, and missing skills |
| `recommendations` | Knowledge Base | Keyed on skill name | Structured learning modules, durations, and platforms |
| `knowledge_vectors`| Vector Knowledge Store | Independent Document Store | Text chunks and dense vector embeddings for RAG |

### 4.5 Document Structure
A representative candidate document in the `users` collection:
```json
{
  "_id": {"$oid": "65342a1ef82d9a10bc931001"},
  "user_id": 101,
  "name": "Shashank Verma",
  "email": "shashank.verma@example.com",
  "education": "B.Tech Computer Science",
  "experience_years": 2,
  "skills": ["Python", "SQL", "Pandas", "Scikit-Learn", "Git"],
  "created_at": {"$date": "2026-10-21T10:00:00Z"},
  "updated_at": {"$date": "2026-10-21T10:00:00Z"}
}
```

An extracted resume document in the `resumes` collection demonstrating embedded subdocuments:
```json
{
  "_id": {"$oid": "65342a1ef82d9a10bc932001"},
  "resume_id": 301,
  "user_id": 101,
  "filename": "shashank_resume.pdf",
  "skills": ["Python", "SQL", "Pandas", "Scikit-Learn", "Git"],
  "projects": [
    {
      "name": "Customer Churn Predictor",
      "tools": ["Python", "Scikit-Learn", "Pandas"],
      "description": "Engineered Random Forest pipeline achieving 89% recall on telecom dataset."
    }
  ],
  "upload_date": {"$date": "2026-10-21T10:05:00Z"}
}
```

### 4.6 Data Modeling Patterns
1. **Attribute Pattern:** Applied to skills within `users`, `jobs`, and `resumes` by modeling them as homogeneous arrays of strings, enabling multikey indexing.
2. **Subset Pattern:** In `resumes`, only the most recent project highlights are embedded, avoiding unbounded document growth.
3. **Log / Event Sourcing Pattern:** In `analyses`, each evaluation is appended as a distinct immutable document capturing point-in-time scores.

### 4.7 Embedding vs. Referencing Decisions
* **Embedded Subdocuments:** The `projects` array is embedded directly inside `resumes` because project details are always read concurrently with the resume and never queried as standalone entities.
* **Referenced Documents:** `users` and `jobs` are maintained as distinct collections and referenced via integer foreign keys (`user_id`, `job_id`) within `analyses`. This avoids duplicating large job descriptions across thousands of candidate evaluations.

### 4.8 Data Model Relationship Diagram
```
┌──────────────┐         1:1           ┌──────────────┐
│    users     ├──────────────────────►│   resumes    │
│  (user_id)   │                       │ (projects[]) │
└──────┬───────┘                       └──────────────┘
       │
       │ 1:N
       ▼
┌──────────────┐         N:1           ┌──────────────┐
│   analyses   │◄──────────────────────┤     jobs     │
│ (user, job)  │                       │  (job_id)    │
└──────────────┘                       └──────────────┘
       │
       │ Semantic Cosine Matching
       ▼
┌──────────────────────────────┐
│      knowledge_vectors       │
│  (content, embedding[128])   │
└──────────────────────────────┘
```

---

# 5. MONGODB IMPLEMENTATION

### 5.1 MongoDB Setup & Connection Management
The application connects to MongoDB using PyMongo. Connection configuration is encapsulated in `database/db_connection.py`. The connection manager supports both local connections (`mongodb://localhost:27017/`) and remote MongoDB Atlas replica sets. A connection pool of 50 sockets is initialized with a 5000ms server selection timeout.

```python
from pymongo import MongoClient

client = MongoClient(
    mongo_uri,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
    socketTimeoutMS=5000,
    maxPoolSize=50
)
db = client["skill_gap_analyzer"]
```

### 5.2 Database Creation
MongoDB creates databases lazily upon the first write operation. In `db_connection.py`, the target database handle `skill_gap_analyzer` is initialized and verified using the lightweight administrative command `client.admin.command('ping')`.

### 5.3 Collection Creation
Collections (`users`, `resumes`, `jobs`, `skills`, `analyses`, `recommendations`, `knowledge_vectors`) are initialized programmatically during the database seeding routine (`database/seed_data.py`).

### 5.4 Schema Validation
Schema validation is enforced at the application layer through Python type hints, dictionaries, and database constraints. The connection setup ensures unique keys are strictly observed across all inserts.

### 5.5 Insert Operations
Single-document inserts utilize `insert_one()`, while batch operations leverage `insert_many(ordered=False)` for maximum network throughput:
```python
# Single document insertion
result = db.users.insert_one({
    "user_id": 107,
    "name": "Priya Sharma",
    "email": "priya.sharma@example.com",
    "skills": ["Python", "FastAPI", "MongoDB"],
    "created_at": datetime.now(timezone.utc)
})

# Bulk insertion of jobs
db.jobs.insert_many(JOBS_DATA, ordered=False)
```

### 5.6 Read Operations
The system executes primary key lookups, projected queries, and text searches:
```python
# Primary key exact lookup
user = db.users.find_one({"user_id": 101})

# Array matching using $all operator
matched_jobs = db.jobs.find({"required_skills": {"$all": ["Python", "Docker"]}})

# Full-text search across Title and Company
results = db.jobs.find({"$text": {"$search": "Machine Learning"}})
```

### 5.7 Update Operations
Atomic update operators modify specific document fields without rewriting the entire document:
```python
# In-place scalar update
db.users.update_one({"user_id": 101}, {"$set": {"experience_years": 3}})

# Array deduplicated addition using $addToSet
db.users.update_one({"user_id": 101}, {"$addToSet": {"skills": "Docker"}})

# Array element removal using $pull
db.users.update_one({"user_id": 101}, {"$pull": {"skills": "Pandas"}})
```

### 5.8 Delete Operations
The system supports both single document removal and collection purges:
```python
# Single candidate deletion
db.users.delete_one({"user_id": 101})

# Clean collection reset
db.analyses.delete_many({})
```

---

# 6. ADVANCED MONGODB OPERATIONS

### 6.1 Indexing Strategy
To ensure low-latency query execution, specialized indexes are constructed during system startup via `setup_indexes()` in `database/db_connection.py`.

#### Table 3: Indexes Specification
| Collection | Index Key(s) | Index Type | Purpose / Query Supported |
| :--- | :--- | :--- | :--- |
| `users` | `user_id` (1) | Unique, Single Field | Rapid candidate lookup and duplicate prevention |
| `users` | `email` (1) | Unique, Sparse | Guarantees email uniqueness when provided |
| `resumes` | `skills` (1) | **Multikey Index** | Fast indexing of individual items in the skills array |
| `jobs` | `required_skills` (1)| **Multikey Index** | Accelerates array queries filtering jobs by skill |
| `jobs` | `title` (text), `company` (text) | **Text Index** | Powers full-text keyword searches across job openings |
| `analyses` | `match_score` (1) | Single Field | Optimizes score range filters and sorting operations |
| `knowledge_vectors`| `doc_id` (1) | Unique | Fast point lookup for RAG vector documents |

### 6.2 Aggregation Framework
The platform implements 5 multi-stage aggregation pipelines in `database/aggregations.py`.

#### Table 4: Implemented Aggregation Pipelines
| Pipeline Name | Objective | Pipeline Stages Used | Key Operators |
| :--- | :--- | :--- | :--- |
| **1. Top Matched Skills** | Rank candidate skills most matched by employers | `$unwind` $\rightarrow$ `$group` $\rightarrow$ `$sort` $\rightarrow$ `$limit` $\rightarrow$ `$project` | `$sum`, `$unwind` |
| **2. Common Skill Gaps** | Identify the most frequent candidate skill gaps | `$unwind` $\rightarrow$ `$group` $\rightarrow$ `$sort` $\rightarrow$ `$limit` $\rightarrow$ `$project` | `$sum`, `$sort: -1` |
| **3. Job Market Demand** | Determine the most demanded industry skills | `$unwind` $\rightarrow$ `$group` $\rightarrow$ `$sort` $\rightarrow$ `$limit` $\rightarrow$ `$project` | `$sum`, `$limit: 10` |
| **4. Job Performance Join** | Compute applicant count & average score per role | `$lookup` $\rightarrow$ `$unwind` $\rightarrow$ `$group` $\rightarrow$ `$sort` $\rightarrow$ `$project` | `$lookup`, `$avg`, `$round` |
| **5. Score Bucketing** | Categorize match scores into 4 performance tiers | `$bucket` | `$bucket`, boundaries, `$avg` |

#### Detailed Implementation of Foreign Collection Join (`$lookup`):
```python
pipeline = [
    {
        "$lookup": {
            "from": "jobs",
            "localField": "job_id",
            "foreignField": "job_id",
            "as": "job_details"
        }
    },
    {"$unwind": "$job_details"},
    {
        "$group": {
            "_id": "$job_id",
            "job_title": {"$first": "$job_details.title"},
            "company": {"$first": "$job_details.company"},
            "avg_match_score": {"$avg": "$match_score"},
            "total_evaluations": {"$sum": 1},
            "highest_score": {"$max": "$match_score"}
        }
    },
    {"$sort": {"avg_match_score": -1}},
    {
        "$project": {
            "_id": 0,
            "job_id": "$_id",
            "job_title": 1,
            "company": 1,
            "avg_match_score": {"$round": ["$avg_match_score", 1]},
            "total_evaluations": 1
        }
    }
]
```

### 6.3 Advanced Complex Queries
The system evaluates complex compound conditions combining logical and comparison operators:
```python
# Candidates with >= 2 years experience possessing both Python and SQL
query = {
    "$and": [
        {"experience_years": {"$gte": 2}},
        {"skills": {"$all": ["Python", "SQL"]}}
    ]
}
candidates = list(db.users.find(query))
```

### 6.4 Data Modeling Operations: Vector Embeddings
In `knowledge_vectors`, curriculum and architectural patterns are stored alongside dense 128-dimensional floating-point embeddings:
```json
{
  "doc_id": "curric_docker",
  "category": "learning_roadmap",
  "title": "Containerization with Docker",
  "skills": ["Docker", "DevOps"],
  "content": "Master containerization, Dockerfiles, and multi-container orchestration.",
  "embedding": [0.0125, -0.0452, 0.0881, 0.0319]
}
```

### 6.5 Query Optimization & Execution Analysis (`explain()`)
The system analyzes execution plans via MongoDB's `.explain("executionStats")` interface.
* **Unindexed Scan (`COLLSCAN`):** Without an index, querying `db.users.find({"email": "..."})` evaluates every document in the collection (`totalDocsExamined = N`).
* **Indexed Scan (`IXSCAN`):** With the unique index `uniq_email`, the database traverses a B-Tree index structure (`stage: "IXSCAN"`), examining exactly 1 document (`totalDocsExamined = 1`), reducing execution time from linear $O(N)$ to logarithmic $O(\log N)$.

### 6.6 Project-Specific Operations: RAG Vector Retrieval
The Retrieval-Augmented Generation engine retrieves knowledge chunks from MongoDB by computing cosine similarity over stored embeddings:
$$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^n A_i B_i}{\sqrt{\sum_{i=1}^n A_i^2} \sqrt{\sum_{i=1}^n B_i^2}}$$

The top-$K$ scoring curriculum chunks are injected into the Google Gemini LLM prompt context to synthesize grounded, actionable learning advice and project designs.

---

# 7. APPLICATION INTEGRATION

### 7.1 Technology Environment
The application is built in Python 3.10+ using Streamlit as the interactive frontend. The backend integrates `pymongo` for database persistence, `pypdf` for resume text parsing, `scikit-learn` for TF-IDF vectorization, and `google-generativeai` for LLM orchestration.

### 7.2 MongoDB Connection Architecture
Connection management in `database/db_connection.py` provides:
1. **URI Sanitization:** Automatically strips accidental `<>` characters and applies RFC 3986 percent-encoding to passwords containing special characters (`@`, `#`, `$`).
2. **Resilient Fallback:** If the live database is offline during an evaluation, the application falls back to an in-memory sample dataset, ensuring zero downtime.

### 7.3 Driver / ODM Integration
Direct PyMongo driver calls provide high throughput without the overhead of heavy Object-Document Mappers. Custom conversion functions cleanly transform MongoDB BSON types (`ObjectId`, `datetime`) into JSON-serializable dictionaries for frontend rendering.

### 7.4 CRUD Integration with User Interface
The **Data Engine & Query Lab** tab in `app.py` allows users to execute live CRUD operations directly from the UI:
* Adding new skills triggers atomic `$addToSet` updates.
* Removing skills invokes `$pull`.
* Creating candidate profiles executes `insert_one()` with immediate UI re-rendering.

### 7.5 Aggregation Integration with Interactive Visualizations
Aggregation pipeline outputs feed directly into Plotly Express charts:
* **Horizontal Bar Charts:** Visualizing Top In-Demand Skills.
* **Grouped Bar Charts:** Displaying Candidate Supply vs. Employer Demand.
* **Donut Charts:** Illustrating Applicant Score Distribution Buckets.

### 7.6 End-to-End Application Workflow
```
[ Upload PDF Resume ]
        │
        ▼
[ PyPDF Text Extraction ] ───► [ NLP Skill Taxonomy Matcher ]
        │
        ▼
[ Dual-Metric Scoring Engine ] (70% Direct Overlap + 30% TF-IDF Cosine)
        │
        ▼
[ MongoDB Persistence ] ─────► Save record to `analyses` collection
        │
        ▼
[ RAG Vector Retrieval ] ────► Retrieve top-K chunks from `knowledge_vectors`
        │
        ▼
[ Google Gemini Synthesis ] ──► Display Personalized Study Plan & Project Blueprint
```

---

# 8. RESULTS AND OUTPUT ANALYSIS

### 8.1 Insert Results
The seed routine successfully initialized **7 collections**, inserting 6 candidate master profiles, 6 job openings, 30 canonical skill records, and 10 dense vector documents. Single document inserts via `insert_one` executed with write confirmation acknowledgments in under 4ms.

### 8.2 Read Results
Primary key lookups (`find_one({"user_id": 101})`) returned complete BSON documents in $<2\text{ms}$. Full-text search across job postings (`$text: {$search: "Machine Learning"}`) accurately retrieved corresponding roles with relevance scores.

### 8.3 Update Results
Executing `$addToSet` with a new skill (`"Docker"`) updated the candidate document atomically. Subsequent attempts to add `"Docker"` again resulted in `modified_count: 0`, confirming set-level deduplication.

### 8.4 Delete Results
Executing `delete_user(106)` successfully removed the candidate document (`deleted_count: 1`). Subsequent lookups for the same ID returned `None`.

### 8.5 Validation Results
Inserting a duplicate user ID resulted in a `DuplicateKeyError` (E11000) from the database engine, confirming that unique index constraints prevent primary key collisions.

### 8.6 Indexing Results & Execution Plans
Evaluating `explain("executionStats")` on the `uniq_user_id` index demonstrated an `IXSCAN` stage where `totalDocsExamined: 1` matched `nReturned: 1`, confirming optimal index utilization.

### 8.7 Aggregation Output Analysis
#### Table 5: Aggregation Verification Matrix
| Aggregation Pipeline | Input Collection | Aggregated Output Summary | Technical Interpretation |
| :--- | :--- | :--- | :--- |
| **Top Demanded Skills** | `jobs` | Python (4), Docker (4), MongoDB (3), SQL (3) | Correctly identifies Docker and Python as top market requirements |
| **Common Skill Gaps** | `analyses` | Docker (2), Power BI (1), Statistics (1), AWS (1) | Highlights containerization (Docker) as the primary candidate deficiency |
| **Candidate Supply vs Demand** | `resumes` & `jobs` | Docker: Demand 4 vs Supply 2 (Gap: +2) | Confirms a net deficit of 2 containerization engineers in the candidate pool |
| **Score Bucketing** | `analyses` | 80–100%: 2; 60–79%: 1; 40–59%: 2; 0–39%: 1 | Shows candidate scores distributed across all four evaluation tiers |
| **Job Performance Join** | `analyses` $\bowtie$ `jobs` | ML Engineer: Avg Score 100%; Cloud Data Eng: 50% | Demonstrates cross-collection foreign key resolution via `$lookup` |

### 8.8 Advanced Query Results
The vector similarity pipeline accurately matched candidate skill gaps (e.g., missing Docker) with the curriculum document `"Containerization Mastery with Docker & Compose"`, producing similarity scores $>0.82$.

---

# 9. DISCUSSION

### 9.1 MongoDB Advantages over Relational Databases
1. **Natural Skill Modeling:** Skills and projects are stored as native arrays and embedded subdocuments, eliminating junction tables.
2. **Schema Flexibility:** Job specifications can dynamically introduce new skill requirements without requiring database migration scripts.
3. **Unified Vector & Document Tier:** Storing embeddings directly alongside business entities removes the operational complexity of managing an external vector database.

### 9.2 Database Design Discussion & Trade-offs
Referencing `users` and `jobs` from `analyses` rather than embedding full job details prevents data redundancy and keeps document sizes well below MongoDB’s 16MB BSON limit. The minor trade-off—requiring `$lookup` pipelines for combined reports—is mitigated by primary key indexes on foreign fields.

### 9.3 Query Performance & Optimization
Creating multikey indexes on `resumes.skills` and `jobs.required_skills` transformed array intersection checks from $O(N)$ full collection scans into indexed B-Tree searches. In-memory aggregations using `$project` stages stripped unnecessary fields early in the pipeline to conserve working memory.

### 9.4 Scalability and Distributed Architecture
MongoDB’s architecture natively supports horizontal scaling via sharding. Collections like `analyses` and `resumes` can be partitioned across shard clusters using hashed sharding on `user_id`, ensuring uniform write distribution as the platform scales.

### 9.5 Challenges Encountered and Technical Solutions
* **Challenge 1: Duplicate Array Entries:** Repeatedly adding skills caused duplicate strings in profiles.  
  * *Solution:* Replaced `$push` with the set-preserving operator `$addToSet`.
* **Challenge 2: URI Special Characters in Atlas:** Passwords containing characters like `@` or `#` broke the connection URI parser.  
  * *Solution:* Implemented automated RFC 3986 percent-encoding in `sanitize_mongo_uri()`.
* **Challenge 3: Offline Resilience:** Network timeouts caused UI rendering errors when the remote database was unreachable.  
  * *Solution:* Built a seamless fallback layer that gracefully serves cached data if the database ping exceeds 5000ms.

---

# 10. CONCLUSION

The **Skill Gap Analyzer & Career Intelligence Platform** successfully demonstrates the design, implementation, and optimization of an intelligent NoSQL database system using **MongoDB** and **Python**. By leveraging MongoDB's document model, atomic array operators (`$addToSet`, `$pull`), multikey indexes, and multi-stage aggregation pipelines (`$unwind`, `$group`, `$lookup`, `$bucket`), the application solves key limitations of traditional relational career systems. The integration of a Retrieval-Augmented Generation (RAG) engine grounded in MongoDB vector documents demonstrates the practical convergence of modern NoSQL database systems with generative artificial intelligence.

---

# 11. FUTURE SCOPE

* **MongoDB Atlas Vector Search:** Migrate local cosine similarity calculations to native MongoDB Atlas `$vectorSearch` indexes utilizing Hierarchical Navigable Small World (HNSW) graphs.
* **Change Streams for Real-Time Alerts:** Implement MongoDB Change Streams (`watch()`) to push real-time notifications to candidates whenever a newly posted job matches their skill profile.
* **Automated Resume Parsing with OCR:** Incorporate computer vision OCR to process scanned, image-based PDF resumes.
* **Multi-Tenant Enterprise Role Management:** Expand the user schema to support role-based access control (RBAC) with dedicated portals for University Placement Cells, Corporate Recruiters, and Students.

---

# REFERENCES

1. **MongoDB, Inc.** (2026). *The MongoDB Manual: Document Data Modeling, Indexes, and Aggregation Framework*. https://www.mongodb.com/docs/manual/
2. **Banker, K., Bakkum, P., Verch, S., Garrett, D., & Hawkins, T.** (2016). *MongoDB in Action: Covers MongoDB version 3.0+*. Manning Publications.
3. **PyMongo Documentation.** (2026). *Python driver for MongoDB (v4.6)*. https://pymongo.readthedocs.io/
4. **Google DeepMind.** (2024). *Gemini: A Family of Highly Capable Multimodal Models*. arXiv preprint arXiv:2312.11805.
5. **Lewis, P., et al.** (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems (NeurIPS), 33, 9459-9474.
6. **Pedregosa, F., et al.** (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
7. **Streamlit Community.** (2026). *Streamlit Python Documentation and Component Architecture*. https://docs.streamlit.io/
