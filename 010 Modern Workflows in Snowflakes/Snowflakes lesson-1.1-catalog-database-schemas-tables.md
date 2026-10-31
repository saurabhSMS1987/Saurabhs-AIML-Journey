# Lesson 1: Catalog, Database, Schemas, and Tables

> [!NOTE]
> **Source: [AnalystBuilder](https://www.analystbuilder.com)**<br>
> **Date completed:** October 25, 2026

How Snowflake organizes data, explained with financial audit examples from a utility company's finance department.

## The Big Picture

Think of Snowflake like an office filing system:

| Snowflake | Office analogy |
|---|---|
| **Account** | The whole office building |
| **Database** | A filing cabinet |
| **Schema** | A drawer in that cabinet |
| **Table** | A folder of records inside the drawer |

```
Account                    UTILITY_CO_PROD
└── Database               FINANCE_AUDIT
    └── Schema             GENERAL_LEDGER
        └── Table          JOURNAL_ENTRIES
```

To find any table, you give its full address: `DATABASE.SCHEMA.TABLE`
Example: `FINANCE_AUDIT.GENERAL_LEDGER.JOURNAL_ENTRIES`

## Catalog

- **Snowflake has no "Catalog" level.** The term comes from another tool, Databricks.
- In Snowflake, the top level is the **Account**, the building that holds all your filing cabinets.
- You may still see the word "catalog" in Snowflake's system tables (for example, the `TABLE_CATALOG` column). There, it just means **database**.
- **Watch out:** a Snowflake **warehouse** does not store data. It's the computing power that runs your queries, like the staff who pull and read the files.
- **Example:** a company might use one account for testing (`UTILITY_CO_DEV`) and another for real data (`UTILITY_CO_PROD`), so tests never affect real financial records.

## Database

- A database lives inside an account and holds related schemas. It's one filing cabinet.
- It works the same way as a database in traditional SQL.
- **Example:** the `FINANCE_AUDIT` database holds all the data auditors need to review the company's books, kept separate from other cabinets like `HR` or `OPERATIONS`.

## Schema

- A schema lives inside a database and groups related tables by topic. It's one drawer in the cabinet.
- **Example:** inside `FINANCE_AUDIT`, each area of the books gets its own drawer:

```
FINANCE_AUDIT
├── GENERAL_LEDGER     the company's main accounting records
├── ACCOUNTS_PAYABLE   money the company owes (vendor bills)
├── REVENUE            money the company earns (customer billing)
└── FIXED_ASSETS       power plants, poles, transformers, and their value
```

## Table

- A table holds the actual data in rows and columns, like a spreadsheet. It's a folder inside the drawer.
- Snowflake stores tables in its own compressed format, split into small chunks called **micro-partitions**. This keeps queries fast even on huge amounts of data. (Delta format belongs to Databricks, not Snowflake.)
- **Examples:**

| Schema (drawer) | Table (folder) | What auditors check |
|---|---|---|
| `GENERAL_LEDGER` | `JOURNAL_ENTRIES` | Every accounting entry was properly approved |
| `ACCOUNTS_PAYABLE` | `VENDOR_INVOICES` | No bill was paid twice |
| `REVENUE` | `CUSTOMER_INVOICES` | Revenue recorded matches what customers were billed |
| `FIXED_ASSETS` | `ASSET_REGISTER` | Equipment values and depreciation are correct |

```sql
-- Look up journal entries using the table's full address
SELECT entry_id, amount, approved_by
FROM FINANCE_AUDIT.GENERAL_LEDGER.JOURNAL_ENTRIES;
```
