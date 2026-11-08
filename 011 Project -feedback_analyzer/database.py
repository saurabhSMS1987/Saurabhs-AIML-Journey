"""
All the database work lives here (SQLite).

Learning source: CodeBasics.io
Keeping the database code in its own file makes app.py shorter and easier to read.
"""
import os
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

# The database file sits next to this code (or wherever FEEDBACK_DB points).
DB_FILE = os.getenv("FEEDBACK_DB") or str(Path(__file__).parent / "feedback.db")

COLUMNS = ["id", "saved_at", "batch", "review", "label", "score", "theme", "suggestion"]


def connect():
    return closing(sqlite3.connect(DB_FILE))


def init_db():
    """Create the feedback table the first time, and add new columns to older databases."""
    with connect() as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                review TEXT,
                label TEXT,
                score INTEGER,
                theme TEXT
            )
        """)
        existing = {row[1] for row in conn.execute("PRAGMA table_info(feedback)")}
        for column, kind in [("suggestion", "TEXT DEFAULT ''"), ("saved_at", "TEXT"), ("batch", "TEXT")]:
            if column not in existing:
                conn.execute(f"ALTER TABLE feedback ADD COLUMN {column} {kind}")


def save_results(results, batch: str = "") -> int:
    """Write analyzed reviews into the database. Rows that failed analysis are skipped.

    Returns how many rows were saved.
    """
    rows = [r for r in results if r.get("label") != "error"]
    saved_at = datetime.now().isoformat(timespec="seconds")
    with connect() as conn, conn:
        conn.executemany(
            "INSERT INTO feedback (saved_at, batch, review, label, score, theme, suggestion) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            [(saved_at, batch.strip(), r["review"], r["label"], r["score"], r["theme"], r.get("suggestion", ""))
             for r in rows],
        )
    return len(rows)


def load_history() -> list[dict]:
    """Read every saved review, newest first."""
    with connect() as conn:
        rows = conn.execute(f"SELECT {', '.join(COLUMNS)} FROM feedback ORDER BY id DESC").fetchall()
    return [dict(zip(COLUMNS, row)) for row in rows]


def delete_all() -> int:
    """Remove every saved review. Returns how many were deleted."""
    with connect() as conn, conn:
        return conn.execute("DELETE FROM feedback").rowcount
