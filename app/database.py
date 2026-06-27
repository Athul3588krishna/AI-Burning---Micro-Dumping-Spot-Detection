import sqlite3
from app.config import DATABASE_PATH


def create_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id TEXT,
            detection_type TEXT,
            confidence REAL,
            timestamp TEXT,
            image_path TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_violation(camera_id, detection_type, confidence, timestamp, image_path):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO violations
        (camera_id,detection_type,confidence,timestamp,image_path)
        VALUES (?,?,?,?,?)
    """, (
        camera_id,
        detection_type,
        confidence,
        timestamp,
        image_path
    ))

    conn.commit()
    conn.close()


def get_all_violations():

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