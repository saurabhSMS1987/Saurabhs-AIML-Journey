# Takeaways: Advanced Python: Logging, pytest and MySQL

*Nov 4, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Python Advanced: Logging, PyTest, Pydantic – Takeaways* from the **[Codebasics.io](https://codebasics.io) Advanced Python course**.

My one-page recap of the fourth Advanced Python module, kept handy for quick revision. The PDF's title also mentions Pydantic, but its pages cover logging, pytest and MySQL.

## Logging

- Python's `logging` module has five severity levels: **DEBUG, INFO, WARNING, ERROR and CRITICAL**.
- Set it up quickly with `logging.basicConfig()`, or build custom **loggers, handlers and formatters** for finer control.
- Logs track what an application does, a better tool than `print()` for debugging and understanding the flow.
- Handlers send logs to different destinations: the **console**, a **file** or a **remote server**.
- Good logging supports **audit trails** and compliance, and is essential for troubleshooting in production.

## Automated testing with pytest

- pytest handles both simple unit tests and complex functional tests.
- Any function named **`test_...`** is found and run automatically.
- **Fixtures** handle setup and teardown, such as preparing shared test data.
- **Test discovery** finds tests across many files and folders, which keeps large test suites manageable.
- **Plugins** add parallel testing, coverage reports and more, supporting test-driven development (TDD).

## Working with MySQL in Python

- Libraries such as **`mysql-connector-python`** and **`pymysql`** connect to MySQL, run queries and handle transactions.
- A connection needs **host, database name, user and password**. Keep credentials out of the code, for example in environment variables.
- A **cursor** runs `SELECT`, `INSERT`, `UPDATE` and `DELETE` commands and returns the results.
- Always **close cursors and connections** to free resources and prevent data leaks.

## All together

```python
import logging
import sqlite3                                       # same pattern as MySQL; built into Python

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def unapproved_manual_count(db_path):
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM gl WHERE source = ? AND approver IS NULL", ("Manual",))
        count = cursor.fetchone()[0]
        logging.info("Unapproved manual entries: %d", count)
        return count
    finally:
        connection.close()                           # always close the connection

def test_unapproved_manual_count(tmp_path):          # tmp_path is a built-in pytest fixture
    db = tmp_path / "gl.db"
    with sqlite3.connect(db) as con:
        con.execute("CREATE TABLE gl (je_id TEXT, source TEXT, approver TEXT)")
        con.executemany("INSERT INTO gl VALUES (?, ?, ?)",
                        [("JE1", "Manual", None), ("JE2", "Manual", "K. Wong"), ("JE3", "Automated", None)])
    assert unapproved_manual_count(db) == 1
```
