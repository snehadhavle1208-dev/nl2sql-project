# 🧠 NL2SQL Chatbot using Vanna AI 2.0 + FastAPI

## 📌 Project Overview

This project implements an AI-powered Natural Language to SQL (NL2SQL) system using **Vanna AI 2.0** and **FastAPI**.  
Users can ask questions in plain English, and the system converts them into SQL queries, executes them on a SQLite database, and returns results.

The system follows a hybrid approach:
- AI-based SQL generation (Vanna Agent)
- Rule-based fallback for reliability

---

## 🚀 Features

- Convert natural language questions → SQL queries
- Execute queries on SQLite database
- Return structured results (columns + rows)
- SQL validation for safety (only SELECT allowed)
- Hybrid fallback system for guaranteed responses
- Pre-seeded memory for improved accuracy
- REST API using FastAPI
- Interactive API docs via Swagger UI

---

## 🏗️ Architecture
User Query (English)
↓
FastAPI Backend (/chat)
↓
Vanna AI Agent (LLM + Tools + Memory)
↓
SQL Generation
↓
SQL Validation (Safe queries only)
↓
SQLite Execution
↓
Response (JSON)


---

## 🛠️ Tech Stack

| Technology | Purpose |
|----------|--------|
| Python 3.10+ | Backend language |
| Vanna AI 2.0 | NL2SQL agent |
| FastAPI | REST API |
| SQLite | Database |
| Gemini API | LLM provider |
| Pandas | Data handling |
| Plotly | Visualization (optional) |

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-link>
cd nl2sql_project
```

### Create Virtual Environment

python -m venv venv
venv\Scripts\activate   # Windows

### Install Dependencies
pip install -r requirements.txt

### Set API Key
Create .env file:
GOOGLE_API_KEY=your_api_key_here

### Create Database
python setup_database.py

### Seed Memory
python seed_memory.py

### Run Server
uvicorn main:app --reload

🌐 API Usage

Open Swagger UI:

👉 http://127.0.0.1:8000/docs


### POST /chat
Request:

{
  "question": "How many patients do we have?"
}

Response:
{
  "question": "...",
  "sql": "SELECT COUNT(*) FROM patients",
  "columns": ["COUNT(*)"],
  "rows": [[200]]
}

### GET /health
{
  "status": "ok",
  "message": "API running"
}


### 🧪 Testing

The system was tested using 20 predefined questions covering:

Basic queries
Aggregations
Joins
Time-based queries

Results are documented in RESULTS.md.



### ⚠️ Challenges Faced
Vanna API version differences caused integration issues
ToolRegistry and Agent initialization varied across versions
Streaming responses required async handling
Memory API differed (text-based vs structured)


### 🎯Conclusion

This project successfully demonstrates a working NL2SQL system using Vanna AI and FastAPI.
A hybrid AI + rule-based approach ensures both flexibility and reliability.


### NOTE 
Due to Vanna version inconsistencies, a hybrid fallback approach was implemented to ensure system reliability.

Due to version differences in the installed Vanna 2.0 package, the ToolRegistry API was not consistent (register/register_tool methods were unavailable).

To ensure a fully working system, I implemented a compatible approach by directly passing tools via AgentConfig.

All required components (RunSqlTool, VisualizeDataTool, DemoAgentMemory, etc.) are correctly used, and the system works end-to-end as expected.