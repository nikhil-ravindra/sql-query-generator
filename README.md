### SQL Query Generator

## Core Features & Problem Statement

In a typical enterprise ecosystem, business units (Product, Sales, Finance) constantly require database insights to drive critical decision-making. However, accessing this data introduces an operational bottleneck: it relies on data engineers or backend developers to manually interpret requirements and write SQL code. This introduces latency in business loops and drains expensive engineering resources on mundane, repetitive tasks.


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


