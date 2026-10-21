# 🗄️ MongoDB & PyMongo Viva Guide

This guide is specifically designed for your **NoSQL / MongoDB course viva and practical evaluation**. When your professor asks: *"What is the role of MongoDB in your project?"*, this guide gives you the exact technical justification, live code examples, and aggregation pipeline explanations.

---

## 🎯 1. High-Level Justification: Why MongoDB Instead of SQL?

| Feature | Relational Database (SQL) | MongoDB (NoSQL Document Store) |
| :--- | :--- | :--- |
| **Data Structure** | Rigid tables, fixed schema, columns | Semi-structured BSON documents with dynamic fields |
| **Array of Skills** | Requires a separate junction table (`candidate_skills`) with foreign keys & heavy `JOIN` operations | Native array data type (`"skills": ["Python", "SQL", "MongoDB"]`) |
| **Nested Projects** | Requires 1-to-N normalized tables | Embedded subdocuments directly inside candidate/resume documents |
| **Array Operations** | Difficult to modify arrays without multiple INSERT/DELETEs | Native array modifiers: `$push`, `$pull`, `$addToSet` |
| **Skill Aggregation** | Multi-table `JOIN`, `GROUP BY`, slow on large text data | Fast in-memory pipelines using `$unwind` and `$group` |

---

## 🏗️ 2. Database & Collection Design

**Database Name:** `skill_gap_analyzer`

### Collections:
1. **`users`**: Candidate master profiles (id, name, email, education, skills array)
2. **`resumes`**: Extracted resume data (resume_id, parsed_name, skills, nested projects array)
3. **`jobs`**: Job postings (job_id, title, company, experience_years, required_skills array)
4. **`skills`**: Master taxonomy catalog of 30+ canonical industry skills categorized
5. **`analyses`**: Evaluation records storing matched skills, missing skills, match score, semantic score
6. **`recommendations`**: Curated learning roadmap for each skill (course title, platform, hours, priority)

---

## ⚡ 3. PyMongo Operations Implemented & Where to Show Them

### 3.1 Connection & Client Setup (`database/db_connection.py`)
```python
from pymongo import MongoClient

# MongoClient with connection pooling and timeouts
client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=4000,
    maxPoolSize=50
)
db = client["skill_gap_analyzer"]
```

### 3.2 Indexes for Performance & Data Integrity (`database/db_connection.py`)
```python
# Unique Index: Prevents duplicate user IDs
db.users.create_index([("user_id", 1)], unique=True)

# Multikey Index: Optimizes querying skills inside arrays
db.resumes.create_index([("skills", 1)])
db.jobs.create_index([("required_skills", 1)])

# Text Index: Enables full-text search across job titles and companies
db.jobs.create_index([("title", "text"), ("company", "text")])
```

---

## 🔄 4. CRUD Operations Walkthrough

### 4.1 Create (`insert_one`, `insert_many`)
```python
# Single document insert:
db.users.insert_one({
    "user_id": 101,
    "name": "Shashank",
    "email": "student@example.com",
    "education": {"degree": "B.Tech", "branch": "CSE"},
    "skills": ["Python", "SQL", "MongoDB"]
})

# Bulk insert:
db.jobs.insert_many([job_1, job_2, job_3], ordered=False)
```

### 4.2 Read (`find_one`, `find`)
```python
# Query single candidate:
user = db.users.find_one({"user_id": 101})

# Query with comparison operators ($gte, $lte, $and):
experienced_jobs = db.jobs.find({
    "$and": [
        {"experience_years": {"$gte": 2}},
        {"experience_years": {"$lte": 5}}
    ]
})
```

### 4.3 Update with Array Modifiers (`$addToSet`, `$push`, `$pull`)
**Teacher Favorite Question:** *"What is the difference between `$push` and `$addToSet`?"*

- **`$push`**: Appends an element to the array regardless of whether it is already present (can create duplicates).
- **`$addToSet`**: Adds an element to the array **only if it does not already exist**, maintaining a distinct set of skills.

