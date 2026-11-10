# SQL Basics: Summary Analytics with COUNT, MIN, MAX, AVG and GROUP BY: My Notes

*Nov 9, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SQL Basics: Data Retrieval – Single Table** course, chapter **"Summary analytics (MIN, MAX, AVG, GROUP BY)"**, from **[Codebasics.io](https://codebasics.io)**. The audit examples run on SQLite through Python's built-in `sqlite3` module. Where MySQL syntax differs, it's noted.

## Where I started

The first two chapters returned **rows**. This one returned **answers**: how many, how much, the highest, the lowest and the average, for the whole table or for each group. That's the shift from listing data to **analysing** it, and it's exactly what a trial balance, a preparer summary or a monthly trend is.

## The data in brief

The same **movies** table, now summarised by `industry` (Hollywood or Bollywood) and by `studio`, using the `imdb_rating` column.

## What I learnt

**Aggregate functions turn many rows into one value:**

```sql
SELECT COUNT(*) FROM movies;                                          -- how many rows
SELECT MAX(imdb_rating) FROM movies WHERE industry = 'Bollywood';     -- highest
SELECT MIN(imdb_rating) FROM movies WHERE industry = 'Bollywood';     -- lowest
SELECT ROUND(AVG(imdb_rating), 2) FROM movies WHERE studio = 'Marvel Studios';   -- average, to 2 decimals
```

**`AS` gives a result column a readable name, and several aggregates can sit in one query:**

```sql
SELECT
    MIN(imdb_rating) AS min_rating,
    MAX(imdb_rating) AS max_rating,
    ROUND(AVG(imdb_rating), 2) AS avg_rating
FROM movies
WHERE studio = 'Marvel Studios';
```

**`GROUP BY` calculates the aggregate separately for each group:**

```sql
SELECT industry, COUNT(industry) AS movie_count, AVG(imdb_rating) AS avg_rating
FROM movies
GROUP BY industry;                                  -- one row per industry

SELECT studio, COUNT(studio) AS cnt, ROUND(AVG(imdb_rating), 1) AS avg_rating
FROM movies
WHERE studio != ''                                  -- leave out blank studios first
GROUP BY studio
ORDER BY avg_rating DESC;                           -- sort by the alias
```

| Function | Returns |
| --- | --- |
| `COUNT(*)` | The number of rows |
| `COUNT(column)` | The number of rows where that column **isn't `NULL`** |
| `MIN()`, `MAX()` | The smallest and largest values |
| `AVG()` | The mean, **ignoring `NULL`s** |
| `ROUND(x, n)` | `x` rounded to `n` decimal places |
| `SUM()` | The total. It isn't used in the lecture, but it's the one I'll use most |

**The order SQL works in:** `WHERE` filters rows **first**, then `GROUP BY` forms the groups, then the aggregates are calculated, and finally `ORDER BY` sorts the result. That's why `WHERE studio != ''` removes blank studios *before* they're counted.

**Two details worth knowing:**

- **Every column in `SELECT` must either be grouped or aggregated.** `SELECT studio, title, COUNT(*) ... GROUP BY studio` is ambiguous, because which title should it show? MySQL rejects it by default.
- **`NULL`s affect the results quietly:** `AVG(imdb_rating)` averages only the rated movies, and `COUNT(imdb_rating)` counts only those too. Comparing `COUNT(*)` with `COUNT(column)` is a quick way to see how many values are missing.

## How this shows up in financial statement audit work

Summaries like these are how I'd check an extract is complete, then decide where to look closer. These snippets build a small sample journal entry table. Debits are positive and credits negative, so every balanced entry sums to zero.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE gl (je_id TEXT, posted_on TEXT, account TEXT, amount REAL, source TEXT, preparer TEXT, approver TEXT);
INSERT INTO gl VALUES
 ('JE001','2026-10-12','1200', 12500,'Automated','SYSTEM','SYSTEM'), ('JE001','2026-10-12','4000',-12500,'Automated','SYSTEM','SYSTEM'),
 ('JE002','2026-11-20','6300',  9950,'Manual','M. Gomez','K. Wong'), ('JE002','2026-11-20','2000', -9950,'Manual','M. Gomez','K. Wong'),
 ('JE003','2026-12-31','1200',250000,'Manual','A. Rao', NULL),      ('JE003','2026-12-31','4000',-250000,'Manual','A. Rao', NULL),
 ('JE004','2026-12-30','6100', 12000,'Automated','SYSTEM','SYSTEM'), ('JE004','2026-12-30','2100',-12000,'Automated','SYSTEM','SYSTEM'),
 ('JE005','2026-12-31','6300',  5000,'Manual','J. Lee','D. Smith'),   ('JE005','2026-12-31','2000', -4500,'Manual','J. Lee','D. Smith'),
 ('JE006','2026-11-05','6200',   850,'Manual','M. Gomez', NULL),     ('JE006','2026-11-05','1000',  -850,'Manual','M. Gomez', NULL);
""")

def run(sql):
    return con.execute(sql).fetchall()
```

**1. A population summary: the first check on any extract.** If debits and credits balance, the total of all lines is zero:

```python
print(run("""
SELECT COUNT(*) AS lines, COUNT(DISTINCT je_id) AS entries,
       SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS debits,
       ROUND(SUM(amount), 2) AS net,
       MAX(amount) AS largest_debit, MIN(amount) AS largest_credit
FROM gl"""))
# [(12, 6, 290300.0, 500.0, 250000.0, -250000.0)]: the ledger is out of balance by 500
```

**2. Which entry causes the imbalance?** Grouping by `je_id` gives each entry's net, and an entry that balances nets to zero:

```python
print(run("SELECT je_id, ROUND(SUM(amount), 2) AS net FROM gl GROUP BY je_id ORDER BY ABS(net) DESC, je_id LIMIT 3"))
# [('JE005', 500.0), ('JE001', 0.0), ('JE002', 0.0)]: JE005's debit is 500 more than its credit
```

The next chapter's `HAVING` clause filters these groups directly, for example `HAVING net != 0`.

**3. Balances by account,** a mini trial balance built straight from the ledger, ready to agree to the client's trial balance:

```python
for row in run("SELECT account, COUNT(*) AS lines, SUM(amount) AS balance FROM gl GROUP BY account ORDER BY account"):
    print(row)
# ('1000', 1, -850.0) ... ('1200', 2, 262500.0) ... ('4000', 2, -262500.0) ... ('6300', 2, 14950.0)
```

**4. Who posts what?** Manual activity by preparer, with missing approvals counted via `COUNT(*) − COUNT(approver)`:

```python
print(run("""
SELECT preparer,
       COUNT(DISTINCT je_id) AS entries,
       SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS debit_value,
       ROUND(AVG(ABS(amount)), 0) AS avg_line,
       COUNT(*) - COUNT(approver) AS lines_without_approver
FROM gl
WHERE source = 'Manual'
GROUP BY preparer
ORDER BY debit_value DESC"""))
# [('A. Rao', 1, 250000.0, 250000.0, 2), ('M. Gomez', 2, 10800.0, 5400.0, 2), ('J. Lee', 1, 5000.0, 4750.0, 0)]
```

A. Rao posted the single largest manual entry, with **no approver**: a clear selection for testing.

**5. A monthly trend,** grouping by part of the date:

```python
print(run("""
SELECT substr(posted_on, 1, 7) AS month, COUNT(DISTINCT je_id) AS entries,
       SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS debit_value
FROM gl GROUP BY month ORDER BY month"""))
# [('2026-10', 1, 12500.0), ('2026-11', 2, 10800.0), ('2026-12', 3, 267000.0)]: December carries most of the value
```

In MySQL, the month would be `DATE_FORMAT(posted_on, '%Y-%m')`. In SQLite, `substr()` takes the first 7 characters of the date text.

## My reflection

This chapter felt like the point where SQL becomes an audit tool rather than a lookup tool. One `GROUP BY` produces a trial balance, a preparer profile or a monthly trend, straight from the full population. And the first check, "does the ledger sum to zero?", is a single query.

The detail I'll keep in mind is how quietly **`NULL`s** change answers. `AVG` and `COUNT(column)` simply skip them, so a summary can look complete while hiding gaps. Comparing `COUNT(*)` with `COUNT(approver)` turned that from a risk into a test.
