import sqlite3
from flask import current_app
from werkzeug.security import generate_password_hash
#Ariticial Intelligence was used to ORGANIZE Our NOTES, FIX BUGS, and WORK WITH INDENTATION ISSUES

# Purpose:
# This file sets up and manages the SQLite database schema


def get_connection():
    # Establish SQLite connection
    db_name = current_app.config.get("DB_NAME", "tasks.db")
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def seed_test_user():

    conn = get_connection()

    cursor = conn.cursor()

    email = "testuser@email.com"

    password_hash = generate_password_hash("securepass123")

    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))

    existing_user = cursor.fetchone()

    if not existing_user:

        cursor.execute("""

            INSERT INTO users (email, password_hash)

            VALUES (?, ?)

        """, (email, password_hash))

    conn.commit()

    conn.close()


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------------
    # Create table (fresh installs)
    # -------------------------------
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
        category TEXT NOT NULL DEFAULT 'General',
        group_name TEXT,
        description TEXT,
        notes TEXT
    )
    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        user_id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT NOT NULL UNIQUE,

        password_hash TEXT NOT NULL,

        failed_attempts INTEGER NOT NULL DEFAULT 0,

        lock_until TEXT

    )

    """)

    # -------------------------------
    # Migration (existing databases)
    # -------------------------------
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in cursor.fetchall()]

    if "start_after" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN start_after TEXT")

    if "description" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN description TEXT")

    if "notes" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN notes TEXT")

    if "group_name" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN group_name TEXT")

    conn.commit()
    conn.close()
    seed_test_user()