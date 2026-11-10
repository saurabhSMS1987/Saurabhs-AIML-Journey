# SQL Basics: Retrieving Data with SELECT, WHERE, DISTINCT and LIKE: My Notes

*Nov 9, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SQL Basics: Data Retrieval – Single Table** course, chapter **"Retrieve data using text query (SELECT, WHERE, DISTINCT, LIKE)"**, from **[Codebasics.io](https://codebasics.io)**. The audit examples run on SQLite through Python's built-in `sqlite3` module, and the same SQL works in MySQL.

## Where I started

I've already queried databases from Python in the MySQL lecture, but always with someone else's `SELECT` statement. This chapter went back to the foundations: how to **ask a table a question in SQL itself**. It's the skill I'll use most at work, because most of our journal entry data sits in databases before it ever reaches Python or Excel.

## The data in brief

The lecture used a **movies database**: a `movies` table with columns such as `title`, `industry` (Hollywood or Bollywood), `studio`, `release_year` and `imdb_rating`.

## What I learnt

**The core pattern: which columns, from which table, which rows.**

```sql
USE moviesdb;                                     -- choose the database to work in

SELECT * FROM movies;                             -- * = every column
SELECT title, industry FROM movies;               -- only the columns you need
SELECT * FROM movies WHERE industry = "Hollywood";
SELECT COUNT(*) FROM movies WHERE industry = "Hollywood";   -- how many rows match
SELECT DISTINCT industry FROM movies;             -- each value once: Hollywood, Bollywood
```

| Keyword | What it does |
| --- | --- |
| `USE` | Points the query at one database, when the server holds several |
| `SELECT` | Chooses the columns, with `*` for all of them |
| `FROM` | Names the table |
| `WHERE` | Keeps only the rows that meet a condition |
| `COUNT(*)` | Counts the rows that match |
| `DISTINCT` | Removes repeated values, showing each one only once |

**Text searches with `LIKE` and the `%` wildcard.** `%` stands for "any characters, or none":

```sql
SELECT * FROM movies WHERE title LIKE 'THOR%';       -- starts with "Thor"
SELECT * FROM movies WHERE title LIKE '%America%';   -- contains "America" anywhere
```

| Pattern | Matches |
| --- | --- |
| `'THOR%'` | Titles that **start** with Thor |
| `'%America%'` | Titles **containing** America |
| `'%Returns'` | Titles that **end** with Returns |

**Finding blank values:** `WHERE studio = ''` finds movies whose studio is an **empty text value**.

**Three details worth knowing:**

- **Quotes:** MySQL accepts both `"Hollywood"` and `'Hollywood'` for text. Standard SQL, and most other databases, use **single quotes** for text, so single quotes are the safer habit.
- **Case:** `LIKE 'THOR%'` matched `Thor: Ragnarok` because MySQL's default settings ignore upper and lower case. Some databases, such as PostgreSQL, don't.
- **Blank isn't the same as missing:** `= ''` finds empty text, but it **doesn't** find `NULL` (a value that was never entered). Missing values need `IS NULL`, which comes up in the next chapter.

## How this shows up in financial statement audit work

These are the first queries I'd run on a client's journal entry table: what's in it, how many entries there are, which users posted them, and which descriptions look unusual. The snippets build a small sample table so they run anywhere.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE journal_entries (
    je_id TEXT, posting_date TEXT, account TEXT, amount REAL,
    source TEXT, preparer TEXT, description TEXT);
INSERT INTO journal_entries VALUES
 ('JE001','2026-12-28','4000', 12500,'Automated','SYSTEM','Sales invoice batch'),
 ('JE002','2026-12-31','4000',250000,'Manual','A. Rao','Year-end revenue adjustment'),
 ('JE003','2026-12-31','6300', 9950,'Manual','M. Gomez','Consulting fee'),
 ('JE004','2027-01-02','4000',-250000,'Manual','A. Rao','Reversal of JE002'),
 ('JE005','2026-11-15','1999', 3750,'Manual','temp_user','Misc'),
 ('JE006','2026-12-30','6100', 12000,'Automated','SYSTEM','Rent accrual'),
 ('JE007','2026-12-31','2100', 50000,'Manual','J. Lee',''),
 ('JE008','2026-12-29','6200', 850,'Manual','S. Patel', NULL);
""")

def run(sql):
    return con.execute(sql).fetchall()
```

**1. The population: how many entries, and how many of them manual?**

```python
print(run("SELECT COUNT(*) FROM journal_entries"))                                  # [(8,)]
print(run("SELECT COUNT(*) FROM journal_entries WHERE source = 'Manual'"))          # [(6,)]
print(run("SELECT je_id, account, amount FROM journal_entries WHERE amount >= 50000"))
# [('JE002', '4000', 250000.0), ('JE007', '2100', 50000.0)]
```

Agreeing the row count and total to the client's trial balance is the first completeness check on any extract.

**2. Who posts entries?** `DISTINCT` lists every user once, ready to compare with the client's list of authorised users:

```python
print(run("SELECT DISTINCT preparer FROM journal_entries"))
# [('SYSTEM',), ('A. Rao',), ('M. Gomez',), ('temp_user',), ('J. Lee',), ('S. Patel',)]
print(run("SELECT COUNT(DISTINCT preparer) FROM journal_entries"))                  # [(6,)]
```

A user called `temp_user` is exactly the kind of name that shouldn't be on that list.

**3. Keyword searches on descriptions with `LIKE`:** a standard journal entry test for risky wording:

```python
print(run("SELECT je_id, description FROM journal_entries "
          "WHERE description LIKE '%adjust%' OR description LIKE '%reversal%' OR description LIKE 'Misc%'"))
# [('JE002', 'Year-end revenue adjustment'), ('JE004', 'Reversal of JE002'), ('JE005', 'Misc')]

print(run("SELECT je_id, preparer FROM journal_entries WHERE preparer LIKE 'temp%'"))   # [('JE005', 'temp_user')]
```

JE002 and JE004 together show **revenue recorded on 31 December and reversed on 2 January**, a classic cut-off red flag.

**4. Entries with no explanation: blank and missing are different.**

```python
print(run("SELECT je_id FROM journal_entries WHERE description = ''"))              # [('JE007',)]
print(run("SELECT je_id FROM journal_entries WHERE description = '' OR description IS NULL"))
# [('JE007',), ('JE008',)]: checking only = '' would have missed JE008
```

**5. Posting to a suspense account,** using `LIKE` on an account code:

```python
print(run("SELECT je_id, account, description FROM journal_entries WHERE account LIKE '19%'"))
# [('JE005', '1999', 'Misc')]: suspense, posted by temp_user with a one-word description
```

## My reflection

Six keywords (`SELECT`, `FROM`, `WHERE`, `COUNT`, `DISTINCT` and `LIKE`) already cover a surprising number of standard journal entry tests: population counts, user listings, keyword searches and blank descriptions. Running them directly in the database also means I'm testing the **full population** where it lives, not a copy that might have been filtered on its way to Excel.

The detail I'll remember is **blank vs `NULL`**. In the lecture, `studio = ''` was enough. In client data, a missing description could be stored either way, and checking only one would quietly understate the exceptions.