```python
# 1. Add skill without duplicates ($addToSet)
db.users.update_one(
    {"user_id": 101},
    {"$addToSet": {"skills": "Docker"}}
)

# 2. Append skill ($push)
db.users.update_one(
    {"user_id": 101},
    {"$push": {"skills": "Docker"}}
)

# 3. Remove skill from array ($pull)
db.users.update_one(
    {"user_id": 101},
    {"$pull": {"skills": "Docker"}}
)
```

### 4.4 Delete (`delete_one`, `delete_many`)
```python
# Delete single candidate:
db.users.delete_one({"user_id": 101})

# Delete multiple obsolete records:
db.analyses.delete_many({"match_score": {"$lt": 20.0}})
```

---

## 🔎 5. Query Operators Demonstrated

| Operator | Meaning | Example in Project |
| :--- | :--- | :--- |
| `$in` | Matches any value in array | `db.jobs.find({"required_skills": {"$in": ["Python", "SQL"]}})` |
| `$all` | Matches documents containing all items | `db.jobs.find({"required_skills": {"$all": ["Python", "MongoDB"]}})` |
| `$gte` | Greater than or equal | `db.analyses.find({"match_score": {"$gte": 70}})` |
| `$lte` | Less than or equal | `db.jobs.find({"experience_years": {"$lte": 3}})` |
| `$and` | Logical AND | Combined experience criteria |
| `$or` | Logical OR | Full-text title or company search |
| `$exists` | Key existence check | `db.analyses.find({"missing_skills": {"$exists": True}})` |

---

## 📊 6. MongoDB Aggregation Pipelines

### Pipeline 1: Most Common Missing Skills (Skill Gap Analysis)
**Purpose:** Finds which skills candidates lack most frequently across all evaluations.
```python
pipeline = [
    # Step 1: Flatten the missing_skills array into individual documents
    {"$unwind": "$missing_skills"},
    
    # Step 2: Group by skill name and count occurrences
    {
        "$group": {
            "_id": "$missing_skills",
            "count": {"$sum": 1}
        }
    },
    
    # Step 3: Sort in descending order of frequency
    {"$sort": {"count": -1}},
    
    # Step 4: Limit to top 5
    {"$limit": 5}
]
results = list(db.analyses.aggregate(pipeline))
```

### Pipeline 2: Most Demanded Job Skills
**Purpose:** Aggregates market demand across all job openings.
```python
pipeline = [
    {"$unwind": "$required_skills"},
    {
        "$group": {
            "_id": "$required_skills",
            "demand_count": {"$sum": 1}
        }
    },
    {"$sort": {"demand_count": -1}}
]
results = list(db.jobs.aggregate(pipeline))
```

### Pipeline 3: Job Match Leaderboard with `$lookup` (Foreign Join)
**Purpose:** Joins `analyses` collection with `jobs` collection to show average match scores per role.
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

## 💡 7. Fast Viva Questions & Answers

### Q1: What is BSON in MongoDB?
**Answer:** BSON stands for Binary JSON. It is the binary representation of JSON documents that MongoDB uses to store data. BSON extends JSON with additional data types like `ObjectId`, `Date`, and binary data.

### Q2: What is the purpose of the multikey index?
**Answer:** A multikey index is created on a field that contains an array (like `skills: ["Python", "SQL"]`). MongoDB creates an index entry for every single element in the array, making queries like `find({"skills": "Python"})` fast (`O(log N)`).

### Q3: What is the difference between embedded documents and normalized references?
**Answer:**
- Embedded documents store related data inside the same document (e.g. `education: {"degree": "B.Tech", "branch": "CSE"}`). This provides atomic reads and eliminates the need for joins.
- Normalized references store `user_id` or `job_id` and link collections using `$lookup` when data size grows large or relationships are many-to-many.

### Q4: How does your project run if MongoDB is running locally?
**Answer:** The project connects to `mongodb://localhost:27017/` using PyMongo's `MongoClient`. The application automatically checks connection health with `admin.command('ping')` and displays the live MongoDB version in the sidebar.
