# SQL: CROSS JOIN and CONCAT: My Notes

*Nov 10, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SQL Basics: Data Retrieval – Multiple Tables** course, chapter **"Cross Join"**, from **[Codebasics.io](https://codebasics.io)**, using the lecture's `food_db` database. The examples run on SQLite 3.45 through Python's built-in `sqlite3` module. MySQL differences are noted.

## Where I started

Every join so far matched rows on a **shared key**. A `CROSS JOIN` doesn't need one: it pairs **every row of one table with every row of the other**. At first that sounded like a mistake waiting to happen, and it can be. But it's exactly the right tool for building a complete grid of combinations, which turns out to be very useful for completeness testing.

## The data in brief

The lecture's `food_db` has two small tables for a restaurant menu, with **no column in common**:

| `items` | price | | `variants` | variant_price |
| --- | --- | --- | --- | --- |
| vada pav | 10 | | butter | 5 |
| dosa | 20 | | cheese | 10 |
| sandwich | 16 | | plain | 0 |

## What I learnt

**A `CROSS JOIN` creates every combination,** and calculated columns build the full menu:

```sql
SELECT *,
       CONCAT(name, " - ", variant_name) AS full_name,
       (price + variant_price) AS full_price
FROM food_db.items
CROSS JOIN food_db.variants;
```

The result has **3 × 3 = 9 rows**, one for every item-and-variant pairing:

| full_name | full_price | | full_name | full_price | | full_name | full_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| vada pav - butter | 15 | | dosa - butter | 25 | | sandwich - butter | 21 |
| vada pav - cheese | 20 | | dosa - cheese | 30 | | sandwich - cheese | 26 |
| vada pav - plain | 10 | | dosa - plain | 20 | | sandwich - plain | 16 |

| Concept | Meaning |
| --- | --- |
| `CROSS JOIN` | Pairs every row of table A with every row of table B. There's no `ON` condition |
| Result size | Rows in A **×** rows in B |
| `CONCAT(a, " - ", b)` | Joins text together, like Excel's `CONCAT` or `&` |
| `food_db.items` | `database.table`: refers to a table in another database without a `USE` statement |

**When to use it:** when two tables share no column, but you need **every combination** of their values: menu options, product × size, or (for audit) entity × month.

**Three details worth knowing:**

- **The size grows fast.** 1,000 rows crossed with 1,000 rows gives a million rows. Always check the row counts first.
- **`CONCAT` with a `NULL` returns `NULL`** in MySQL. `CONCAT_WS(" - ", a, b)` skips `NULL` values instead.
- **`||` isn't portable.** In SQLite, PostgreSQL and Oracle, `||` joins text. In MySQL, `||` means logical `OR` by default, so `CONCAT` is the safe choice there. SQLite 3.44+ also supports `concat()`.

## How this shows up in financial statement audit work

The audit power of a `CROSS JOIN` is in building **what should exist**, then comparing it with **what does exist**. These snippets build a small example.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE entities (entity TEXT);
INSERT INTO entities VALUES ('UK01'), ('US01'), ('IN01');

CREATE TABLE periods (period TEXT);
INSERT INTO periods VALUES ('2026-10'), ('2026-11'), ('2026-12');

-- recurring monthly depreciation journals actually posted
CREATE TABLE depreciation_je (entity TEXT, period TEXT, amount REAL);
INSERT INTO depreciation_je VALUES
 ('UK01','2026-10',4200), ('UK01','2026-11',4200), ('UK01','2026-12',4200),
 ('US01','2026-10',6100), ('US01','2026-12',6100),
 ('IN01','2026-10',1800), ('IN01','2026-11',1800), ('IN01','2026-12',1800), ('IN01','2026-12',1800);

CREATE TABLE manual_je (je_id TEXT, amount REAL);
INSERT INTO manual_je VALUES ('JE01',4200), ('JE02',9950), ('JE03',25000), ('JE04',98000), ('JE05',250000);

CREATE TABLE thresholds (threshold REAL);
INSERT INTO thresholds VALUES (5000), (10000), (50000), (100000);
""")

def run(sql):
    return con.execute(sql).fetchall()
```

**1. The expected grid: every entity × every month,** like the menu of every item × variant:

```python
print(run("SELECT COUNT(*) FROM entities CROSS JOIN periods"))     # [(9,)]: 3 entities × 3 months
```

**2. Completeness of recurring journals.** A `LEFT JOIN` from the grid to the actual postings shows any month where depreciation was **never posted**, and any that were **posted twice**:

```python
print(run("""
SELECT e.entity, p.period, COUNT(d.amount) AS journals_posted
FROM entities e
CROSS JOIN periods p
LEFT JOIN depreciation_je d ON d.entity = e.entity AND d.period = p.period
GROUP BY e.entity, p.period
HAVING COUNT(d.amount) != 1
ORDER BY e.entity, p.period"""))
# [('IN01', '2026-12', 2), ('US01', '2026-11', 0)]: US01 missed November, and IN01 posted December twice
```

Querying only the posted journals could never show the **missing** November entry, because there's no row to find. The cross-joined grid creates the row that should be there. (`HAVING` filters grouped results, like `WHERE` for groups. It's the chapter I'll cover next.)

**3. Sensitivity analysis: how many entries would each threshold select?** Crossing entries with candidate thresholds answers it in one query, which is useful when agreeing a testing threshold:

```python
print(run("""
SELECT t.threshold,
       SUM(CASE WHEN m.amount >= t.threshold THEN 1 ELSE 0 END) AS entries_selected,
       SUM(CASE WHEN m.amount >= t.threshold THEN m.amount ELSE 0 END) AS value_covered
FROM thresholds t CROSS JOIN manual_je m
GROUP BY t.threshold ORDER BY t.threshold"""))
# [(5000.0, 4, 382950.0), (10000.0, 3, 373000.0), (50000.0, 2, 348000.0), (100000.0, 1, 250000.0)]
```

A 50,000 threshold tests just 2 entries yet covers 348,000 of the 387,150 total (90%).

**4. Readable labels and composite keys with concatenation:**

```python
print(run("""
SELECT e.entity || '-' || p.period AS entity_period
FROM entities e CROSS JOIN periods p
ORDER BY entity_period LIMIT 3"""))
# [('IN01-2026-10',), ('IN01-2026-11',), ('IN01-2026-12',)]
```

Keys like `UK01-2026-12` make a handy single column for matching or labelling. In MySQL, write `CONCAT(e.entity, '-', p.period)`.

## My reflection

I came into this chapter thinking a `CROSS JOIN` was something to avoid, since every textbook warns about it exploding row counts. That warning stands, but the depreciation example changed my mind about its value. The hardest thing to test in audit is **what's missing**, because missing entries leave no rows behind. A cross-joined grid of everything that *should* exist, compared with what does, makes those gaps visible.

It also makes Excel thinking explicit, as the lecture said: the menu is just every row label against every column label, and `CONCAT` is Excel's `&` in SQL clothing.
