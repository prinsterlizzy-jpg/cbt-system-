import sqlite3
from database import connect
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import random

def verify_user(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT password, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    hashed, role = row
    if check_password_hash(hashed, password):
        return {"username": username, "role": role}
    return None

def add_user(username, password, role='student'):
    conn = connect()
    cur = conn.cursor()
    hashed = generate_password_hash(password)
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, hashed, role))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def add_question(question, o1, o2, o3, o4, answer):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO questions (question, option1, option2, option3, option4, answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question, o1, o2, o3, o4, answer))
    conn.commit()
    conn.close()

def get_all_questions():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, question, option1, option2, option3, option4 FROM questions")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_question_by_id(qid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, question, option1, option2, option3, option4 FROM questions WHERE id=?", (qid,))
    row = cur.fetchone()
    conn.close()
    return row

def get_answer(qid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT answer FROM questions WHERE id=?", (qid,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def save_result(username, score, total):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO results (username, score, total) VALUES (?, ?, ?)", (username, score, total))
    conn.commit()
    conn.close()

def get_results_for_user(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, score, total, timestamp FROM results WHERE username=? ORDER BY timestamp DESC", (username,))
    rows = cur.fetchall()
    conn.close()
    return rows

def create_exam_session(username, duration_seconds):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM questions")
    ids = [str(r[0]) for r in cur.fetchall()]
    random.shuffle(ids)
    order = ",".join(ids)
    exam_id = str(uuid.uuid4())
    cur.execute("INSERT INTO exams (exam_id, username, question_order, duration) VALUES (?, ?, ?, ?)",
                (exam_id, username, order, duration_seconds))
    conn.commit()
    conn.close()
    return exam_id, ids

def get_exam_session(exam_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT exam_id, username, question_order, duration, created_at FROM exams WHERE exam_id=?", (exam_id,))
    row = cur.fetchone()
    conn.close()
    return row
