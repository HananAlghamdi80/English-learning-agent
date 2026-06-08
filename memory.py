import sqlite3
from datetime import datetime

DB_NAME = "learner_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        level TEXT,
        goal TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner_name TEXT,
        mode TEXT,
        user_message TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_learner(name, level, goal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO learners (name, level, goal) VALUES (?, ?, ?)",
        (name, level, goal)
    )

    conn.commit()
    conn.close()


def save_session(learner_name, mode, user_message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sessions (learner_name, mode, user_message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (learner_name, mode, user_message, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def get_session_count(learner_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM sessions WHERE learner_name = ?",
        (learner_name,)
    )

    count = cursor.fetchone()[0]
    conn.close()

    return count


def get_last_mode(learner_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT mode FROM sessions
        WHERE learner_name = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (learner_name,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else "No practice yet"


def get_recent_sessions(learner_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT mode, user_message, created_at
        FROM sessions
        WHERE learner_name = ?
        ORDER BY id DESC
        LIMIT 5
        """,
        (learner_name,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows