### SQL Query Generator

Convert plain English questions into SQL queries using an LLM — no SQL knowledge required.

Type something like *"show me all students who failed"* and the app writes the SQL for you, runs it on a real database, and displays the results.


## What It Does

- Takes a natural language question as input
- Sends it to an LLM (Llama 3 via Groq API) along with the database schema
- Gets back a valid SQL query
- Runs the query on a local SQLite database
- Displays both the generated SQL and the actual results


## Project Structure

```
sql-query-generator/
│
├── database/
│   └── school.db          # SQLite database with sample school data
│
├── backend/
│   └── main.py            # FastAPI server
│
├── frontend/
│   └── index.html         # Simple web interface
│
├── .env                   # API keys (not committed to git)
├── .gitignore
└── README.md
```

---

##  Tech Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3 (via Groq API) |
| Backend | Python, FastAPI |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOURUSERNAME/sql-query-generator.git
cd sql-query-generator
```

### 2. Install dependencies

```bash
pip3 install fastapi uvicorn groq python-dotenv
```

### 3. Set up your API key

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com)

### 4. Run the backend

```bash
cd backend
uvicorn main:app --reload
```

### 5. Open the frontend

Open `frontend/index.html` in your browser and start querying!

---

##  Sample Database

The app comes with a sample school database containing:

- `students` — id, name, age, email
- `courses` — id, name, credits
- `grades` — student_id, course_id, grade

### Example queries you can try

- *"Show all students"*
- *"Which students scored above 80?"*
- *"List all courses and their credits"*
- *"Who got the highest grade in Math?"*

---

##  Future Work

- Fine-tune an open source model (CodeLlama) using QLoRA on text-to-SQL datasets for a fully self-hosted solution
- Support for uploading custom database schemas
- Query history and saved queries
- Support for more complex multi-table queries

---
