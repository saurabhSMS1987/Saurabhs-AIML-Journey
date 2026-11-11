# SQL: Why Do We Need Multiple Tables?: My Notes

*Nov 10, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SQL Basics: Data Retrieval – Multiple Tables** course, chapter **"Why do we need multiple tables?"**, from **[Codebasics.io](https://codebasics.io)**. The audit examples run on SQLite through Python's built-in `sqlite3` module, and the same SQL works in MySQL.

## Where I started

Every query so far worked on **one table**. Real systems almost never store data that way. A client's ERP keeps journal lines in one table, the chart of accounts in another, vendors in a third and users in a fourth. This short chapter explained **why** data is split up like that, which is the foundation for `JOIN`, the next big topic.

## The data in brief

The lecture's `sales.xlsx` shows the same 9 grocery transactions stored two ways:

| Sheet | Rows | Columns | What it holds |
| --- | --- | --- | --- |
| `sales_all_in_one` | 9 | 8 | Everything in one table: date, item name, category, price, weight, and customer name, email and address |
| `sales` | 9 | 4 | Just the transaction: date, `item_id`, `customer_id`, weight |
| `customers` | 3 | 4 | Each customer **once**: ID, name, email, address |
| `items` | 6 | 4 | Each item **once**: ID, name, category, price per kg |

In the all-in-one sheet, Tony Sharma's name, email and address are typed **5 times** and Peter Pandey's **4 times**. In the split version, each appears once, and the sales table refers to them by ID.

## What I learnt

**Why companies split data into multiple tables:**

| Reason | In the lecture's example |
| --- | --- |
| **Save space by avoiding repetition** | A customer's address is stored once, not on every purchase |
| **Organise data better** | Transactions, customers and items each have their own table |
| **Make updates easily** | If Tony moves, his address changes in **one** row of `customers`. In the all-in-one sheet, it would need changing in 5 rows, and missing one leaves the data contradicting itself |

**The vocabulary behind it** (my addition, since the lecture shows the idea through the sheets):

| Term | Meaning | Example |
| --- | --- | --- |
| **Primary key** | A column that uniquely identifies each row of a table | `customer_id` in `customers` |
| **Foreign key** | A column that points to a primary key in another table | `customer_id` in `sales` |
| **Normalisation** | Splitting data so that each fact is stored once | The three-table version of the sales data |

**`JOIN` puts the pieces back together.** It matches rows across tables on their keys. Joining the lecture's three sheets on `item_id` and `customer_id` **rebuilds `sales_all_in_one` exactly**, which I checked:

```python
import sqlite3
import pandas as pd

sheets = pd.read_excel("sales.xlsx", sheet_name=None)
con = sqlite3.connect(":memory:")
for name in ["sales", "customers", "items"]:
    sheets[name].dropna(how="all").dropna(axis=1, how="all").to_sql(name, con, index=False)

rebuilt = pd.read_sql("""
    SELECT s.transaction_date, i.item_name, i.item_category, i.price_per_kg, s.order_weight,
           c.customer_name, c.customer_email, c.customer_address
    FROM sales s
    JOIN items i     ON s.item_id = i.item_id
    JOIN customers c ON s.customer_id = c.customer_id""", con)
print(rebuilt.shape)    # (9, 8): the same 9 rows and 8 columns as sales_all_in_one
```

One more thing the split version shows: **Bruce Hariyali (customer 402)** exists in `customers` but has **no sales**. In the all-in-one sheet, he simply doesn't appear, because a flat file only shows customers who bought something.

## How this shows up in financial statement audit work

Journal entry data is a textbook example of multiple tables: **journal lines** refer to a **chart of accounts**, a **vendor master** and a **user master** by ID. Understanding that structure tells me what to request from a client, how to rebuild a full picture, and which **integrity tests** to run. These snippets build a small example.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE accounts (account_id TEXT PRIMARY KEY, account_name TEXT, fsli TEXT);
INSERT INTO accounts VALUES ('1000','Cash','Cash'), ('2000','Payables','Payables'),
                            ('6300','Consulting','Operating expenses'), ('6200','Travel','Operating expenses');

CREATE TABLE users (user_id TEXT PRIMARY KEY, user_name TEXT, status TEXT);
INSERT INTO users VALUES ('U01','A. Rao','Active'), ('U02','M. Gomez','Active'), ('U03','J. Lee','Left company');

CREATE TABLE vendors (vendor_id TEXT PRIMARY KEY, vendor_name TEXT, bank_account TEXT);
INSERT INTO vendors VALUES ('V10','Acme Consulting','GB11-0001'), ('V11','Beta Travel','GB22-0002'),
                           ('V12','Gamma Ltd','GB33-0003');

CREATE TABLE gl_lines (je_id TEXT, account_id TEXT, vendor_id TEXT, user_id TEXT, amount REAL);
INSERT INTO gl_lines VALUES
 ('JE01','6300','V10','U01', 9950), ('JE01','2000','V10','U01',-9950),
 ('JE02','6200','V11','U02',  850), ('JE02','1000','V11','U02', -850),
 ('JE03','6300','V99','U03', 4200), ('JE03','2999','V99','U03',-4200);
""")

def run(sql):
    return con.execute(sql).fetchall()
```

**1. Rebuild a readable view of the journal,** the same idea as rebuilding `sales_all_in_one`:

```python
print(run("""
SELECT g.je_id, a.account_name, v.vendor_name, u.user_name, g.amount
FROM gl_lines g
JOIN accounts a ON g.account_id = a.account_id
JOIN vendors  v ON g.vendor_id  = v.vendor_id
JOIN users    u ON g.user_id    = u.user_id
WHERE g.amount > 0"""))
# [('JE01', 'Consulting', 'Acme Consulting', 'A. Rao', 9950.0), ('JE02', 'Travel', 'Beta Travel', 'M. Gomez', 850.0)]
```

JE03 has disappeared, because its account and vendor don't match anything. That's the next test.

**2. Orphan records: lines pointing to master data that doesn't exist.** In a well-built system, foreign keys would prevent this. In an extract, it's a red flag:

```python
print(run("SELECT je_id, account_id FROM gl_lines WHERE account_id NOT IN (SELECT account_id FROM accounts)"))
# [('JE03', '2999')]: posted to an account that isn't in the chart of accounts
print(run("SELECT DISTINCT je_id, vendor_id FROM gl_lines WHERE vendor_id NOT IN (SELECT vendor_id FROM vendors)"))
# [('JE03', 'V99')]: paid to a vendor that isn't in the vendor master
```

**3. Using master data attributes:** entries posted by users who have **left the company**:

```python
print(run("""
SELECT DISTINCT g.je_id, u.user_name, u.status
FROM gl_lines g JOIN users u ON g.user_id = u.user_id
WHERE u.status != 'Active'"""))
# [('JE03', 'J. Lee', 'Left company')]: the same entry again, now with three red flags
```

**4. Master records with no activity,** the audit version of Bruce Hariyali:

```python
print(run("SELECT vendor_id, vendor_name FROM vendors WHERE vendor_id NOT IN (SELECT vendor_id FROM gl_lines)"))
# [('V12', 'Gamma Ltd')]: a dormant vendor, a candidate for removal from the master file
```

`NOT IN (SELECT ...)` is a **subquery**. The upcoming join lectures show the same tests with a `LEFT JOIN`.

## My reflection

This short chapter explained something I'd seen without really understanding: why client extracts come as separate files and **IDs instead of names**. Each fact lives in one place, and keys link them together. The lecture's sales sheets made it concrete. One customer's address typed five times is five chances for it to disagree with itself.

For audit, the structure is also a **test plan**. Every foreign key is a question: does this account exist? Is this vendor approved? Is this user still employed? And the master data tells me what a flat file can't, such as the customer, or vendor, with no activity at all.
