"""
database/seed.py
Run this to create and populate school.db with sample data.
"""

import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "school.db")

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            student_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            email           TEXT UNIQUE NOT NULL,
            enrollment_year INTEGER
        );

        CREATE TABLE IF NOT EXISTS grades (
            grade_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id   INTEGER NOT NULL,
            course_name  TEXT NOT NULL,
            score        REAL,
            grade_letter TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );
    """)

    # Seed students
    students = [
        ("Alice Sharma",   "alice@school.com",   2022),
        ("Bob Mendes",     "bob@school.com",      2021),
        ("Clara Zhou",     "clara@school.com",    2023),
        ("David Okafor",   "david@school.com",    2022),
        ("Eva Petrov",     "eva@school.com",      2021),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO students (name, email, enrollment_year) VALUES (?, ?, ?)",
        students
    )

    # Seed grades
    grades = [
        (1, "Mathematics",  92.0, "A"),
        (1, "Physics",      85.5, "B"),
        (2, "Mathematics",  47.0, "F"),
        (2, "Chemistry",    61.0, "C"),
        (3, "Mathematics",  78.0, "B"),
        (3, "Biology",      95.0, "A"),
        (4, "Physics",      43.0, "F"),
        (4, "Mathematics",  55.0, "D"),
        (5, "Chemistry",    88.0, "B"),
        (5, "Biology",      91.5, "A"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO grades (student_id, course_name, score, grade_letter) VALUES (?, ?, ?, ?)",
        grades
    )

    conn.commit()
    print(f" Database seeded successfully at: {db_path}")
    print(f"   → {len(students)} students | {len(grades)} grade records")