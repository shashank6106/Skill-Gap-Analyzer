# 🗄️ MongoDB, PyMongo & RAG Viva Guide

This guide is specifically designed for your **NoSQL / MongoDB course viva and practical evaluation**. When your professor asks: *"What is the role of MongoDB in your project and how is RAG integrated?"*, this guide gives you the exact technical justification, live code examples, and aggregation pipeline explanations.

---

## 🎯 1. High-Level Justification: Why MongoDB Instead of SQL?

| Feature | Relational Database (SQL) | MongoDB (NoSQL Document Store) |
| :--- | :--- | :--- |
| **Data Structure** | Rigid tables, fixed schema, columns | Semi-structured BSON documents with dynamic fields |
| **Array of Skills** | Requires a separate junction table (`candidate_skills`) with foreign keys & heavy `JOIN` operations | Native array data type (`"skills": ["Python", "SQL", "MongoDB"]`) |
| **Nested Projects** | Requires 1-to-N normalized tables | Embedded subdocuments directly inside candidate/resume documents |
| **Vector Embeddings (RAG)** | Requires external specialized vector database | Stores vector embeddings (`[0.021, -0.41, ...]`) directly alongside text chunks in MongoDB documents |
| **Array Operations** | Difficult to modify arrays without multiple INSERT/DELETEs | Native array modifiers: `$push`, `$pull`, `$addToSet` |
| **Skill Aggregation** | Multi-table `JOIN`, `GROUP BY`, slow on large text data | Fast in-memory pipelines using `$unwind` and `$group` |

---

## 🧬 2. How RAG (Retrieval-Augmented Generation) Uses MongoDB

### The 3 Stages of RAG in our Project:

```
User Query / Resume Gaps
        │
        ▼
1. RETRIEVE ────→ Query MongoDB collection: `knowledge_vectors`
        │         Find top-K semantically relevant curriculum modules & project patterns
        │         using vector cosine similarity.
        ▼
2. AUGMENT  ────→ Inject Candidate Profile + Job Requirements + Retrieved MongoDB Chunks
        │         into Google Gemini LLM Prompt.
        ▼
3. GENERATE ────→ Generates grounded, hallucination-free Career Advice & 
                  Personalized Portfolio Projects to bridge missing skills!
```

### Document Structure in `knowledge_vectors` Collection:
```json
{
  "doc_id": "curric_docker",
  "category": "learning_roadmap",
  "title": "Containerization Mastery with Docker & Compose",
  "skills": ["Docker", "Linux", "DevOps"],
  "content": "Learn Docker architecture, container lifecycles, and docker-compose...",
  "embedding": [0.0125, -0.0452, 0.0881, "... 128 to 768 dimensions ..."]
}
```

---

## 🏗️ 3. Database & Collection Design

**Database Name:** `skill_gap_analyzer`

### Active Collections:
1. **`users`**: Candidate master profiles (id, name, email, education, skills array)
2. **`resumes`**: Extracted resume data (resume_id, parsed_name, skills, nested projects array)
3. **`jobs`**: Job postings (job_id, title, company, experience_years, required_skills array)
4. **`skills`**: Master taxonomy catalog of 30+ canonical industry skills categorized
5. **`analyses`**: Evaluation records storing matched skills, missing skills, match score, semantic score
6. **`recommendations`**: Curated learning roadmap for each skill (course title, platform, hours, priority)
7. **`knowledge_vectors`**: Dense vector embeddings of curriculum, jobs, and project architectures for RAG retrieval

---

## ⚡ 4. PyMongo Operations Implemented

### 4.1 Connection & Indexing (`database/db_connection.py`)
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=4000)
db = client["skill_gap_analyzer"]

# Multikey Index on array fields:
db.resumes.create_index([("skills", 1)])
db.jobs.create_index([("required_skills", 1)])

# Vector Knowledge collection index:
db.knowledge_vectors.create_index([("doc_id", 1)], unique=True)
db.knowledge_vectors.create_index([("category", 1)])
```

### 4.2 CRUD Operations
- **Insert:** `db.users.insert_one({...})` / `db.jobs.insert_many([...])`
- **Read:** `db.users.find_one({"user_id": 101})`
- **Update with $set (Atomic Fields & ATS Bullets):**
  ```python
  # Persist optimized resume bullets to user document:
  db.users.update_one(
      {"user_id": 101},
      {"$set": {"optimized_bullets": bullets_list, "bullets_updated_at": datetime.utcnow()}}
  )
  ```
- **Update with Array Deduplication:**
  ```python
  # $addToSet prevents duplicate skills:
  db.users.update_one(
      {"user_id": 101},
      {"$addToSet": {"skills": "Docker"}}
  )
  ```
- **Update with Array Removal:**
  ```python
  db.users.update_one(
      {"user_id": 101},
      {"$pull": {"skills": "Docker"}}
  )
  ```
- **Delete:** `db.users.delete_one({"user_id": 101})`

---

## 📊 5. MongoDB Aggregation Pipelines

### Pipeline 1: Most Common Missing Skills (Skill Gap Analysis)
```python
pipeline = [
    # 1. Deconstruct missing_skills array into individual records
    {"$unwind": "$missing_skills"},
    # 2. Group by skill name and sum occurrences
    {
        "$group": {
            "_id": "$missing_skills",
            "count": {"$sum": 1}
        }
    },
    # 3. Order by frequency descending
    {"$sort": {"count": -1}},
    {"$limit": 5}
]
results = list(db.analyses.aggregate(pipeline))
```

### Pipeline 2: Job Match Leaderboard with `$lookup` (Foreign Join)
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
            "avg_score": {"$avg": "$match_score"},
            "total_applicants": {"$sum": 1}
        }
    },
    {"$sort": {"avg_score": -1}}
]
results = list(db.analyses.aggregate(pipeline))
```

---

## 💡 6. Essential Viva Questions & Answers

### Q1: What makes this project a RAG (Retrieval-Augmented Generation) system?
**Answer:**
Standard LLMs hallucinate or give generic advice. In our project:
1. **Retrieval:** When a candidate asks a question or requests a project, our engine searches the MongoDB `knowledge_vectors` collection for the most relevant curriculum and project architecture chunks.
2. **Augmentation:** The retrieved MongoDB chunks, along with the candidate's exact resume and missing skills, are fed into the prompt context.
3. **Generation:** Google Gemini generates a grounded, personalized career roadmap and resume bullet points tailored to their specific situation.

### Q2: What is the difference between $push and $addToSet?
**Answer:**
- `$push`: Always appends the element to the array, potentially causing duplicate skills.
- `$addToSet`: Adds the element **only if it does not already exist**, maintaining a unique mathematical set of skills in the candidate profile.

### Q3: What does the $unwind stage do in MongoDB?
**Answer:**
`$unwind` deconstructs an array field from input documents to output a document for each element in the array. This allows subsequent aggregation stages like `$group` to aggregate and count individual skills across the entire database.
