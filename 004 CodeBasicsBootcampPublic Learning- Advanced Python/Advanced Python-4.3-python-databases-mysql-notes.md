# Working with Databases from Python (MySQL): My Notes

*Nov 4, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Database Helper with MySQL** lecture from **Code Basics**. The runnable audit examples use Python's built-in [`sqlite3` module](https://docs.python.org/3/library/sqlite3.html) and [`contextlib`](https://docs.python.org/3/library/contextlib.html), so they work without a MySQL server. **Database credentials are masked in these notes.**

## Where I started

Most client data doesn't live in CSV files. It lives in **databases**: ERP systems, billing platforms and general ledgers. This lecture built a small helper file, `db_helper.py`, that connects Python to a MySQL database for an **expense manager** app, and reads, adds and deletes expense records. The interesting part wasn't the SQL itself, but how to open and close connections safely every time.

## The code in brief

`db_helper.py` works with an `expense_manager` database containing an `expenses` table with `expense_date`, `amount`, `category` and `notes` columns. It has one helper and four functions:

| Function | SQL | What it does |
| --- | --- | --- |
| `get_db_cursor(commit=False)` | n/a | Opens a connection, hands back a cursor and closes everything afterwards |
| `fetch_all_records()` | `SELECT * FROM expenses` | Reads every expense |
| `fetch_expenses_for_date(date)` | `SELECT ... WHERE expense_date = %s` | Reads one day's expenses |
| `insert_expense(date, amount, category, notes)` | `INSERT INTO expenses ...` | Adds an expense, such as ₹300 on Food for Panipuri |
| `delete_expenses_for_date(date)` | `DELETE FROM expenses WHERE ...` | Removes one day's expenses |

## What I learnt

**Connecting with `mysql.connector`:** the connection details are host, user, password and database name. The password is masked here, and should never be written into code:

```python
import os
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],      # masked: the lecture file hardcoded it
    database="expense_manager",
)
cursor = connection.cursor(dictionary=True)  # each row comes back as a dict: {'amount': 300, ...}
```

**A context manager for the connection.** The `@contextmanager` decorator plus `yield` (both from earlier lectures) wrap opening and closing into one reusable block:

```python
from contextlib import contextmanager

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(...)
    cursor = connection.cursor(dictionary=True)
    yield cursor                    # the code inside the "with" block runs here
    if commit:
        connection.commit()         # save changes, but only for inserts and deletes
    cursor.close()
    connection.close()

with get_db_cursor() as cursor:
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
```

**Parameterised queries:** values are passed separately with `%s` placeholders, never pasted into the SQL text:

```python
cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
```

This protects against **SQL injection**, where a malicious value rewrites the query, and handles quotes and dates correctly. Note the trailing comma in `(expense_date,)`: the parameters must be a tuple, even when there's only one.

**Reads vs writes:** `SELECT` needs no commit. `INSERT`, `UPDATE` and `DELETE` only take effect after `connection.commit()`, which is why the helper takes `commit=True` for those.

**One improvement worth making:** if a query fails inside the `with` block, the lecture's helper never reaches its closing lines, so the connection stays open. Wrapping the `yield` in `try` / `finally` guarantees the clean-up, as the first audit snippet shows.

## How this shows up in financial statement audit work

Querying a client's database, or a copy of it, directly is often faster and more complete than asking for exports. These snippets use Python's built-in SQLite, so they run anywhere. With MySQL, the only changes are the connection line and the placeholder (`%s` instead of `?`).

**1. A safer context manager: always close, and roll back on error.**

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_cursor(db_path, commit=False):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row          # rows behave like dicts, like dictionary=True
    cursor = connection.cursor()
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception:
        connection.rollback()                     # undo partial changes if anything fails
        raise
    finally:
        cursor.close()                            # always runs, error or not
        connection.close()
```

**2. Loading a sample general ledger table.** In practice, this would be the client's database, or a copy provided for the audit:

```python
with get_cursor("audit_copy.db", commit=True) as cur:
    cur.execute("DROP TABLE IF EXISTS gl")
    cur.execute("CREATE TABLE gl (je_id TEXT, posting_date TEXT, account TEXT, amount REAL, source TEXT, approver TEXT)")
    cur.executemany("INSERT INTO gl VALUES (?, ?, ?, ?, ?, ?)", [
        ("JE01", "2026-12-28", "4000", -12_500, "Automated", "SYSTEM"),
        ("JE01", "2026-12-28", "1200",  12_500, "Automated", "SYSTEM"),
        ("JE02", "2026-12-31", "4000", -250_000, "Manual", None),
        ("JE02", "2026-12-31", "1200",  250_000, "Manual", None),
        ("JE03", "2027-01-02", "4000", -8_400, "Automated", "SYSTEM"),
        ("JE03", "2027-01-02", "1200",  8_400, "Automated", "SYSTEM"),
    ])
```

**3. Parameterised audit queries.** The test values (period end, threshold) are parameters, so the same query can be re-run for any client or year:

```python
period_end, threshold = "2026-12-31", 100_000

with get_cursor("audit_copy.db") as cur:
    cur.execute("""
        SELECT je_id, posting_date, ABS(amount) AS amount
        FROM gl
        WHERE source = 'Manual' AND approver IS NULL AND ABS(amount) > ? AND amount > 0
    """, (threshold,))
    print([dict(r) for r in cur.fetchall()])
    # [{'je_id': 'JE02', 'posting_date': '2026-12-31', 'amount': 250000.0}]: large, manual and unapproved

    cur.execute("SELECT account, ROUND(SUM(amount), 2) AS balance FROM gl WHERE posting_date <= ? GROUP BY account", (period_end,))
    print({r["account"]: r["balance"] for r in cur.fetchall()})
    # {'1200': 262500.0, '4000': -262500.0}: the year-end trial balance, built by SQL
```

**4. Why parameters matter: the injection risk.** A value pasted into the SQL text can change the query's meaning entirely:

```python
user_input = "2026-12-31' OR '1'='1"

with get_cursor("audit_copy.db") as cur:
    cur.execute(f"SELECT COUNT(*) FROM gl WHERE posting_date = '{user_input}'")    # unsafe: text pasted in
    print(cur.fetchone()[0])                                                       # 6: every row returned
    cur.execute("SELECT COUNT(*) FROM gl WHERE posting_date = ?", (user_input,))   # safe: a parameter
    print(cur.fetchone()[0])                                                       # 0: treated as plain text
```

**5. Read-only access for audit work.** An auditor should never be able to change client data. Opening the database read-only enforces that in code. With MySQL, the equivalent is a database user granted only `SELECT`:

```python
read_only = sqlite3.connect("file:audit_copy.db?mode=ro", uri=True)
try:
    read_only.execute("DELETE FROM gl")
except sqlite3.OperationalError as e:
    print("Blocked:", e)                       # Blocked: attempt to write a readonly database
finally:
    read_only.close()
```

## My reflection

The context manager was the idea that tied the earlier lectures together: decorators and `yield` turned out to have a very practical use. Every database connection is opened, used and closed in one predictable pattern, so I never have to remember to clean up.

Two habits I'm taking straight into audit work. First, **parameterised queries**, so a test is re-runnable for any period and can't be broken by an odd value. Second, **read-only access**. The lecture's helper can insert and delete, which suits an app developer, but an auditor's connection to client data should be able to look and never touch. And credentials belong in environment variables, never in a file that might end up on GitHub.
