# =============================================================================
# backend/main.py
# AI-Powered Text-to-SQL Engine — FastAPI Application Server
# =============================================================================

import os
import sqlite3
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI(
    title="Text-to-SQL Engine",
    description="Translates natural language queries into executable SQL via Groq LLM",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_SCHEMA = """
You are an expert SQL query generator. You have access to a SQLite database
with the following schema:

TABLE: students
  - student_id   INTEGER PRIMARY KEY AUTOINCREMENT
  - name         TEXT NOT NULL
  - email        TEXT UNIQUE NOT NULL
  - enrollment_year INTEGER

TABLE: grades
  - grade_id     INTEGER PRIMARY KEY AUTOINCREMENT
  - student_id   INTEGER (FOREIGN KEY → students.student_id)
  - course_name  TEXT NOT NULL
  - score        REAL
  - grade_letter TEXT

RELATIONSHIP: grades.student_id references students.student_id (many-to-one)

RULES YOU MUST FOLLOW:
1. Return ONLY the raw SQL query — no markdown, no explanation, no backticks.
2. Always use valid SQLite syntax.
3. For JOIN queries, use students.student_id = grades.student_id.
4. Never use DROP, DELETE, INSERT, UPDATE, or any data-mutation statements.
5. If the question cannot be answered with this schema, return exactly: ERROR: Cannot generate query.
"""

class QueryRequest(BaseModel):
    question: str

def execute_sql_query(sql: str) -> list[dict]:
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "school.db")

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.post("/query")
async def generate_and_execute_query(request: QueryRequest):
    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": DATABASE_SCHEMA
                },
                {
                    "role": "user",
                    "content": request.question
                }
            ],
            temperature=0.1,
            max_tokens=500,
        )

        raw_llm_output = chat_completion.choices[0].message.content.strip()

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"LLM inference layer failed: {str(e)}"
        )

    if raw_llm_output.startswith("ERROR:"):
        raise HTTPException(
            status_code=400,
            detail=f"LLM could not generate a valid query: {raw_llm_output}"
        )

    sql_upper = raw_llm_output.upper()
    forbidden_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "CREATE"]

    for keyword in forbidden_keywords:
        if keyword in sql_upper:
            raise HTTPException(
                status_code=400,
                detail=f"Security policy violation: query contains forbidden keyword '{keyword}'"
            )

    try:
        results = execute_sql_query(raw_llm_output)

    except sqlite3.OperationalError as e:
        raise HTTPException(
            status_code=422,
            detail=f"SQL execution failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database layer error: {str(e)}"
        )

    return {
        "question": request.question,
        "generated_sql": raw_llm_output,
        "results": results,
        "row_count": len(results)
    }

@app.get("/")
async def health_check():
    return {"status": "online", "service": "Text-to-SQL Engine", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)