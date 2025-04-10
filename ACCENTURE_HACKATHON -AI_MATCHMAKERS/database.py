# database.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('job_screening.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            raw_jd TEXT,
            summary_json TEXT,
            created_at TEXT
        )
    ''')
    # Candidates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            resume_text TEXT,
            extracted_json TEXT,
            match_score REAL,
            shortlisted INTEGER DEFAULT 0,
            email TEXT,
            created_at TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(id)
        )
    ''')


    conn.commit()
    conn.close()
