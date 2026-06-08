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


##  Tech Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3 (via Groq API) |
| Backend | Python, FastAPI |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |


##  Future Work

- Fine-tune an open source model (CodeLlama) using QLoRA on text-to-SQL datasets for a fully self-hosted solution
- Support for uploading custom database schemas
- Query history and saved queries
- Support for more complex multi-table queries


