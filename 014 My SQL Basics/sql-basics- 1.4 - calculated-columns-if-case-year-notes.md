# SQL Basics: Calculated Columns with IF, CASE and Date Functions: My Notes

*Nov 10, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SQL Basics: Data Retrieval – Single Table** course, chapter **"Calculated columns (IF, CASE, YEAR, CURYEAR)"**, from **[Codebasics.io](https://codebasics.io)**. The audit examples run on SQLite through Python's built-in `sqlite3` module. Where MySQL syntax differs, it's noted.

## Where I started

Until now, every query returned columns that already existed. This chapter showed how to **create new ones on the fly**: profit from revenue and budget, revenue converted to one currency, values rescaled to one unit. Nothing in the table changes; the new column exists only in the query's result. For audit work, that's how raw ledger fields become **test flags**.

## The data in brief

Two tables from the movies database:

- **`actors`:** names and `birth_year`.
- **`financials`:** each movie's `budget` and `revenue`, recorded in different **currencies** (USD and INR) and different **units** (Thousands, Millions and Billions).

## What I learnt

**1. Arithmetic on columns.** Any expression can become a new column, named with `AS`:

```sql
SELECT *, (revenue - budget) AS profit FROM financials;

SELECT name, birth_year, (YEAR(CURDATE()) - birth_year) AS age FROM actors;
```

`CURDATE()` returns today's date, and `YEAR()` takes the year from it. The chapter title's "CURYEAR" refers to this combination; it isn't a separate function. Subtracting birth years gives the age **this year**, which may be one too high for someone who hasn't had their birthday yet.

**2. `IF` for two outcomes:** `IF(condition, value_if_true, value_if_false)`:

```sql
SELECT movie_id, revenue, currency, unit,
       IF(currency = 'USD', revenue * 77, revenue) AS revenue_inr
FROM financials;
```

USD revenue is converted to rupees at a rate of 77, and INR revenue stays as it is.

**3. `CASE` for three or more outcomes:**

```sql
SELECT DISTINCT unit FROM financials;          -- first, find every unit that exists

SELECT movie_id, revenue, currency, unit,
    CASE
        WHEN unit = 'Thousands' THEN revenue / 1000
        WHEN unit = 'Billions'  THEN revenue * 1000
        ELSE revenue                            -- already in millions
    END AS revenue_mln
FROM financials;
```

`CASE` checks each `WHEN` in order, uses the first one that's true, and falls back to `ELSE`. Running `SELECT DISTINCT unit` **first** was a good habit: it confirms every unit is covered before writing the conversion.

| Tool | Use when | Portability |
| --- | --- | --- |
| Arithmetic (`+ - * /`) | Deriving a value, such as profit or margin | Works everywhere |
| `IF(cond, a, b)` | Exactly two outcomes | **MySQL only** |
| `CASE WHEN ... END` | Two or more outcomes | Works in every SQL database |
| `YEAR()`, `CURDATE()` | Date parts and today's date | MySQL names. SQLite uses `strftime()` and `date('now')` |

**Two details worth knowing:**

- **Fixed rates are a judgement.** `revenue * 77` uses one exchange rate for every movie, whatever its release date. That's fine for a lecture, but in practice the rate should come from a dated rates table, and the source documented.
- **Watch the `ELSE`.** Any unit not listed (a typo like `Milions`, say) silently falls into `ELSE` and is treated as millions. Checking `DISTINCT` values first prevents that.

## How this shows up in financial statement audit work

Calculated columns turn a ledger into a **test file**: debit and credit columns, amounts in one currency, aging buckets and risk flags, all computed in one query from the full population. These snippets build a small sample table.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE gl (je_id TEXT, posted_on TEXT, approved_on TEXT, account TEXT,
                 amount REAL, currency TEXT, unit TEXT, source TEXT);
INSERT INTO gl VALUES
 ('JE001','2026-12-28','2026-12-28','4000', -12500,'GBP','Units','Automated'),
 ('JE002','2026-12-31','2027-01-04','4000',   -250,'GBP','Thousands','Manual'),
 ('JE003','2026-12-26','2026-12-29','6300',   9950,'USD','Units','Manual'),
 ('JE004','2026-11-14','2026-11-16','6100',  12000,'EUR','Units','Manual'),
 ('JE005','2026-12-30','2026-12-30','1200',    1.5,'INR','Millions','Automated');
""")

def show(sql):
    cur = con.execute(sql)
    print([d[0] for d in cur.description])
    for row in cur.fetchall():
        print(row)
```

**1. Debit and credit columns from one signed amount,** a `CASE` per column:

```python
show("""
SELECT je_id, amount,
       CASE WHEN amount > 0 THEN amount ELSE 0 END AS debit,
       CASE WHEN amount < 0 THEN -amount ELSE 0 END AS credit
FROM gl""")
# JE001: debit 0, credit 12500 | JE003: debit 9950, credit 0 ...
```

**2. One unit, then one currency:** the lecture's unit and currency conversions, combined. Units are checked first, as in the lecture:

```python
show("SELECT DISTINCT unit FROM gl")       # Units, Thousands, Millions: every case is covered below

show("""
SELECT je_id, amount, unit, currency,
       ROUND(
         amount * CASE unit WHEN 'Thousands' THEN 1000 WHEN 'Millions' THEN 1000000 ELSE 1 END
                * CASE currency WHEN 'USD' THEN 0.79 WHEN 'EUR' THEN 0.85 WHEN 'INR' THEN 0.0095 ELSE 1 END
       , 2) AS amount_gbp
FROM gl""")
# JE002: -250 Thousands GBP -> -250000.0 | JE005: 1.5 Millions INR -> 14250.0
```

The rates here are illustrative. In an engagement, they'd come from a documented, dated source, ideally a rates table joined in (covered in the next part of the course).

**3. Days to approve, and an aging bucket:**

```python
show("""
SELECT je_id, posted_on, approved_on,
       CAST(julianday(approved_on) - julianday(posted_on) AS INTEGER) AS days_to_approve,
       CASE
           WHEN approved_on > '2026-12-31' AND posted_on <= '2026-12-31' THEN 'Approved after year end'
           WHEN julianday(approved_on) - julianday(posted_on) > 2 THEN 'Slow (over 2 days)'
           ELSE 'Timely'
       END AS approval_status
FROM gl ORDER BY days_to_approve DESC""")
# JE002: 4 days, 'Approved after year end' | JE003: 3 days, 'Slow (over 2 days)'
```

In MySQL, the day difference is `DATEDIFF(approved_on, posted_on)`.

**4. A simple risk score from several flags.** Each `CASE` adds a point, and the total ranks entries for testing:

```python
show("""
SELECT je_id, account, amount,
       (CASE WHEN source = 'Manual' THEN 1 ELSE 0 END)
     + (CASE WHEN strftime('%w', posted_on) IN ('0', '6') THEN 1 ELSE 0 END)      -- weekend: 0 = Sunday, 6 = Saturday
     + (CASE WHEN posted_on >= '2026-12-28' THEN 1 ELSE 0 END)                    -- last days of the year
     + (CASE WHEN account LIKE '4%' AND source = 'Manual' THEN 1 ELSE 0 END)      -- manual revenue
       AS risk_score
FROM gl ORDER BY risk_score DESC, je_id""")
# JE002 scores 3: a manual revenue entry in the last days of the year
```

In MySQL, the weekend check is `DAYOFWEEK(posted_on) IN (1, 7)`.

## My reflection

Calculated columns changed how I think about writing tests. Instead of exporting data and adding formula columns in Excel, the query itself can produce debit and credit splits, converted amounts, approval delays and risk flags, all for the **full population** and in a form a reviewer can read and re-run.

The habit I'll keep from the lecture is the small one: **check the `DISTINCT` values before writing a `CASE`**. In client data, an unexpected unit, currency or status code is common, and a `CASE` without that check would quietly push it into the `ELSE` branch and convert it wrongly.
