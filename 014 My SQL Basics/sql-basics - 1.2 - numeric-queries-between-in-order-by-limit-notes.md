# SQL Basics: Numeric Queries with BETWEEN, IN, ORDER BY, LIMIT and OFFSET: My Notes

*Nov 9, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SQL Basics: Data Retrieval – Single Table** course, chapter **"Retrieve data using numeric query (BETWEEN, IN, ORDER BY, LIMIT, OFFSET)"**, from **[Codebasics.io](https://codebasics.io)**. The audit examples run on SQLite through Python's built-in `sqlite3` module, and the same SQL works in MySQL.

## Where I started

The first chapter filtered rows by **text**. This one filtered by **numbers**: ratings above a value, ranges, lists of years, missing values, and finally **sorting** and taking the top few rows. These are the building blocks of nearly every journal entry test I run, such as amounts over a threshold, entries inside a cut-off window, and the largest items for testing.

## The data in brief

The same **movies** table as before, this time focusing on its numeric columns: `imdb_rating` (some missing for unreleased films) and `release_year`.

## What I learnt

**Comparisons and ranges:**

```sql
SELECT * FROM movies WHERE imdb_rating > 9;

SELECT * FROM movies WHERE imdb_rating >= 6 AND imdb_rating <= 8;
SELECT * FROM movies WHERE imdb_rating BETWEEN 6 AND 8;        -- same result, shorter

SELECT * FROM movies WHERE release_year = 2018 OR release_year = 2019 OR release_year = 2022;
SELECT * FROM movies WHERE release_year IN (2018, 2019, 2022);  -- same result, shorter
```

| Tool | Meaning | Note |
| --- | --- | --- |
| `<`, `<=`, `>`, `>=`, `=`, `!=` | Compare with a value | |
| `AND`, `OR` | Combine conditions | Use brackets when mixing them |
| `BETWEEN a AND b` | From `a` to `b` | **Includes both ends** |
| `IN (x, y, z)` | Equals any value in the list | Replaces a chain of `OR`s |

**Missing values:**

```sql
SELECT * FROM movies WHERE imdb_rating IS NULL;       -- not yet rated
SELECT * FROM movies WHERE imdb_rating IS NOT NULL;   -- rated
```

`NULL` means "unknown", so `imdb_rating = NULL` never matches anything. It must be `IS NULL`.

**Sorting and taking the top rows:**

```sql
SELECT * FROM movies WHERE industry = 'Bollywood' ORDER BY imdb_rating ASC;            -- lowest first (ASC is the default)
SELECT * FROM movies WHERE industry = 'Bollywood' ORDER BY imdb_rating DESC LIMIT 5;   -- the top 5
SELECT * FROM movies WHERE industry = 'Bollywood' ORDER BY imdb_rating DESC LIMIT 5 OFFSET 1;   -- skip 1, take 5: ranks 2 to 6
```

| Clause | What it does |
| --- | --- |
| `ORDER BY col` | Sorts rows, ascending by default |
| `ORDER BY col DESC` | Sorts largest first |
| `LIMIT n` | Keeps only the first `n` rows |
| `OFFSET k` | Skips the first `k` rows before `LIMIT` applies |

**Two details worth knowing:**

- **`NULL`s and sorting:** in MySQL, `NULL` ratings sort **first** in ascending order, so filter them out with `IS NOT NULL` when ranking.
- **Ties:** if two rows share the same value, `LIMIT` can cut between them unpredictably. Adding a second sort column, as in `ORDER BY imdb_rating DESC, title`, keeps the results repeatable.

## How this shows up in financial statement audit work

Thresholds, ranges, account lists, cut-off windows and "the largest N items" are the everyday language of journal entry testing. These snippets build a small sample table so they run anywhere.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE journal_entries (je_id TEXT, posted_at TEXT, account TEXT, amount REAL, source TEXT, approver TEXT);
INSERT INTO journal_entries VALUES
 ('JE001','2026-12-28 10:15','4000', 12500,'Automated','SYSTEM'),
 ('JE002','2026-12-31 22:40','4000',250000,'Manual', NULL),
 ('JE003','2026-12-31 11:05','6300',  9950,'Manual','K. Wong'),
 ('JE004','2027-01-02 09:30','4000',-250000,'Manual','K. Wong'),
 ('JE005','2026-11-15 14:20','1999',  3750,'Manual','D. Smith'),
 ('JE006','2026-12-30 09:00','6100', 12000,'Automated','SYSTEM'),
 ('JE007','2026-12-31 16:45','2100', 50000,'Manual','D. Smith'),
 ('JE008','2026-12-29 12:10','6300',  9800,'Manual','K. Wong'),
 ('JE009','2026-10-05 15:00','6200',   850,'Manual', NULL),
 ('JE010','2026-12-31 18:20','6300',  9990,'Manual','D. Smith');
""")

def run(sql):
    return con.execute(sql).fetchall()
```

**1. Entries above a threshold, and entries just below an approval limit.** `BETWEEN` makes the "just below the limit" test readable. Clusters there can signal entries split to avoid a higher approval:

```python
print(run("SELECT je_id, amount FROM journal_entries WHERE amount >= 50000"))
# [('JE002', 250000.0), ('JE007', 50000.0)]
print(run("SELECT je_id, amount FROM journal_entries WHERE amount BETWEEN 9500 AND 9999.99 ORDER BY amount DESC"))
# [('JE010', 9990.0), ('JE003', 9950.0), ('JE008', 9800.0)]: three entries just under a 10,000 limit
```

**2. Specific accounts with `IN`:** revenue, suspense and accruals in one query:

```python
print(run("SELECT je_id, account, amount FROM journal_entries WHERE account IN ('4000', '1999', '2100') AND source = 'Manual'"))
# [('JE002', '4000', 250000.0), ('JE004', '4000', -250000.0), ('JE005', '1999', 3750.0), ('JE007', '2100', 50000.0)]
```

**3. A cut-off window, and the `BETWEEN` trap with timestamps.** When the column holds a date **and** a time, `BETWEEN '2026-12-24' AND '2026-12-31'` stops at **midnight at the start** of 31 December, so it misses entries posted later that day:

```python
print(run("SELECT COUNT(*) FROM journal_entries WHERE posted_at BETWEEN '2026-12-24' AND '2026-12-31'"))
# [(3,)]: misses everything posted on 31 December
print(run("SELECT COUNT(*) FROM journal_entries WHERE posted_at >= '2026-12-24' AND posted_at < '2027-01-01'"))
# [(7,)]: the safe pattern, from the start date up to *before* the next day
print(run("SELECT je_id, posted_at, amount FROM journal_entries WHERE posted_at >= '2027-01-01' AND posted_at < '2027-01-08'"))
# [('JE004', '2027-01-02 09:30', -250000.0)]: the reversal just after year end
```

In audit, this is the difference between catching the **31 December 22:40 revenue entry (JE002)** and missing it. Together with its 2 January reversal (JE004), it's the classic cut-off pattern.

**4. Missing approvals:**

```python
print(run("SELECT je_id, amount FROM journal_entries WHERE source = 'Manual' AND approver IS NULL"))
# [('JE002', 250000.0), ('JE009', 850.0)]
print(run("SELECT COUNT(*) FROM journal_entries WHERE approver = NULL"))
# [(0,)]: "= NULL" never matches, a silent mistake
```

**5. The largest items for testing, and the next batch with `OFFSET`.** A tie-breaker on `je_id` keeps the selection repeatable for the reviewer:

```python
print(run("SELECT je_id, amount FROM journal_entries WHERE source = 'Manual' ORDER BY ABS(amount) DESC, je_id LIMIT 3"))
# [('JE002', 250000.0), ('JE004', -250000.0), ('JE007', 50000.0)]
print(run("SELECT je_id, amount FROM journal_entries WHERE source = 'Manual' ORDER BY ABS(amount) DESC, je_id LIMIT 3 OFFSET 3"))
# [('JE010', 9990.0), ('JE003', 9950.0), ('JE008', 9800.0)]: the next three, if the sample is extended
```

`ABS(amount)` ranks a large **credit** (like the −250,000 reversal) alongside a large debit. Sorting on `amount` alone would push it to the bottom.

## My reflection

This chapter turned SQL from "find rows" into "find the **right** rows": a threshold, a window, a list of accounts and the top items. Those map almost one-to-one onto journal entry test parameters, which makes the queries easy to explain to a reviewer.

The lesson I'll carry is about **boundaries**. `BETWEEN` includes both ends, `= NULL` never works, and a date-only `BETWEEN` on a timestamp silently drops the last day of the period. In audit, the last day of the period is exactly where the risk sits, so I'll write cut-off windows as `>= start AND < next day`, every time.
