import sqlite3
from calendar import monthrange
from datetime import date
from pathlib import Path

from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    db.commit()
    db.close()


def seed_db():
    db = get_db()
    already_seeded = db.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"] > 0
    if already_seeded:
        db.close()
        return

    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    today = date.today()
    last_day = monthrange(today.year, today.month)[1]

    def d(day):
        return date(today.year, today.month, min(day, last_day)).isoformat()

    db.executemany(
        """
        INSERT INTO expenses (user_id, category, amount, date, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (user_id, "Food", 850.00, d(2), "Groceries"),
            (user_id, "Transport", 450.00, d(4), "Fuel"),
            (user_id, "Bills", 3200.00, d(6), "Electricity bill"),
            (user_id, "Health", 1200.00, d(9), "Pharmacy visit"),
            (user_id, "Entertainment", 600.00, d(12), "Movie night"),
            (user_id, "Shopping", 2100.00, d(16), "New shoes"),
            (user_id, "Other", 300.00, d(20), "Miscellaneous"),
            (user_id, "Food", 540.00, d(24), "Restaurant dinner"),
        ],
    )
    db.commit()
    db.close()
