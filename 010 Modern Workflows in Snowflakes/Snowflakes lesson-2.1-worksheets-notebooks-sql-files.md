# Lesson 3: Worksheets, Notebooks, and SQL Files

> [!NOTE]
> **Source: [AnalystBuilder](https://www.analystbuilder.com)**<br>
> **Date completed:** October 26, 2026

Three ways to write and keep your work in Snowflake, explained with examples from an audit of an insurance company's financial statements.

## The Big Picture

An auditor's desk has three kinds of paper on it. Snowflake has the same three tools:

| Snowflake | Auditor's desk analogy | Best for |
|---|---|---|
| **Worksheet** | A scratch pad | Quick checks and one-off questions |
| **Notebook** | An audit working paper | Step-by-step analysis with explanations |
| **SQL file** | A saved audit procedure | Queries you'll reuse and share |

The examples use an `INSURANCE_AUDIT` database with three schemas: `POLICIES`, `CLAIMS`, and `GENERAL_LEDGER`.

## Worksheets

- The classic SQL editor in Snowflake. You write a query, run it, and see the results. Nothing fancy.
- Best for quick data exploration, one-off queries, and testing whether your SQL logic works.

**Example: Do claims paid match the books?**

An auditor wants a quick answer: does the total of claims paid in the claims system match the amount recorded in the general ledger for 2025?

```sql
SELECT
  (SELECT SUM(paid_amount)
   FROM INSURANCE_AUDIT.CLAIMS.CLAIM_PAYMENTS
   WHERE YEAR(payment_date) = 2025) AS claims_system_total,

  (SELECT SUM(amount)
   FROM INSURANCE_AUDIT.GENERAL_LEDGER.JOURNAL_ENTRIES
   WHERE account_name = 'Claims Paid'
     AND fiscal_year = 2025) AS ledger_total;
```

If the two numbers match, the auditor moves on. A worksheet is perfect for this: one question, one answer.

## Notebooks

- A newer tool that mixes **SQL**, **Python**, and **Markdown** (plain-text notes) in one place.
- Work is split into **cells**. Each cell is either code you run or notes you write.
- Better for multi-step work and analysis where you want your explanation sitting right next to your code.

**Example: Testing whether claim reserves look reasonable**

Insurers set aside money, called **reserves**, for claims that haven't been paid yet. Auditors check whether those reserves look reasonable by studying how past claims grew over time. That takes several steps, so a notebook fits well.

**Cell 1 (Markdown):** explain the goal

```markdown
## Reserve Review: Auto Insurance, 2021–2025
Goal: see how much claims grew after they were first reported,
to judge whether this year's reserves are reasonable.
```

**Cell 2 (SQL):** pull the claims data

```sql
SELECT accident_year, development_year, SUM(paid_amount) AS paid
FROM INSURANCE_AUDIT.CLAIMS.CLAIM_PAYMENTS
WHERE line_of_business = 'AUTO'
GROUP BY accident_year, development_year;
```

**Cell 3 (Python):** arrange it into a table auditors can read

```python
from snowflake.snowpark.context import get_active_session

session = get_active_session()
df = session.sql("""
    SELECT accident_year, development_year, SUM(paid_amount) AS paid
    FROM INSURANCE_AUDIT.CLAIMS.CLAIM_PAYMENTS
    WHERE line_of_business = 'AUTO'
    GROUP BY accident_year, development_year
""").to_pandas()

# Rows = year the accident happened, columns = years since then
triangle = df.pivot(index="ACCIDENT_YEAR", columns="DEVELOPMENT_YEAR", values="PAID")
triangle.cumsum(axis=1)
```

**Cell 4 (Markdown):** record the finding

```markdown
**Finding:** Claims from 2023 grew faster than earlier years.
Follow up with the actuarial team before signing off on 2025 reserves.
```

Anyone reviewing the notebook later can see what was done, why, and what was found, just like a good working paper.

## SQL Files

- A **SQL file** is a plain-text file ending in `.sql` that holds one or more SQL queries.
- Unlike a quick worksheet query, a SQL file is meant to be **saved, reused, and shared**.
- You can download your queries from Snowflake as `.sql` files, and Snowflake's newer **Workspaces** editor lets you organize SQL files in folders and connect them to Git.
- Because it's just text, a SQL file can be stored on **GitHub**, so the team can track every change made to an audit procedure.

**Example: A year-end premium cutoff test**

Every year, auditors check that premiums were recorded in the right year. A policy that starts in January 2026 should not count as 2025 income. The team saves this check as `premium_cutoff_test.sql` and reruns it each year-end by changing one date.

```sql
-- premium_cutoff_test.sql
-- Purpose: find policies recorded in the year under audit
--          that actually start in the following year.
-- Change the dates below for each year-end audit.

SELECT policy_id, effective_date, booked_date, written_premium
FROM INSURANCE_AUDIT.POLICIES.POLICY_REGISTER
WHERE booked_date   <= '2025-12-31'
  AND effective_date > '2025-12-31'
ORDER BY written_premium DESC;
```

## Key Takeaway

| | Worksheet | Notebook | SQL File |
|---|---|---|---|
| **What it is** | Simple SQL editor | Mix of SQL, Python, and notes | Saved text file of SQL queries |
| **Best for** | Quick checks, testing SQL | Multi-step analysis with explanations | Reusable, shareable procedures |
| **Insurance audit example** | Claims paid vs. ledger | Claim reserve review | Year-end premium cutoff test |
