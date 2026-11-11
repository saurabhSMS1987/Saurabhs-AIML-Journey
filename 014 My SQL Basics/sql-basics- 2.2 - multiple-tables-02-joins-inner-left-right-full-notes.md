# SQL Joins: INNER, LEFT, RIGHT and FULL: My Notes

*Nov 10, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SQL Basics: Data Retrieval – Multiple Tables** course, chapter **"SQL Joins (INNER, LEFT, RIGHT, FULL)"**, from **[Codebasics.io](https://codebasics.io)**. The audit examples run on SQLite 3.45 through Python's built-in `sqlite3` module. MySQL differences are noted.

## Where I started

The last chapter explained *why* data is split across tables. This one showed how to **put it back together** with `JOIN`, and, just as importantly, what happens to rows that **don't** find a match. For audit work, those unmatched rows are often the whole point: the invoice that never reached the ledger, or the bank payment with no matching entry.

## The data in brief

Two tables from the movies database: **`movies`** (title, industry and so on) and **`financials`** (budget, revenue, currency, unit), linked by **`movie_id`**. Some movies have no financial record, and some financial records belong to movies that aren't in `movies`, which is what makes the different join types visible.

## What I learnt

**The basic join:** match rows where the key is equal.

```sql
SELECT m.movie_id, title, budget, revenue, currency, unit
FROM movies m                         -- "m" is an alias, short for movies
INNER JOIN financials f               -- "f" for financials
ON m.movie_id = f.movie_id;
```

Aliases like `m` and `f` keep queries short, and `m.movie_id` says exactly which table's `movie_id` is meant. Writing just `JOIN` means `INNER JOIN`, the default.

**The four join types:**

| Join | Keeps | Unmatched values show as |
| --- | --- | --- |
| `INNER JOIN` | Only rows with a match in **both** tables | n/a (they're dropped) |
| `LEFT JOIN` | **All** rows from the left table, plus matches | `NULL` in the right table's columns |
| `RIGHT JOIN` | **All** rows from the right table, plus matches | `NULL` in the left table's columns |
| `FULL JOIN` | **All** rows from **both** tables | `NULL` on whichever side has no match |

`LEFT`, `RIGHT` and `FULL` are together called **outer joins**.

**MySQL has no `FULL JOIN`**, so the lecture built one with `UNION`:

```sql
SELECT m.movie_id, title, revenue FROM movies m LEFT JOIN financials f ON m.movie_id = f.movie_id
UNION
SELECT m.movie_id, title, revenue FROM movies m RIGHT JOIN financials f ON m.movie_id = f.movie_id;
```

`UNION` stacks the two results and removes rows that appear in both.

**Other useful forms from the lecture:**

```sql
-- swapping the tables: financials LEFT JOIN movies = movies RIGHT JOIN financials
SELECT m.movie_id, title, revenue FROM financials f LEFT JOIN movies m ON m.movie_id = f.movie_id;

-- USING: a shortcut when the key column has the same name in both tables
SELECT movie_id, title, revenue FROM movies m LEFT JOIN financials f USING (movie_id);

-- joining on more than one column, with AND
... JOIN other_table o ON t.col1 = o.col1 AND t.col2 = o.col2
```

The SQL editor (MySQL Workbench) also has an **export button** to save any result as a `.csv` file.

**Three details worth knowing:**

- **Pick the key column from the right table.** In the `FULL JOIN` above, `m.movie_id` is `NULL` for financial records with no movie. `COALESCE(m.movie_id, f.movie_id)`, or `USING`, shows the ID from whichever side has it.
- **`UNION` removes identical rows; `UNION ALL` keeps them.** If two genuinely separate records happen to look identical, `UNION` silently merges them.
- **Joins can multiply rows.** If the right-hand key isn't unique, each left row matches several right rows, and totals inflate.

## How this shows up in financial statement audit work

Joins are how reconciliations work in SQL: sub-ledger to general ledger, bank to cash book, journal lines to master data. The **matched** rows confirm, and the **unmatched** rows are the exceptions. These snippets build a small example.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE ar_invoices (invoice_id TEXT, customer TEXT, amount REAL);        -- AR sub-ledger
INSERT INTO ar_invoices VALUES ('INV101','Acme',12500), ('INV102','Beta',8400),
                               ('INV103','Gamma',3100), ('INV104','Delta',92000);

CREATE TABLE gl_revenue (je_id TEXT, invoice_id TEXT, amount REAL);            -- revenue postings in the GL
INSERT INTO gl_revenue VALUES ('JE01','INV101',12500), ('JE02','INV102',8400),
                              ('JE03','INV104',90000), ('JE04', NULL, 250000);

CREATE TABLE bank (txn_date TEXT, amount REAL, ref TEXT);
INSERT INTO bank VALUES ('2026-12-30',12500,'Acme'), ('2026-12-31',8400,'Beta'), ('2026-12-31',4300,'Unknown');

CREATE TABLE cash_book (posted_on TEXT, amount REAL, je_id TEXT);
INSERT INTO cash_book VALUES ('2026-12-30',12500,'JE10'), ('2026-12-30',8400,'JE11');

CREATE TABLE vendors (vendor_id TEXT, vendor_name TEXT);
INSERT INTO vendors VALUES ('V10','Acme Consulting'), ('V10','Acme Consulting Ltd'), ('V11','Beta Travel');

CREATE TABLE ap_lines (je_id TEXT, vendor_id TEXT, amount REAL);
INSERT INTO ap_lines VALUES ('JE20','V10',9950), ('JE21','V11',850);
""")

def run(sql):
    return con.execute(sql).fetchall()
```

**1. `INNER JOIN`: invoices that reached the ledger, and whether the amounts agree.**

```python
print(run("""
SELECT a.invoice_id, a.amount AS ar_amount, g.amount AS gl_amount, a.amount - g.amount AS difference
FROM ar_invoices a JOIN gl_revenue g ON a.invoice_id = g.invoice_id"""))
# [('INV101', 12500.0, 12500.0, 0.0), ('INV102', 8400.0, 8400.0, 0.0), ('INV104', 92000.0, 90000.0, 2000.0)]
```

INV104 matched, but the ledger recorded 2,000 less than the invoice.

**2. `LEFT JOIN ... IS NULL`: invoices that never reached the ledger** (completeness):

```python
print(run("""
SELECT a.invoice_id, a.amount FROM ar_invoices a
LEFT JOIN gl_revenue g ON a.invoice_id = g.invoice_id
WHERE g.invoice_id IS NULL"""))
# [('INV103', 3100.0)]: invoiced to the customer, but missing from revenue
```

**3. The other direction: revenue with no invoice behind it** (occurrence). Swapping the tables turns a `LEFT JOIN` into the reverse check:

```python
print(run("""
SELECT g.je_id, g.amount FROM gl_revenue g
LEFT JOIN ar_invoices a ON g.invoice_id = a.invoice_id
WHERE a.invoice_id IS NULL"""))
# [('JE04', 250000.0)]: 250,000 of revenue with no supporting invoice
```

**4. A full reconciliation in one result,** the lecture's `UNION` approach, with `COALESCE` so the key always shows:

```python
for row in run("""
SELECT COALESCE(a.invoice_id, g.invoice_id, g.je_id) AS ref, a.amount AS ar, g.amount AS gl,
       CASE WHEN a.invoice_id IS NULL THEN 'GL only'
            WHEN g.invoice_id IS NULL THEN 'AR only'
            WHEN a.amount != g.amount THEN 'Amount differs'
            ELSE 'Matched' END AS status
FROM ar_invoices a LEFT JOIN gl_revenue g ON a.invoice_id = g.invoice_id
UNION
SELECT COALESCE(a.invoice_id, g.invoice_id, g.je_id), a.amount, g.amount, 'GL only'
FROM gl_revenue g LEFT JOIN ar_invoices a ON a.invoice_id = g.invoice_id
WHERE a.invoice_id IS NULL
ORDER BY status, ref"""):
    print(row)
# ('INV103', 3100.0, None, 'AR only') / ('INV104', 92000.0, 90000.0, 'Amount differs')
# ('JE04', None, 250000.0, 'GL only') / ('INV101', ...'Matched') / ('INV102', ...'Matched')
```

SQLite 3.39+ and PostgreSQL also support `FULL JOIN` directly. In MySQL, this `UNION` pattern is the way.

**5. Joining on two columns: bank to cash book on date AND amount.**

```python
print(run("""
SELECT b.txn_date, b.amount, b.ref FROM bank b
LEFT JOIN cash_book c ON b.amount = c.amount AND b.txn_date = c.posted_on
WHERE c.je_id IS NULL"""))
# [('2026-12-31', 8400.0, 'Beta'), ('2026-12-31', 4300.0, 'Unknown')]
```

The 4,300 receipt is genuinely unrecorded. The 8,400 one *was* recorded, but on 30 December, a day earlier than the bank. Matching on **both** columns flags it as a **timing difference** to explain, which matching on amount alone would have hidden.

**6. The row-multiplication trap: a duplicated master record.**

```python
print(run("SELECT COUNT(*), SUM(amount) FROM ap_lines"))                                     # [(2, 10800.0)]
print(run("SELECT COUNT(*), SUM(l.amount) FROM ap_lines l JOIN vendors v ON l.vendor_id = v.vendor_id"))
# [(3, 20750.0)]: V10 appears twice in the vendor master, so its 9,950 line is counted twice
```

Comparing row counts and totals before and after a join is a two-second check that catches this.

## My reflection

Joins turned out to be the SQL version of a reconciliation, which made them feel familiar straight away. An `INNER JOIN` shows what agrees, while a `LEFT JOIN ... IS NULL` in **each direction** gives me completeness (invoices missing from revenue) and occurrence (revenue with no invoice). And the `UNION`-based full join puts the whole reconciliation into one table a reviewer can read.

The warnings stuck just as firmly: `NULL` keys after an outer join, `UNION` quietly merging lookalike rows, and a duplicated master record doubling a total. So my habit now is to **check the row count and total before and after every join**. If they move unexpectedly, the join is wrong, not the client.
