import sqlite3
from werkzeug.security import generate_password_hash

DB = "cbt.db"

def connect():
    return sqlite3.connect(DB, check_same_thread=False)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        exam_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        question_order TEXT NOT NULL, -- comma-separated question ids
        duration INTEGER NOT NULL, -- seconds
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # default admin
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", generate_password_hash("admin123"), "admin"))

    cur.execute("SELECT * FROM users WHERE username='student'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("student", generate_password_hash("student123"), "student"))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
