import os
import sqlite3
from app.config import DATABASE_PATH


def create_database():
    """
    Creates the violations SQLite database and table if they do not exist.
    """
    # Ensure logs directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            violation_type TEXT,
            confidence REAL,
            timestamp TEXT,
            screenshot_path TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def insert_violation(filename, violation_type, confidence, timestamp, screenshot_path, status='Pending'):
    """
    Inserts a new violation record.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO violations
        (filename, violation_type, confidence, timestamp, screenshot_path, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        filename,
        violation_type,
        confidence,
        timestamp,
        screenshot_path,
        status
    ))

    conn.commit()
    conn.close()


def get_all_violations():
    """
    Retrieves all logged violations, ordered by ID descending.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM violations
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def update_violation_status(violation_id, status):
    """
    Updates the status of a specific violation (e.g., Pending, Resolved, Spurious).
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE violations
        SET status = ?
        WHERE id = ?
    """, (status, violation_id))

    conn.commit()
    conn.close()


def delete_violation(violation_id):
    """
    Deletes a specific violation by ID.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM violations
        WHERE id = ?
    """, (violation_id,))

    conn.commit()
    conn.close()