import sqlite3
from flask import current_app

def get_connection():
    db_name = current_app.config.get("DB_NAME", "tasks.db")
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        due_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        duration_minutes INTEGER NOT NULL DEFAULT 60,
        effort_level TEXT NOT NULL DEFAULT 'Medium',
        start_after TEXT,
        category TEXT NOT NULL DEFAULT 'General'
    )
    """)

    conn.commit()
    conn.close()