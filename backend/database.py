import sqlite3
import pandas as pd

DB_NAME = "cyber_history.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prediction TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_prediction(prediction):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO prediction_history(prediction) VALUES(?)",
        (prediction,)
    )

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM prediction_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows