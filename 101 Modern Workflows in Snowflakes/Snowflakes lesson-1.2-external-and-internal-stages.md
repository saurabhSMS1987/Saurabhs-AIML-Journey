# Lesson 2: External and Internal Stages

> [!NOTE]
> **Source: [AnalystBuilder](https://www.analystbuilder.com)**<br>
> **Date completed:** October 25, 2026

How files get into Snowflake, explained with financial audit examples from a utility company's finance department.

## What Is a Stage?

A **stage** is a landing zone for files before they're loaded into a table.

Going back to the filing system from Lesson 1: if a table is a folder in a drawer, a stage is the **inbox tray**. Documents arrive there first, and you decide what to file and where.

There are two kinds:

| | Office analogy |
|---|---|
| **External stage** | The documents stay in another building (your cloud storage). Snowflake just keeps the address. |
| **Internal stage** | The documents are dropped into Snowflake's own inbox tray. Snowflake stores them for you. |

## External Stage

**Scenario:** Every night, the company's accounting system exports the day's journal entries as a CSV file to an Amazon S3 bucket, for example `s3://utilityco-finance-raw/gl/2026-10-24.csv`. Auditors want to load these into Snowflake when needed, without keeping a second copy of every raw file.

**Step 1: Create the stage (point Snowflake at the S3 folder)**

```sql
CREATE OR REPLACE STAGE FINANCE_AUDIT.GENERAL_LEDGER.GL_EXPORT_STAGE
  URL = 's3://utilityco-finance-raw/gl/'
  STORAGE_INTEGRATION = finance_s3_integration
  FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
```

- The files stay in S3. Snowflake only saves the location.
- `STORAGE_INTEGRATION` is the secure "key" that lets Snowflake read the bucket. An administrator usually sets it up once.
- Like tables, a stage lives inside a database and schema.

**Step 2: See what files are there**

```sql
LIST @FINANCE_AUDIT.GENERAL_LEDGER.GL_EXPORT_STAGE;
```

**Step 3: Load one day's file into the table**

```sql
COPY INTO FINANCE_AUDIT.GENERAL_LEDGER.JOURNAL_ENTRIES
FROM @FINANCE_AUDIT.GENERAL_LEDGER.GL_EXPORT_STAGE
PATTERN = '.*2026-10-24.*'
ON_ERROR = 'ABORT_STATEMENT';
```

- `PATTERN` picks only the file for October 24.
- `ON_ERROR = 'ABORT_STATEMENT'` stops the load if any row is bad. **For audit work, this is safer than `'CONTINUE'`**, which skips bad rows silently and could leave entries missing from the books.

The raw file stays in S3. Only the loaded rows are stored in Snowflake.

## Internal Stage

**Scenario:** An auditor receives a one-off spreadsheet from procurement, `approved_vendors.xlsx`, to check that payments only went to approved vendors. There's no S3 bucket for it, and it's only needed for this audit.

**Step 1: Save the spreadsheet as CSV**

Snowflake can't load Excel files directly, so save it as `approved_vendors.csv` first.

**Step 2: Create an internal stage**

```sql
CREATE OR REPLACE STAGE FINANCE_AUDIT.ACCOUNTS_PAYABLE.AUDIT_UPLOADS
  DIRECTORY = (ENABLE = TRUE);
```

`DIRECTORY = (ENABLE = TRUE)` keeps a browsable list of the files in the stage.

**Step 3: Upload the file**

Use the **Browse** button in the Snowflake web interface, or run `PUT` from a command-line tool such as SnowSQL. `PUT` does not work in a web worksheet.

```sql
PUT file:///Users/you/approved_vendors.csv @FINANCE_AUDIT.ACCOUNTS_PAYABLE.AUDIT_UPLOADS;
```

**Step 4: Load it into a table**

```sql
COPY INTO FINANCE_AUDIT.ACCOUNTS_PAYABLE.APPROVED_VENDORS
FROM @FINANCE_AUDIT.ACCOUNTS_PAYABLE.AUDIT_UPLOADS
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

Snowflake stores the file itself, so no outside bucket is needed.

## Stages Can Hold Any File Type

Tables only accept structured data (rows and columns). Stages accept **any file**, which makes them useful for keeping audit evidence next to the data, for example:

- Scanned PDFs of signed vendor contracts
- Images of approved invoices
- Bank statements received as PDFs

## Key Takeaway

| | External Stage | Internal Stage |
|---|---|---|
| **Where files live** | Your cloud storage (S3, Azure, Google Cloud) | Snowflake's own storage |
| **Best for** | Regular, ongoing files like nightly ledger exports | Quick, one-off files like a spreadsheet for one audit |
| **You pay for** | Your cloud storage | Snowflake storage |
| **Audit example** | Daily journal entry exports | Approved vendor list from procurement |
