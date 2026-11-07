"""SQLite storage for the expense tracker."""
import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).parent / "expenses.db"

DEFAULT_CATEGORIES = [
    "Food & Groceries",
    "Rent & Housing",
    "Transport",
    "Utilities",
    "Shopping",
    "Health",
    "Entertainment",
    "Education",
    "Travel",
    "Other",
]

# Currency code -> (symbol, name). Add more here if you need them.
CURRENCIES = {
    "INR": ("₹", "Indian Rupee"),
    "USD": ("$", "US Dollar"),
    "EUR": ("€", "Euro"),
    "GBP": ("£", "British Pound"),
    "JPY": ("¥", "Japanese Yen"),
    "AUD": ("A$", "Australian Dollar"),
    "CAD": ("C$", "Canadian Dollar"),
    "SGD": ("S$", "Singapore Dollar"),
    "AED": ("AED ", "UAE Dirham"),
    "CHF": ("CHF ", "Swiss Franc"),
    "CNY": ("CN¥", "Chinese Yuan"),
}
DEFAULT_CURRENCY = "INR"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount > 0),
                currency TEXT NOT NULL DEFAULT '{DEFAULT_CURRENCY}',
                note TEXT
            )
            """
        )
        # Upgrade databases created by the earlier version (no currency column).
        columns = {row[1] for row in conn.execute("PRAGMA table_info(expenses)")}
        if "currency" not in columns:
            conn.execute(
                f"ALTER TABLE expenses ADD COLUMN currency TEXT NOT NULL DEFAULT '{DEFAULT_CURRENCY}'"
            )


def add_expense(expense_date: date, category: str, amount: float, currency: str, note: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO expenses (expense_date, category, amount, currency, note) VALUES (?, ?, ?, ?, ?)",
            (expense_date.isoformat(), category.strip(), float(amount), currency, note.strip()),
        )


def delete_expense(expense_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (int(expense_id),))


def get_expenses(
    start: date | None = None,
    end: date | None = None,
    currency: str | None = None,
) -> pd.DataFrame:
    query = "SELECT id, expense_date, category, amount, currency, note FROM expenses"
    conditions, params = [], []
    if start and end:
        conditions.append("expense_date BETWEEN ? AND ?")
        params += [start.isoformat(), end.isoformat()]
    if currency:
        conditions.append("currency = ?")
        params.append(currency)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY expense_date DESC, id DESC"

    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params)

    df["expense_date"] = pd.to_datetime(df["expense_date"]).dt.date
    return df


def get_categories() -> list[str]:
    """Default categories plus any custom ones the user has logged."""
    with get_connection() as conn:
        rows = conn.execute("SELECT DISTINCT category FROM expenses").fetchall()
    custom = sorted({r[0] for r in rows} - set(DEFAULT_CATEGORIES))
    return DEFAULT_CATEGORIES + custom


def get_used_currencies() -> list[str]:
    """Currencies that have at least one expense, most used first."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT currency FROM expenses GROUP BY currency ORDER BY COUNT(*) DESC"
        ).fetchall()
    return [r[0] for r in rows]
