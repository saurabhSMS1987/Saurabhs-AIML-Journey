# Reading Files with pandas: A Practical Guide to Real-World Data

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Sources:** The behaviour described here comes from the official **pandas documentation** (the [IO tools user guide](https://pandas.pydata.org/docs/user_guide/io.html) and the API reference for each reader), the **Python standard library documentation** for the [`csv` module](https://docs.python.org/3/library/csv.html) and [text encodings](https://docs.python.org/3/library/codecs.html#standard-encodings), and **[RFC 4180](https://www.rfc-editor.org/rfc/rfc4180)**, the CSV format specification. The full list is in [Sources](#sources). Every example was run and checked on **pandas 3.0.2 / Python 3.12**. The sample data is invented, and the examples come from banking, insurance, healthcare and utilities.

Reading a clean CSV takes one line. Real extracts are rarely clean: semicolons instead of commas, report titles above the header, totals at the bottom, commas inside addresses, notes that wrap onto a new line, IDs that lose their leading zeros, and files from Windows systems that won't decode. This guide covers each problem, how to spot it and how to fix it.

## How to use this guide

1. Run `python make_sample_files.py` to create every sample file in a `sample_data` folder.
2. Run the snippets from inside `sample_data`. Each one assumes `import pandas as pd`.

## Contents

1. [Look before you load](#1-look-before-you-load)
2. [Which reader for which format](#2-which-reader-for-which-format)
3. [Delimiters](#3-delimiters)
4. [Titles, comments and footers](#4-titles-comments-and-footers)
5. [Split lines and broken rows](#5-split-lines-and-broken-rows)
6. [Missing values, IDs and messy numbers](#6-missing-values-ids-and-messy-numbers)
7. [Dates](#7-dates)
8. [Encodings](#8-encodings)
9. [Fixed-width files](#9-fixed-width-files)
10. [Excel](#10-excel)
11. [JSON](#11-json)
12. [XML, Parquet, SQL and HTML](#12-xml-parquet-sql-and-html)
13. [Compressed files and many files at once](#13-compressed-files-and-many-files-at-once)
14. [Large files](#14-large-files)
15. [Check the data after reading it](#15-check-the-data-after-reading-it)
16. [Troubleshooting table](#16-troubleshooting-table)

---

## 1. Look before you load

Most reading errors are obvious once you see the raw text. Before calling any reader, print the first few lines exactly as they are stored:

```python
with open("claims_paid_report.csv", encoding="utf-8") as f:
    for _ in range(6):
        print(repr(f.readline()))
# 'ACME Health Insurance\n'      <- a title, not a header
# ...
# 'claim_id,amount\n'            <- the real header is on line 5
```

`repr()` shows hidden characters such as tabs (`\t`), Windows line endings (`\r\n`) and byte-order marks (`\ufeff`). For large files, `pd.read_csv(file, nrows=5)` gives a quick preview without loading everything.

## 2. Which reader for which format

| Format | Typical source | Reader | Extra library |
| --- | --- | --- | --- |
| CSV / TXT / TSV | ERP, billing and claims extracts | `pd.read_csv` | – |
| Fixed-width TXT | Mainframe and legacy policy systems | `pd.read_fwf` | – |
| Excel `.xlsx` | Reconciliations, tariff schedules | `pd.read_excel` | `openpyxl` |
| Excel `.xls` (old) | Older reports | `pd.read_excel` | `xlrd` |
| JSON / JSON Lines | APIs, smart meters, web apps | `pd.read_json`, `pd.json_normalize` | – |
| XML | Claims exchanges, regulatory filings | `pd.read_xml` | `lxml` |
| Parquet | Data lakes, analytics platforms | `pd.read_parquet` | `pyarrow` |
| SQL database | Core systems, data warehouses | `pd.read_sql_query` | driver, e.g. `sqlite3` |
| HTML tables | Published rates and tariffs | `pd.read_html` | `lxml` |

## 3. Delimiters

A delimiter is the character that separates fields. A comma is only the default, and many systems use something else.

### 3.1 Semicolons and European number formats

**Example: a German bank statement.** European exports often use `;` between fields because the comma is the decimal mark. Thousands are separated with dots, and dates are day first.

```text
Datum;Beschreibung;Betrag;Saldo
01.09.2026;Gehalt;3.250,00;5.410,75
03.09.2026;Miete;-1.200,00;4.210,75
```

```python
bank = pd.read_csv("bank_statement_eu.csv", sep=";", decimal=",", thousands=".",
                   parse_dates=["Datum"], dayfirst=True)
print(bank["Betrag"].sum())          # 1963.6: real numbers, not text
```

Without `decimal=","` and `thousands="."`, the amounts load as text such as `'3.250,00'`, and totals fail or come out wrong.

### 3.2 Pipe, tab and whitespace

**Pipe (`|`):** common in claims and billing extracts, because pipes rarely appear in names or addresses.

```python
claims = pd.read_csv("claims_extract.txt", sep="|")
```

**Tab (`\t`):** common in lab-system and database exports, usually with a `.tsv` extension.

```python
labs = pd.read_csv("lab_results.tsv", sep="\t")
```

**Variable spaces:** reports formatted to line up neatly on screen.

```text
METER_ID   REGION     KWH
M001       North      420
M002       North     3150
```

```python
meters = pd.read_csv("meter_report_aligned.txt", sep=r"\s+")   # one or more spaces or tabs
```

The old `delim_whitespace=True` option was deprecated in pandas 2.2 and no longer exists in pandas 3.0, so use `sep=r"\s+"` instead.

### 3.3 Unknown delimiter: let Python detect it

When files arrive from many vendors, `sep=None` asks pandas to detect the delimiter. This uses Python's `csv.Sniffer` on the first valid row and needs the Python engine:

```python
vendors = pd.read_csv("vendor_list.csv", sep=None, engine="python")
print(vendors.columns.tolist())      # ['vendor_id', 'vendor_name', 'bank_account']
```

To check the delimiter yourself first:

```python
import csv
with open("vendor_list.csv", encoding="utf-8") as f:
    print(csv.Sniffer().sniff(f.read(1024)).delimiter)   # ;
```

Detection works from a sample, so confirm the column count afterwards. One unusual first row can mislead it.

### 3.4 Multi-character delimiters

**Example: a legacy policy system using `~|~` between fields.** Any separator longer than one character is treated as a **regular expression**, so special characters like `|` must be escaped with `\`:

```text
POLICY~|~HOLDER~|~PREMIUM
P101~|~Anita Rao~|~1200.50
```

```python
legacy = pd.read_csv("policies_legacy.txt", sep=r"~\|~", engine="python")
```

### 3.5 Several different delimiters in one file

**Example: meter readings merged from two systems.** One system used commas, the other used semicolons, and one row even mixes both:

```text
meter_id,reading_date,kwh
M001,2026-09-30,420
M002;2026-09-30;3150
M003,2026-09-30;2875
```

A regular expression *character class* accepts either:

```python
readings = pd.read_csv("readings_mixed.txt", sep=r"[;,]", engine="python")
print(readings.shape)                # (3, 3): every row split correctly
```

> [!WARNING]
> The pandas documentation notes that regex delimiters are *prone to ignoring quoted data*. If a quoted value contains `;` or `,`, as in `"Smith, John"`, a regex separator will split it anyway. In that case, fix the file at source, or standardise each system's extract before combining them.

### 3.6 Delimiters inside values: quoting

**Example: provider addresses that contain commas.** Under RFC 4180, a field containing the delimiter must be wrapped in double quotes, and pandas respects this by default:

```text
provider_id,name,address
PR01,City Hospital,"12, Main Street, Springfield"
```

```python
providers = pd.read_csv("providers.csv")
print(providers["address"][0])       # 12, Main Street, Springfield
```

If a system uses a different quote character, set `quotechar="'"`. If quotes inside values are escaped with a backslash, set `escapechar="\\"`.

## 4. Titles, comments and footers

**Example: a claims report exported from a reporting tool.** It has a title block on top, a comment line in the middle and control totals at the bottom:

```text
ACME Health Insurance
Claims Paid Report
Run date: 30/10/2026

claim_id,amount
C1,1200.00
# manual adjustment removed by ops
C2,850.50
C3,4300.00
TOTAL,6350.50
Record count: 3
```

```python
report = pd.read_csv("claims_paid_report.csv",
                     skiprows=4,          # skip the 4 lines above the header
                     skipfooter=2,        # skip the 2 trailer lines
                     comment="#",         # ignore lines starting with #
                     engine="python")     # skipfooter needs the Python engine
print(report)                             # 3 clean rows: C1, C2, C3
```

**Use the trailer; don't just throw it away.** The control totals let you prove the extract is complete, which is a basic audit check:

```python
with open("claims_paid_report.csv", encoding="utf-8") as f:
    lines = f.read().splitlines()

control_total = float(lines[-2].split(",")[1])        # 6350.50
control_count = int(lines[-1].split(":")[1])          # 3

print(len(report) == control_count)                   # True: no rows lost
print(round(report["amount"].sum(), 2) == control_total)   # True: amounts complete
```

Other useful options are `header=None` with `names=[...]` for files with no header row, `skiprows=[0, 2]` to skip specific lines, and `skip_blank_lines=True`, which is the default.

## 5. Split lines and broken rows

This is where most data quality problems hide. Some errors stop pandas with a `ParserError`, but others load **silently** with values in the wrong columns.

### 5.1 Legitimate line breaks inside quoted fields

**Example: adjuster notes typed over several lines.** RFC 4180 allows line breaks inside a quoted field, and pandas handles it automatically:

```text
claim_id,notes,amount
C1,"Water damage in kitchen.
Insured called twice for update.",5000
C2,"Theft of laptop",1200
```

```python
notes = pd.read_csv("adjuster_notes.csv")
print(len(notes))                    # 2: the two-line note stays in one record
```

### 5.2 Unquoted line breaks: the silent problem

**Example: customer complaints from a utility CRM.** The description field contains a line break but no quotes, so one record is split across two lines:

```text
complaint_id|customer|description|amount
CP1|Anita|Bill too high|120.50
CP2|Rahul|Meter reading wrong
customer says an estimate was used|88.00
CP3|Maria|Late payment fee|15.00
```

pandas reads it **without any error**: short rows are simply padded with `NaN`.

```python
bad = pd.read_csv("complaints_broken.txt", sep="|")
print(len(bad))                      # 4 rows instead of 3
# row 2: "customer says an estimate was used" ends up in complaint_id, and 88.00 in customer
```

**Fix:** rebuild each record by joining lines until it has the expected number of delimiters:

```python
import io

def repair_split_lines(path, sep="|", encoding="utf-8"):
    """Join physical lines until each record has as many delimiters as the header."""
    with open(path, encoding=encoding) as f:
        lines = f.read().splitlines()
    expected = lines[0].count(sep)
    fixed, buffer = [lines[0]], ""
    for line in lines[1:]:
        buffer = f"{buffer} {line}" if buffer else line
        if buffer.count(sep) >= expected:
            fixed.append(buffer)
            buffer = ""
    if buffer:                       # leftover text: keep it visible, don't drop it
        fixed.append(buffer)
    return "\n".join(fixed)

complaints = pd.read_csv(io.StringIO(repair_split_lines("complaints_broken.txt")), sep="|")
print(len(complaints))                            # 3
print(complaints.loc[1, "description"])           # Meter reading wrong customer says an estimate was used
print(complaints.loc[1, "amount"])                # 88.0
```

This works when the delimiter never appears inside the text itself. Always compare the repaired row count with the source system's record count.

### 5.3 Rows with too many fields

**Example: patient addresses with an unquoted comma.** Here pandas *does* stop:

```text
patient_id,name,city
P1,Anita Rao,Pune
P2,Rahul Mehta,Mumbai, Andheri East
P3,Maria Gomez,Delhi
```

```python
# pd.read_csv("patients_bad_rows.csv")
# ParserError: Error tokenizing data. C error: Expected 3 fields in line 3, saw 4
```

The `on_bad_lines` option controls what happens next:

| Setting | Effect | When to use it |
| --- | --- | --- |
| `"error"` (default) | Stops with a `ParserError` | You need to know about every problem |
| `"warn"` | Skips the row and prints a warning | Quick exploration only |
| `"skip"` | Skips the row silently | Rarely, because rows vanish without trace |
| A function | You decide row by row (Python engine only) | Capturing or repairing bad rows |

In audit work, silently dropping rows is the worst option. Capture them instead:

```python
rejected = []

def capture(bad_line):
    rejected.append(bad_line)        # keep it for the exceptions log
    return None                      # returning None drops it from the DataFrame

patients = pd.read_csv("patients_bad_rows.csv", on_bad_lines=capture, engine="python")
print(len(patients), rejected)       # 2 [['P2', 'Rahul Mehta', 'Mumbai', ' Andheri East']]
```

Or repair the row if you know the pattern. Here, the extra pieces belong to the last column:

```python
def merge_extra_into_city(bad_line):
    return bad_line[:2] + [",".join(bad_line[2:])]

patients = pd.read_csv("patients_bad_rows.csv", on_bad_lines=merge_extra_into_city, engine="python")
print(patients.loc[1, "city"])       # Mumbai, Andheri East
```

### 5.4 A delimiter at the end of every line

**Example: a meter export where each data row ends with a comma, but the header doesn't.** pandas sees one more field than column names and quietly turns the first column into the index, so every value shifts:

```text
meter_id,kwh
M001,420,
M002,3150,
```

```python
print(pd.read_csv("trailing_delim.csv"))                   # meter_id becomes the index, kwh fills with NaN
print(pd.read_csv("trailing_delim.csv", index_col=False))  # correct: meter_id 420 / 3150
```

`index_col=False` is the fix recommended in the `read_csv` documentation for exactly this case.

## 6. Missing values, IDs and messy numbers

**Example: a premium register exported from a policy administration system.**

```text
policy_no,holder,premium,adjustment,paid_flag
000123,Anita Rao,"$1,200.00",(150.00),Y
004567,Rahul Mehta,"$860.00",N/A,N
007788,Maria Gomez,-,NULL,Y
```

There are four problems in five columns:

```python
reg = pd.read_csv(
    "premium_register.csv",
    dtype={"policy_no": str},              # 1. keep leading zeros: 000123, not 123
    na_values=["N/A", "NULL", "-"],        # 2. treat these markers as missing
    true_values=["Y"], false_values=["N"], # 3. Y/N becomes True/False
)

# 4. currency text and accounting-style negatives
reg["premium"] = reg["premium"].str.replace(r"[$,]", "", regex=True).astype(float)
reg["adjustment"] = (reg["adjustment"]
                     .str.replace(r"^\((.*)\)$", r"-\1", regex=True)    # (150.00) -> -150.00
                     .astype(float))

print(reg["policy_no"].tolist())     # ['000123', '004567', '007788']
print(reg["premium"].tolist())       # [1200.0, 860.0, nan]
print(reg["adjustment"].tolist())    # [-150.0, nan, nan]
print(reg.isnull().sum().to_dict())  # {'policy_no': 0, 'holder': 0, 'premium': 1, 'adjustment': 2, 'paid_flag': 0}
```

**Why leading zeros matter:** without `dtype=str`, policy `000123` becomes the number `123` and no longer matches the policy master. The same applies to account numbers, ZIP and postal codes, NHS and medical record numbers, and meter serials. Read every **identifier** as text.

**`thousands=","`** handles plain numbers like `1,200.50`, but not currency symbols or brackets. Those need cleaning, as shown above.

In pandas 3.0, text columns load with the new `str` dtype by default, instead of the old `object` dtype.

## 7. Dates

**Example: hospital admissions with day-first dates, and one impossible date.**

```text
admission_id,admit_date,discharge_date
A1,05/09/2026,08/09/2026
A3,30/09/2026,31/02/2026
```

`05/09/2026` is 5 September in the UK and India, but 9 May in the US. **Always state the format.** Don't let pandas guess it.

```python
adm = pd.read_csv("admissions.csv")
for col in ["admit_date", "discharge_date"]:
    adm[col] = pd.to_datetime(adm[col], format="%d/%m/%Y", errors="coerce")

print(adm.loc[0, "admit_date"].date())                         # 2026-09-05
print(adm[adm["discharge_date"].isnull()]["admission_id"].tolist())   # ['A3']: 31 February doesn't exist
```

`errors="coerce"` turns invalid dates into `NaT` (missing) instead of stopping, so you can **list them as exceptions**. For simple cases, `parse_dates=[...]` with `dayfirst=True` or `date_format="%d/%m/%Y"` inside `read_csv` also works.

## 8. Encodings

**Example: a supplier list exported from an older Windows system.**

```python
# pd.read_csv("suppliers_cp1252.csv")
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 17
suppliers = pd.read_csv("suppliers_cp1252.csv", encoding="cp1252")
print(suppliers["supplier"].tolist())   # ['Café Müller', 'Société Générale']
```

| Encoding | Where you'll meet it |
| --- | --- |
| `utf-8` | The modern default, and pandas' default |
| `utf-8-sig` | UTF-8 with a byte-order mark (BOM), common from Excel's "CSV UTF-8" option |
| `cp1252` | Older Windows exports in Western Europe and the Americas |
| `latin-1` | Older Unix and European systems. It never fails to decode, but may decode wrongly |

**The byte-order mark (BOM).** pandas removes it automatically, but Python's own `csv` module doesn't, so the first column name gets a hidden character:

```python
import csv
with open("export_with_bom.csv", encoding="utf-8") as f:
    print(next(csv.reader(f)))       # ['\ufeffid', 'amount']: 'id' won't match!
with open("export_with_bom.csv", encoding="utf-8-sig") as f:
    print(next(csv.reader(f)))       # ['id', 'amount']
```

`encoding_errors="replace"` lets a file load even with a few undecodable bytes. Only use it once you know which records are affected, because it changes the data.

## 9. Fixed-width files

**Example: a mainframe policy file.** There are no delimiters, just columns at fixed positions. The premium has **two implied decimal places**: `000120050` means 1,200.50.

```text
P0001234ANITA RAO           20260115000120050
P0005678RAHUL MEHTA         20260201000086000
```

```python
policies = pd.read_fwf(
    "policies_fixed_width.txt",
    colspecs=[(0, 8), (8, 28), (28, 36), (36, 45)],   # start and end position of each field
    names=["policy", "holder", "start_date", "premium_cents"],
    dtype={"policy": str, "start_date": str},
)
policies["start_date"] = pd.to_datetime(policies["start_date"], format="%Y%m%d")
policies["premium"] = policies["premium_cents"] / 100     # apply the implied decimals

print(policies["premium"].tolist())  # [1200.5, 860.0, 15000.75]
```

Positions come from the system's **file layout** (or "copybook") document, so always ask for it. If you guess the positions, a field can shift by one character without any error.

## 10. Excel

**Example: a premium register with a title block above the header and one sheet per quarter.**

```python
q1 = pd.read_excel("premiums_2026.xlsx", sheet_name="Q1", header=2)   # header is on row 3
print(q1.columns.tolist())           # ['policy', 'premium']

# every sheet at once: returns a dictionary of {sheet name: DataFrame}
sheets = pd.read_excel("premiums_2026.xlsx", sheet_name=None, header=2)
print(list(sheets))                  # ['Q1', 'Q2']

all_quarters = (pd.concat(sheets, names=["quarter", "row"])
                .reset_index(level="quarter")
                .reset_index(drop=True))
print(all_quarters)                  # 4 rows, with a 'quarter' column showing each row's source sheet
```

Other useful options:

- `usecols="A:C"` reads only certain columns.
- `dtype={"policy": str}` keeps ID formats.
- `nrows` limits the rows read.

> [!TIP]
> Excel files hide traps: merged cells become `NaN` on every row except the first, formulas load as their last *saved* values, and hidden rows and sheets are still read. Check row counts against what you see in Excel.

## 11. JSON

**Example: a smart-meter API returning nested data.** Each meter has a customer object and a list of readings:

```json
[{"meter_id": "M001",
  "customer": {"id": "C101", "region": "North"},
  "readings": [{"date": "2026-09-29", "kwh": 14.2}, {"date": "2026-09-30", "kwh": 13.8}]}]
```

`pd.read_json` keeps the nested parts as lists and dictionaries, which isn't useful for analysis. `pd.json_normalize` flattens them into one row per reading:

```python
import json

with open("smart_meters.json", encoding="utf-8") as f:
    data = json.load(f)

flat = pd.json_normalize(
    data,
    record_path="readings",                                   # one row per reading
    meta=["meter_id", ["customer", "id"], ["customer", "region"]],
)
print(flat.columns.tolist())   # ['date', 'kwh', 'meter_id', 'customer.id', 'customer.region']
print(flat.groupby("meter_id")["kwh"].sum().to_dict())   # {'M001': 28.0, 'M002': 0.0}: M002 reads zero, so check the meter
```

**JSON Lines** (one JSON record per line) is common for event logs and streaming data:

```python
outages = pd.read_json("outage_events.jsonl", lines=True)
print(outages.shape)                 # (3, 3)
```

## 12. XML, Parquet, SQL and HTML

**XML: a claims exchange file.** `xpath` selects the repeating element, and attributes such as `id` become columns:

```python
xml_claims = pd.read_xml("claims.xml", xpath="//claim")
print(xml_claims.columns.tolist())   # ['id', 'patient', 'amount']
```

**Parquet: a data-lake extract.** Parquet files store column types, so IDs, dates and decimals arrive exactly as saved. Read only the columns you need:

```python
pq = pd.read_parquet("claims.parquet", columns=["claim_id", "paid"])   # needs pyarrow
```

**SQL: a billing database.** Always pass filter values as **parameters** rather than pasting them into the query text. That's safer, and it handles quotes in names correctly:

```python
import sqlite3

with sqlite3.connect("billing.db") as con:
    north = pd.read_sql_query("SELECT * FROM invoices WHERE region = ?", con, params=("North",))
print(north["invoice_id"].tolist())  # ['I1', 'I3']
```

**HTML: a published tariff table.** `read_html` returns a **list** of every table on the page, and `match` picks tables containing certain text:

```python
tables = pd.read_html("tariffs.html", match="Residential")
tariffs = tables[0]
print(tariffs.shape)                 # (3, 2)
```

## 13. Compressed files and many files at once

**Compressed files:** pandas detects compression from the file extension (`.gz`, `.zip`, `.bz2`, `.xz`, `.zst`). A `.zip` must contain only one file:

```python
gz = pd.read_csv("claims_extract.txt.gz", sep="|")
zp = pd.read_csv("claims_extract.zip", sep="|")
print(gz.shape, zp.shape)            # (3, 6) (3, 6)
```

**One file per month:** read them all, and **record which file each row came from**, so every exception can be traced back to its source:

```python
import glob
from pathlib import Path

files = sorted(glob.glob("monthly/meter_*.csv"))
monthly = pd.concat(
    [pd.read_csv(f).assign(source_file=Path(f).name) for f in files],
    ignore_index=True,
)
print(monthly["source_file"].value_counts().to_dict())
# {'meter_2026_07.csv': 2, 'meter_2026_08.csv': 2, 'meter_2026_09.csv': 2}
```

## 14. Large files

**Example: a 100,000-row claims file.** Three techniques keep memory down:

```python
# 1. preview the first rows only
pd.read_csv("big_claims.csv", nrows=5)

# 2. load only the columns you need, with compact types
slim = pd.read_csv("big_claims.csv", usecols=["status", "amount"], dtype={"status": "category"})
# memory: about 0.9 MB instead of about 4.4 MB for the full file

# 3. process in chunks and keep running totals
totals, rows = {}, 0
for chunk in pd.read_csv("big_claims.csv", usecols=["status", "amount"], chunksize=25_000):
    rows += len(chunk)
    for status, amount in chunk.groupby("status")["amount"].sum().items():
        totals[status] = totals.get(status, 0) + amount

print(rows)                          # 100000: confirms every row was processed
```

Chunked totals match a full-file read exactly. Chunking only changes how much is held in memory at once.

## 15. Check the data after reading it

Reading without errors doesn't mean reading correctly. These checks catch the silent problems from sections 5 to 8:

```python
def check_extract(df, expected_rows=None, id_col=None, amount_col=None, expected_total=None):
    print("Rows, columns:", df.shape)
    print("Column types:", df.dtypes.astype(str).to_dict())
    print("Missing values:", df.isnull().sum()[lambda s: s > 0].to_dict())
    if id_col:
        print("Duplicate IDs:", df[id_col].duplicated().sum())
    if expected_rows is not None:
        print("Row count matches control:", len(df) == expected_rows)
    if amount_col and expected_total is not None:
        print("Total matches control:", round(df[amount_col].sum(), 2) == expected_total)

check_extract(report, expected_rows=3, id_col="claim_id", amount_col="amount", expected_total=6350.50)
```

Things to confirm every time:

- **Row count** matches the source system or the trailer record.
- **Totals** match control totals.
- **Amount columns are numeric**, not text.
- **IDs are text**, with leading zeros intact.
- **Dates parsed correctly**, with day and month the right way round.
- **No unexpected `NaN`s**, which are often a sign of split lines or shifted columns.
- **No unnamed columns** like `Unnamed: 5`, which are often a sign of trailing delimiters.

## 16. Troubleshooting table

| Symptom or error | Likely cause | Fix |
| --- | --- | --- |
| Everything lands in one column | Wrong delimiter | `sep=";"`, `"\|"`, `"\t"`, or `sep=None, engine="python"` |
| `ParserError: Expected 3 fields ... saw 4` | Unquoted delimiter inside a value | Fix quoting at source, or `on_bad_lines=` with a function |
| Extra rows, values in the wrong columns, unexpected `NaN` | Unquoted line breaks | Repair the lines first (section 5.2) |
| First column became the index, values shifted | Trailing delimiter on data rows | `index_col=False` |
| `Unnamed: 0` column | Index saved with the file, or a trailing delimiter in the header | `index_col=0`, or drop the column |
| `UnicodeDecodeError` | File isn't UTF-8 | `encoding="cp1252"` or `"latin-1"` |
| First column named `\ufeffid` | Byte-order mark | `encoding="utf-8-sig"` |
| `000123` became `123` | ID read as a number | `dtype={"col": str}` |
| Amounts are text, e.g. `'3.250,00'` | European format, or currency symbols | `decimal=","`, `thousands="."`, or clean with `.str.replace` |
| Day and month swapped | Ambiguous date format | `pd.to_datetime(..., format="%d/%m/%Y")` |
| Report title used as the header | Lines above the header | `skiprows=n` |
| A totals row counted as data | Footer lines | `skipfooter=n, engine="python"` |
| Memory error | File too large | `usecols`, `dtype`, `chunksize` |

## Sources

**pandas documentation**

- [IO tools (text, CSV, HDF5, …) user guide](https://pandas.pydata.org/docs/user_guide/io.html)
- [`pandas.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html): `sep`, regex delimiters, `on_bad_lines`, `skipfooter`, `index_col=False`, `chunksize`, encoding options
- [`pandas.read_fwf`](https://pandas.pydata.org/docs/reference/api/pandas.read_fwf.html)
- [`pandas.read_excel`](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)
- [`pandas.read_json`](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html) and [`pandas.json_normalize`](https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html)
- [`pandas.read_xml`](https://pandas.pydata.org/docs/reference/api/pandas.read_xml.html)
- [`pandas.read_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)
- [`pandas.read_sql_query`](https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html)
- [`pandas.read_html`](https://pandas.pydata.org/docs/reference/api/pandas.read_html.html)
- [`pandas.to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)

**Python documentation**

- [`csv` module](https://docs.python.org/3/library/csv.html), including `csv.Sniffer` for delimiter detection
- [Standard encodings](https://docs.python.org/3/library/codecs.html#standard-encodings): `utf-8-sig`, `cp1252`, `latin-1`

**Standards**

- [RFC 4180: Common Format and MIME Type for CSV Files](https://www.rfc-editor.org/rfc/rfc4180), covering quoting rules and line breaks inside quoted fields

**Verification:** every snippet was run against the files created by `make_sample_files.py` on pandas 3.0.2 and Python 3.12. Commented outputs are the actual results.
