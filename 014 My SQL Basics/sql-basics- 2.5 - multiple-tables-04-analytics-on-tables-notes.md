# SQL: Analytics on Joined Tables: My Notes

*Nov 10, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SQL Basics: Data Retrieval – Multiple Tables** course, chapter **"Analytics on two tables"**, from **[Codebasics.io](https://codebasics.io)**. The audit examples run on SQLite 3.45 through Python's built-in `sqlite3` module, and the same SQL works in MySQL.

## Where I started

The joins chapter showed how to **connect** tables. This one put that to work: once `movies` and `financials` are joined, every earlier skill (calculated columns, `WHERE`, `CASE`, `ORDER BY` and `LIMIT`) works across both tables at once. It's the point where SQL starts producing real business answers, like "which Bollywood movie made the most profit?", or, for me, "which accounts moved most since last year?"

## The data in brief

The same two tables, joined on `movie_id`: **`movies`** (title, industry and so on) and **`financials`** (budget, revenue, currency, and a **unit** of Thousands, Millions or Billions).

## What I learnt

The lecture built one query in three steps.

**Step 1: join, and add a calculated column.**

```sql
SELECT m.movie_id, title, budget, revenue, currency, unit,
       (revenue - budget) AS profit
FROM movies m
JOIN financials f ON m.movie_id = f.movie_id;
```

**Step 2: filter on a column from either table.**

```sql
... WHERE m.industry = 'Bollywood';     -- industry lives in movies, profit comes from financials
```

**Step 3: put everything in one unit, then rank.** Profits recorded in thousands and billions can't be compared until they're in the same unit:

```sql
SELECT m.movie_id, title, revenue, currency, unit,
       CASE
           WHEN unit = 'Thousands' THEN ROUND((revenue - budget) / 1000, 2)
           WHEN unit = 'Billions'  THEN ROUND((revenue - budget) * 1000, 2)
           ELSE revenue - budget                       -- already in millions
       END AS profit_mln
FROM movies m
JOIN financials f ON m.movie_id = f.movie_id
WHERE m.industry = 'Bollywood'
ORDER BY profit_mln DESC;                              -- add LIMIT 5 for the top 5
```

**The takeaways:**

| Idea | In the lecture |
| --- | --- |
| Merging tables creates insight | Profit needs `financials`, but filtering by industry needs `movies` |
| Normalise before comparing | `CASE` converts every profit to millions |
| **Top N / bottom N** | `ORDER BY ... DESC LIMIT n` for the top, `ASC LIMIT n` for the bottom |

**Two details worth knowing:**

- **A missing comma changes the result.** In the course's step 3 query, `m.movie_id, title revenue, currency` has no comma between `title` and `revenue`. SQL reads that as `title AS revenue`, so the column labelled *revenue* actually shows **titles**, and no error appears. The version above includes the comma.
- **Same unit isn't the same currency.** The `CASE` puts everything in *millions*, but INR and USD millions still aren't comparable. That's fine within Bollywood, but a cross-industry ranking would need a currency conversion too.

## How this shows up in financial statement audit work

Joining the ledger to its reference tables (the chart of accounts and exchange rates) is how raw postings become a **financial statement view** for analytical review. These snippets build a small two-year example.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE accounts (account TEXT PRIMARY KEY, account_name TEXT, fsli TEXT, statement TEXT);
INSERT INTO accounts VALUES
 ('4000','Product revenue','Revenue','P&L'), ('4100','Service revenue','Revenue','P&L'),
 ('5000','Cost of goods sold','Cost of sales','P&L'), ('6000','Salaries','Operating expenses','P&L'),
 ('6300','Consulting','Operating expenses','P&L'), ('1200','Receivables','Receivables','Balance sheet');

CREATE TABLE balances (entity TEXT, year INTEGER, account TEXT, amount REAL, currency TEXT);
INSERT INTO balances VALUES
 ('UK01',2025,'4000',-1820000,'GBP'), ('UK01',2026,'4000',-1950000,'GBP'),
 ('UK01',2025,'4100', -300000,'GBP'), ('UK01',2026,'4100', -410000,'GBP'),
 ('UK01',2025,'5000', 1090000,'GBP'), ('UK01',2026,'5000', 1180000,'GBP'),
 ('UK01',2025,'6000',  420000,'GBP'), ('UK01',2026,'6000',  430000,'GBP'),
 ('UK01',2025,'6300',   60000,'GBP'), ('UK01',2026,'6300',  190000,'GBP'),
 ('UK01',2025,'1200',  470000,'GBP'), ('UK01',2026,'1200',  640000,'GBP'),
 ('US01',2026,'4000',-2400000,'USD'), ('US01',2026,'5000', 1500000,'USD'),
 ('IN01',2026,'4000',-95000000,'INR'), ('IN01',2026,'5000', 52000000,'INR');

CREATE TABLE fx_rates (currency TEXT, year INTEGER, rate_to_gbp REAL);
INSERT INTO fx_rates VALUES ('GBP',2026,1.0), ('USD',2026,0.79), ('INR',2026,0.0095);
""")

def run(sql):
    return con.execute(sql).fetchall()
```

**1. Ledger balances to a financial statement view,** joining to the chart of accounts and grouping by line item. Revenue is stored as negative (credit) amounts, so `-SUM` shows it as positive:

```python
for row in run("""
SELECT a.fsli,
       -SUM(CASE WHEN b.year = 2025 THEN b.amount END) AS py,
       -SUM(CASE WHEN b.year = 2026 THEN b.amount END) AS cy
FROM balances b JOIN accounts a ON b.account = a.account
WHERE b.entity = 'UK01' AND a.statement = 'P&L'
GROUP BY a.fsli ORDER BY cy DESC"""):
    print(row)
# ('Revenue', 2120000.0, 2360000.0) / ('Operating expenses', -480000.0, -620000.0) / ('Cost of sales', -1090000.0, -1180000.0)
```

The bottom line for UK01 is `-SUM(amount)` across all P&L accounts: a profit of **560,000** in 2026, against 550,000 in 2025.

**2. Flux analysis: the largest movements first** (top N by absolute change):

```python
for row in run("""
SELECT a.account_name,
       SUM(CASE WHEN b.year = 2025 THEN b.amount END) AS py,
       SUM(CASE WHEN b.year = 2026 THEN b.amount END) AS cy,
       SUM(CASE WHEN b.year = 2026 THEN b.amount ELSE -b.amount END) AS change,
       ROUND(100.0 * SUM(CASE WHEN b.year = 2026 THEN b.amount ELSE -b.amount END)
             / ABS(SUM(CASE WHEN b.year = 2025 THEN b.amount END)), 1) AS pct
FROM balances b JOIN accounts a ON b.account = a.account
WHERE b.entity = 'UK01'
GROUP BY a.account_name
ORDER BY ABS(change) DESC, a.account_name
LIMIT 3"""):
    print(row)
# ('Receivables', 470000.0, 640000.0, 170000.0, 36.2) / ('Consulting', 60000.0, 190000.0, 130000.0, 216.7)
# ('Product revenue', -1820000.0, -1950000.0, -130000.0, -7.1)
```

Consulting **more than tripled** (+217%), and receivables grew 36% while product revenue grew only 7%. (Revenue shows −7.1% because credits are negative: a larger credit means *more* revenue.) Both are the kind of movement an auditor would ask the client to explain. The second sort column, `a.account_name`, keeps the order repeatable when two changes are the same size.

**3. Comparing entities in one currency:** the lecture's "same unit" idea, done properly with a **join to an exchange-rate table** instead of a hardcoded rate:

```python
for row in run("""
SELECT b.entity, b.currency,
       ROUND(-SUM(CASE WHEN a.fsli = 'Revenue' THEN b.amount ELSE 0 END) * r.rate_to_gbp) AS revenue_gbp,
       ROUND(100.0 * -SUM(b.amount) / -SUM(CASE WHEN a.fsli = 'Revenue' THEN b.amount ELSE 0 END), 1) AS gross_margin_pct
FROM balances b
JOIN accounts a ON b.account = a.account
JOIN fx_rates r ON b.currency = r.currency AND b.year = r.year
WHERE b.year = 2026 AND a.fsli IN ('Revenue', 'Cost of sales')
GROUP BY b.entity, b.currency, r.rate_to_gbp
ORDER BY gross_margin_pct ASC"""):
    print(row)
# ('US01', 'USD', 1896000.0, 37.5) / ('IN01', 'INR', 902500.0, 45.3) / ('UK01', 'GBP', 2360000.0, 50.0)
```

Sorted **ascending**, this is a **bottom N**: US01 has the thinnest gross margin, which is worth understanding before planning the work. The join matches the rate on **both** currency and year, so each year's balances use that year's rate.

## My reflection

This chapter tied the whole SQL course together. A join supplies the context (what an account *is*, what currency it's in), and the earlier tools turn that into an analysis: `CASE` for normalising, `GROUP BY` for summarising, and `ORDER BY ... LIMIT` for "show me the biggest". In a few lines, a list of ledger balances became an income statement, a flux analysis and a cross-entity comparison.

Two things will stay with me. First, the missing comma in the course query, which silently relabelled titles as revenue. Since SQL won't complain, I'll always eyeball column names against values. Second, **normalise everything before comparing**: units, signs (credits as negatives) and currencies, ideally from a rates table rather than a number typed into the query.
