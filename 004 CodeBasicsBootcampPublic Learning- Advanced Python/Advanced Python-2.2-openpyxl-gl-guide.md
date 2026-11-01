# openpyxl for General Ledger Analysis: A Practical Guide

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Sources:** Features and syntax come from the official **openpyxl documentation** ([openpyxl.readthedocs.io](https://openpyxl.readthedocs.io/en/stable/)): the [tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html), [simple usage](https://openpyxl.readthedocs.io/en/stable/usage.html), [styles](https://openpyxl.readthedocs.io/en/stable/styles.html), [conditional formatting](https://openpyxl.readthedocs.io/en/stable/formatting.html), [data validation](https://openpyxl.readthedocs.io/en/stable/validation.html), [tables](https://openpyxl.readthedocs.io/en/stable/worksheet_tables.html), [defined names](https://openpyxl.readthedocs.io/en/stable/defined_names.html), [charts](https://openpyxl.readthedocs.io/en/stable/charts/introduction.html) and [optimised modes](https://openpyxl.readthedocs.io/en/stable/optimized.html). The `pandas` hand-off follows the [pandas `read_excel` documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html). The full list is in [Sources](#sources). Every example was run and checked on **openpyxl 3.1.5, pandas 3.0 and Python 3.12**. The workbook is invented sample data.

Excel is still where most audit evidence lives: client ledger extracts, trial balances and our own workpapers. **openpyxl** lets Python read those files cell by cell, test every row, and write a formatted, formula-driven workpaper back out. This guide works through a full journal entry (JE) testing exercise: read a messy client general ledger (GL), test it, then build a reviewer-ready workpaper with formulas, tables, conditional formatting, dropdowns, comments, links, charts, protection and print settings.

## How to use this guide

1. Run `python make_gl_workbook.py` to create `sample_data/client_gl_fy2026.xlsx`. It has a GL detail sheet with 1,236 lines (618 journal entries) below a merged title block, plus a trial balance and a chart of accounts. Several audit issues are hidden in it.
2. Run the snippets **in order**. Each section builds on the last, and the finished workpaper is saved to `output/je_testing_workpaper.xlsx`.

## Contents

**Part 1: Reading client workbooks**
1. [Setup and key ideas](#1-setup-and-key-ideas)
2. [Opening a workbook and finding the data](#2-opening-a-workbook-and-finding-the-data)
3. [Reading rows into Python](#3-reading-rows-into-python)
4. [Cleaning what you read](#4-cleaning-what-you-read)

**Part 2: Testing the general ledger**

5. [Journal entry tests](#5-journal-entry-tests)
6. [Reconciling the GL to the trial balance](#6-reconciling-the-gl-to-the-trial-balance)
7. [Handing off to pandas](#7-handing-off-to-pandas)

**Part 3: Building the workpaper**

8. [Creating a workbook and writing data](#8-creating-a-workbook-and-writing-data)
9. [Number formats, column widths and freeze panes](#9-number-formats-column-widths-and-freeze-panes)
10. [Styles: fonts, fills, borders and named styles](#10-styles-fonts-fills-borders-and-named-styles)
11. [Formulas and defined names](#11-formulas-and-defined-names)
12. [Excel tables and filters](#12-excel-tables-and-filters)
13. [Conditional formatting](#13-conditional-formatting)
14. [Data validation dropdowns](#14-data-validation-dropdowns)
15. [Comments and hyperlinks](#15-comments-and-hyperlinks)
16. [Charts](#16-charts)
17. [Layout: inserting, merging, grouping and hiding](#17-layout-inserting-merging-grouping-and-hiding)
18. [Protection](#18-protection)
19. [Print setup](#19-print-setup)
20. [Saving and checking the workpaper](#20-saving-and-checking-the-workpaper)

**Part 4: Going further**

21. [Large files: read-only and write-only modes](#21-large-files-read-only-and-write-only-modes)
22. [Editing an existing client file safely](#22-editing-an-existing-client-file-safely)
23. [What openpyxl can and can't do](#23-what-openpyxl-can-and-cant-do)
24. [Troubleshooting](#24-troubleshooting)
25. [Sources](#sources)

---

# Part 1: Reading client workbooks

## 1. Setup and key ideas

```bash
pip install openpyxl pandas
```

```python
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string

SOURCE = Path("sample_data/client_gl_fy2026.xlsx")
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)
```

**Three objects do almost everything:**

| Object | What it is | How you get it |
| --- | --- | --- |
| `Workbook` | The whole `.xlsx` file | `load_workbook(path)` or `Workbook()` |
| `Worksheet` | One tab | `wb["GL Detail"]`, `wb.active`, `wb.create_sheet()` |
| `Cell` | One cell, with `.value`, `.number_format`, `.font` and more | `ws["C5"]` or `ws.cell(row=5, column=3)` |

**Coordinates:** rows and columns start at **1**, not 0. Letters and numbers convert both ways:

```python
print(get_column_letter(7), column_index_from_string("L"))   # G 12
```

openpyxl reads and writes **`.xlsx`, `.xlsm`, `.xltx` and `.xltm`**. It doesn't open old `.xls` files, and it doesn't **calculate** formulas (more on that in section 11).

## 2. Opening a workbook and finding the data

```python
wb = load_workbook(SOURCE)
print(wb.sheetnames)                 # ['GL Detail', 'Trial Balance', 'Chart of Accounts']

ws = wb["GL Detail"]
print(ws.dimensions)                 # A1:L1240: the used range
print(ws.max_row, ws.max_column)     # 1240 12
print(ws["A1"].value)                # AtliQ Retail Ltd: a title, not data
print(sorted(str(r) for r in ws.merged_cells.ranges))   # ['A1:L1', 'A2:L2']
```

Client extracts rarely start in cell A1. **Find the header row** instead of assuming it:

```python
header_row = next(r for r in range(1, 21) if ws.cell(row=r, column=1).value == "JE ID")
headers = [cell.value for cell in ws[header_row]]
col = {name: i for i, name in enumerate(headers)}     # column name -> position in each row

print(header_row)        # 4
print(headers[:6])       # ['JE ID', 'Line', 'Posting Date', 'Posted At', 'Account', 'Account Name']
```

**Ways to reach cells:**

| Code | Returns |
| --- | --- |
| `ws["G5"]` | One cell |
| `ws.cell(row=5, column=7)` | The same cell, by numbers |
| `ws["A4:L4"]` | A tuple of rows of cells |
| `ws["G"]` | Every cell in column G |
| `ws[5]` | Every cell in row 5 |
| `ws.iter_rows(min_row=5, values_only=True)` | Rows of plain values (fastest for data) |
| `ws.iter_cols(min_col=7, max_col=8)` | Columns of cells |

## 3. Reading rows into Python

```python
gl_rows = list(ws.iter_rows(min_row=header_row + 1, values_only=True))
print(len(gl_rows))                         # 1236

first = gl_rows[0]
print(first[col["JE ID"]], first[col["Account"]], type(first[col["Posting Date"]]).__name__)
# JE00024 5000 datetime: Excel dates arrive as Python datetimes
```

`values_only=True` returns plain values, not `Cell` objects, which is faster and simpler for analysis. Without it, each item is a `Cell`, so you can also read its formatting, such as `cell.number_format` or `cell.font.bold`.

**Merged cells:** only the top-left cell of a merged range holds the value. The other cells read as `None`.

## 4. Cleaning what you read

Client exports often contain **numbers stored as text**, like `"7,076.45"`. They look fine in Excel but break every total:

```python
text_amounts = [(r[col["JE ID"]], r[col["Debit"]]) for r in gl_rows if isinstance(r[col["Debit"]], str)]
print(text_amounts)        # [('JE00024', '7,076.45'), ('JE00039', '11,726.95')]

def to_number(value):
    """Convert ledger amounts to float: blanks to 0, and text like '7,076.45' to 7076.45."""
    if value is None:
        return 0.0
    if isinstance(value, str):
        return float(value.replace(",", "").strip())
    return float(value)

gl = [
    {
        "je_id": r[col["JE ID"]],
        "date": r[col["Posting Date"]],
        "posted_at": r[col["Posted At"]],
        "account": str(r[col["Account"]]),
        "debit": to_number(r[col["Debit"]]),
        "credit": to_number(r[col["Credit"]]),
        "preparer": r[col["Preparer"]],
        "approver": r[col["Approver"]],
        "source": r[col["Source"]],
        "description": r[col["Description"]],
        "excel_row": header_row + 1 + i,              # keep the source row for audit trail links
    }
    for i, r in enumerate(gl_rows)
]
print(round(sum(line["debit"] for line in gl), 2), round(sum(line["credit"] for line in gl), 2))
# 5316863.08 5316363.08
```

The debit and credit totals differ by 500. Section 5 finds the journal entry that causes it.

Keeping `excel_row` means every exception can be traced back to the exact row in the client's file.

---

# Part 2: Testing the general ledger

## 5. Journal entry tests

Each test adds rows to one `exceptions` list. That list becomes the workpaper's Exceptions sheet in Part 3.

```python
exceptions = []

def flag(test, line, detail):
    exceptions.append({"test": test, "je_id": line["je_id"], "date": line["date"],
                       "account": line["account"], "amount": max(line["debit"], line["credit"]),
                       "preparer": line["preparer"], "detail": detail, "gl_row": line["excel_row"]})

# group lines into journal entries
entries = defaultdict(list)
for line in gl:
    entries[line["je_id"]].append(line)

APPROVAL_LIMIT = 10_000
for je_id, lines in entries.items():
    debit_line = lines[0]
    difference = round(sum(l["debit"] for l in lines) - sum(l["credit"] for l in lines), 2)

    if difference != 0:
        flag("Unbalanced entry", debit_line, f"Debits exceed credits by {difference:,.2f}")
    if debit_line["source"] == "Manual" and not debit_line["approver"]:
        flag("No approver", debit_line, "Manual entry with no approver recorded")
    if debit_line["date"].weekday() >= 5:
        flag("Weekend posting", debit_line, f"Posted on a {debit_line['date']:%A}")
    if debit_line["posted_at"].hour >= 22 or debit_line["posted_at"].hour < 6:
        flag("After-hours posting", debit_line, f"Posted at {debit_line['posted_at']:%H:%M}")
    if debit_line["source"] == "Manual" and 9_500 <= debit_line["debit"] < APPROVAL_LIMIT:
        flag("Just below approval limit", debit_line, f"{debit_line['debit']:,.2f} vs limit {APPROVAL_LIMIT:,}")
    if debit_line["source"] == "Manual" and debit_line["debit"] >= 10_000 and debit_line["debit"] % 5_000 == 0:
        flag("Round amount", debit_line, f"Exactly {debit_line['debit']:,.0f}")
    if any(l["account"] == "1999" for l in lines):
        flag("Suspense account", debit_line, "Posts to suspense account 1999")

summary = defaultdict(int)
for e in exceptions:
    summary[e["test"]] += 1
print(dict(sorted(summary.items())))
# {'After-hours posting': 9, 'Just below approval limit': 15, 'No approver': 3, 'Round amount': 7,
#  'Suspense account': 1, 'Unbalanced entry': 1, 'Weekend posting': 6}
print(len(exceptions), "exceptions across", len({e["je_id"] for e in exceptions}), "journal entries")
# 42 exceptions across 30 journal entries
```

## 6. Reconciling the GL to the trial balance

Reading the client's trial balance from the same workbook, then comparing it with balances rebuilt from the GL:

```python
tb_ws = wb["Trial Balance"]
tb = {str(acct): bal for acct, name, bal in tb_ws.iter_rows(min_row=2, values_only=True)}
names = {str(acct): name for acct, name, bal in tb_ws.iter_rows(min_row=2, values_only=True)}

gl_balance = defaultdict(float)
for line in gl:
    gl_balance[line["account"]] += line["debit"] - line["credit"]

recon = [(acct, names[acct], round(gl_balance[acct], 2), tb[acct], round(tb[acct] - gl_balance[acct], 2))
         for acct in tb]
differences = [r for r in recon if r[4] != 0]
print(differences)
# [('4000', 'Product Revenue', -1903655.41, -1928655.41, -25000.0)]
```

Product Revenue differs by 25,000: the trial balance shows 25,000 more revenue (a larger credit) than the ledger supports. That goes straight onto the workpaper.

## 7. Handing off to pandas

openpyxl is the right tool for cell-level reading and formatted output. For heavy grouping and statistics, pass the data to **pandas**, which uses openpyxl underneath to read `.xlsx` files:

```python
import pandas as pd

df = pd.read_excel(SOURCE, sheet_name="GL Detail", header=header_row - 1,   # header=3 means the 4th row
                   dtype={"Account": str})
df["Debit"] = df["Debit"].map(to_number)                                    # same text-to-number fix
print(df.shape)                                                            # (1236, 12)
print(df.groupby("Source")["Debit"].sum().round(0).to_dict())   # {'Automated': 4202120.0, 'Manual': 1114744.0}
```

You can also build a DataFrame straight from rows you've already read: `pd.DataFrame(gl_rows, columns=headers)`. Going the other way, `openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)` writes a DataFrame into a worksheet you then format with openpyxl.

---

# Part 3: Building the workpaper

## 8. Creating a workbook and writing data

```python
out = Workbook()
summary_ws = out.active
summary_ws.title = "Summary"
exc_ws = out.create_sheet("Exceptions")
data_ws = out.create_sheet("GL Data")
recon_ws = out.create_sheet("TB Rec")
print(out.sheetnames)   # ['Summary', 'Exceptions', 'GL Data', 'TB Rec']

# Exceptions sheet: header row plus one row per exception
exc_headers = ["Test", "JE ID", "Date", "Account", "Amount", "Preparer", "Detail", "GL Row", "Status", "Reviewer Note"]
exc_ws.append(exc_headers)
for e in exceptions:
    exc_ws.append([e["test"], e["je_id"], e["date"], e["account"], e["amount"],
                   e["preparer"], e["detail"], e["gl_row"], "Open", None])

# GL Data sheet: the cleaned ledger, for reference and links
data_ws.append(["JE ID", "Date", "Account", "Debit", "Credit", "Preparer", "Approver", "Source", "Description"])
for line in gl:
    data_ws.append([line["je_id"], line["date"], line["account"], line["debit"], line["credit"],
                    line["preparer"], line["approver"], line["source"], line["description"]])

# TB Rec sheet
recon_ws.append(["Account", "Account Name", "Balance per GL", "Balance per TB", "Difference"])
for acct, name, gl_bal, tb_bal, diff in recon:
    recon_ws.append([acct, name, gl_bal, tb_bal, None])                    # difference becomes a formula later

print(exc_ws.max_row - 1, data_ws.max_row - 1, recon_ws.max_row - 1)   # 42 1236 13
```

`ws.append()` writes a list into the next empty row. To write one cell, assign to it: `ws["B2"] = 100` or `ws.cell(row=2, column=2, value=100)`.

## 9. Number formats, column widths and freeze panes

Values and formatting are separate: a number stays a number, and `number_format` controls how Excel displays it.

```python
ACCOUNTING = '#,##0.00;(#,##0.00);"-"'        # 1,250.00 | (1,250.00) for negatives | - for zero
DATE = "dd-mmm-yyyy"

def format_columns(ws, formats, widths):
    for letter, fmt in formats.items():
        for cell in ws[letter][1:]:            # skip the header
            cell.number_format = fmt
    for letter, width in widths.items():
        ws.column_dimensions[letter].width = width

format_columns(exc_ws, {"C": DATE, "E": ACCOUNTING},
               {"A": 26, "B": 10, "C": 13, "D": 9, "E": 14, "F": 11, "G": 42, "H": 8, "I": 18, "J": 30})
format_columns(data_ws, {"B": DATE, "D": ACCOUNTING, "E": ACCOUNTING},
               {"A": 10, "B": 13, "C": 9, "D": 14, "E": 14, "F": 11, "G": 11, "H": 11, "I": 30})
format_columns(recon_ws, {"C": ACCOUNTING, "D": ACCOUNTING, "E": ACCOUNTING},
               {"A": 10, "B": 24, "C": 16, "D": 16, "E": 14})

for sheet in (exc_ws, data_ws, recon_ws):
    sheet.freeze_panes = "A2"                 # keep the header visible while scrolling
print(exc_ws["E2"].number_format)          # #,##0.00;(#,##0.00);"-"
```

`freeze_panes = "B2"` would freeze both the first row and the first column. openpyxl can't auto-fit column widths the way Excel's double-click does, so set them explicitly.

## 10. Styles: fonts, fills, borders and named styles

```python
from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Side

NAVY = "1F2A44"
header_style = NamedStyle(name="wp_header")
header_style.font = Font(bold=True, color="FFFFFF")
header_style.fill = PatternFill(fill_type="solid", start_color=NAVY, end_color=NAVY)
header_style.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="BFC5D2")
header_style.border = Border(left=thin, right=thin, top=thin, bottom=thin)
out.add_named_style(header_style)            # register once, reuse anywhere

for sheet in (exc_ws, data_ws, recon_ws):
    for cell in sheet[1]:
        cell.style = "wp_header"
    sheet.row_dimensions[1].height = 22

print(exc_ws["A1"].font.bold, exc_ws["A1"].fill.start_color.rgb)   # True 001F2A44
```

| Class | Controls | Example |
| --- | --- | --- |
| `Font` | Name, size, bold, italic, colour | `Font(name="Calibri", size=11, bold=True, color="C00000")` |
| `PatternFill` | Cell background | `PatternFill("solid", start_color="FFF2CC")` |
| `Border` and `Side` | Cell borders | `Border(bottom=Side(style="medium"))` |
| `Alignment` | Position, wrapping, rotation | `Alignment(horizontal="right", wrap_text=True)` |
| `NamedStyle` | A reusable bundle of the above | Applied with `cell.style = "wp_header"` |

Style objects can't be changed once created. To change one property, create a new object, or copy the old one: `cell.font = cell.font.copy(bold=True)`.

## 11. Formulas and defined names

Write formulas as text starting with `=`, exactly as you'd type them in Excel. They stay **live**: if a reviewer edits an input, the workpaper updates.

```python
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import quote_sheetname, absolute_coordinate

# TB Rec: difference column as a live formula, plus totals
last = recon_ws.max_row
for r in range(2, last + 1):
    recon_ws[f"E{r}"] = f"=D{r}-C{r}"
recon_ws[f"B{last + 1}"] = "Total"
for letter in "CDE":
    recon_ws[f"{letter}{last + 1}"] = f"=SUM({letter}2:{letter}{last})"
    recon_ws[f"{letter}{last + 1}"].number_format = ACCOUNTING
    recon_ws[f"{letter}{last + 1}"].font = Font(bold=True)

# Summary: a labelled input cell, given a defined name so formulas can refer to it by name
summary_ws["A1"] = "Journal Entry Testing: AtliQ Retail Ltd, FY2026"
summary_ws["A1"].font = Font(bold=True, size=14, color=NAVY)
summary_ws["A3"], summary_ws["B3"] = "Approval limit (input)", APPROVAL_LIMIT
summary_ws["B3"].font = Font(color="0000FF")                       # blue = hardcoded input
summary_ws["B3"].number_format = "#,##0"

ref = f"{quote_sheetname(summary_ws.title)}!{absolute_coordinate('B3')}"
out.defined_names["ApprovalLimit"] = DefinedName("ApprovalLimit", attr_text=ref)

# Summary table: counts and values per test, pulled live from the Exceptions sheet
tests = sorted(summary)
summary_ws.append([])
summary_ws.append(["Test", "Exceptions", "Value", "Open"])
start = summary_ws.max_row + 1
for i, test in enumerate(tests, start=start):
    summary_ws[f"A{i}"] = test
    summary_ws[f"B{i}"] = f"=COUNTIF(Exceptions!$A:$A,A{i})"
    summary_ws[f"C{i}"] = f"=SUMIFS(Exceptions!$E:$E,Exceptions!$A:$A,A{i})"
    summary_ws[f"D{i}"] = f'=COUNTIFS(Exceptions!$A:$A,A{i},Exceptions!$I:$I,"Open")'
    summary_ws[f"C{i}"].number_format = ACCOUNTING
end = start + len(tests) - 1
summary_ws[f"A{end + 1}"] = "Total"
summary_ws[f"B{end + 1}"] = f"=SUM(B{start}:B{end})"
summary_ws[f"C{end + 1}"] = f"=SUM(C{start}:C{end})"
summary_ws[f"D{end + 1}"] = f"=SUM(D{start}:D{end})"
summary_ws[f"C{end + 1}"].number_format = ACCOUNTING
for cell in summary_ws[start - 1]:
    cell.style = "wp_header"
for cell in summary_ws[end + 1]:
    cell.font = Font(bold=True)

summary_ws[f"A{end + 3}"] = "GL debit lines at or above the approval limit"
summary_ws[f"B{end + 3}"] = "=COUNTIF('GL Data'!$D:$D,\">=\"&ApprovalLimit)"   # uses the defined name
summary_ws.column_dimensions["A"].width = 38
for letter in "BCD":
    summary_ws.column_dimensions[letter].width = 14
print(summary_ws[f"B{start}"].value)      # =COUNTIF(Exceptions!$A:$A,A6)
```

**Three rules for formulas:**

1. **Sheet names with spaces need single quotes** in references: `'GL Data'!$D:$D`. Without them, Excel can't read the formula.
2. **openpyxl writes formulas but never calculates them.** The file stores no results until Excel (or LibreOffice) opens and recalculates it. So reading a fresh openpyxl file with `load_workbook(..., data_only=True)` returns `None` for every formula cell.
3. **Some newer Excel functions** (such as `TEXTJOIN`, `CONCAT`, `IFS`, `MAXIFS` and `MINIFS`) must be written with an `_xlfn.` prefix, for example `=_xlfn.MAXIFS(...)`, or Excel shows `#NAME?`. Classic functions like `SUM`, `SUMIFS`, `COUNTIFS`, `IF` and `INDEX`/`MATCH` need no prefix.

**Defined names** (named ranges) make formulas readable: `">="&ApprovalLimit` is clearer than `">="&Summary!$B$3`, and the name still works if the cell moves.

## 12. Excel tables and filters

Turning the exceptions into an **Excel table** gives reviewers banded rows, filter buttons and structured references:

```python
from openpyxl.worksheet.table import Table, TableStyleInfo

table_ref = f"A1:{get_column_letter(exc_ws.max_column)}{exc_ws.max_row}"
exc_table = Table(displayName="tblExceptions", ref=table_ref)
exc_table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
exc_ws.add_table(exc_table)
print(exc_table.ref)                      # A1:J43

# GL Data: a plain filter instead of a table
data_ws.auto_filter.ref = f"A1:I{data_ws.max_row}"
```

- Table names can't contain spaces and must be unique in the workbook.
- A table already has its own filter buttons, so don't also set `auto_filter` on the same range.
- Header cells in a table must be text.

## 13. Conditional formatting

Conditional formatting makes exceptions visible at a glance, and it **updates automatically** if values change.

```python
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule, FormulaRule

red_fill = PatternFill("solid", start_color="F8CBAD", end_color="F8CBAD")
amber_fill = PatternFill("solid", start_color="FFE699", end_color="FFE699")

# 1. Exceptions: highlight amounts at or above the approval limit (uses the defined name)
exc_ws.conditional_formatting.add(f"E2:E{exc_ws.max_row}",
    CellIsRule(operator="greaterThanOrEqual", formula=["ApprovalLimit"], fill=red_fill))

# 2. GL Data: shade whole rows posted at weekends
data_ws.conditional_formatting.add(f"A2:I{data_ws.max_row}",
    FormulaRule(formula=["WEEKDAY($B2,2)>5"], fill=amber_fill))

# 3. TB Rec: flag any non-zero difference
recon_ws.conditional_formatting.add(f"E2:E{recon_ws.max_row - 1}",
    CellIsRule(operator="notEqual", formula=["0"], fill=red_fill, font=Font(bold=True, color="9C0006")))

# 4. Summary: data bars for exception counts, and a colour scale for values
summary_ws.conditional_formatting.add(f"B{start}:B{end}",
    DataBarRule(start_type="min", end_type="max", color="5B9BD5"))
summary_ws.conditional_formatting.add(f"C{start}:C{end}",
    ColorScaleRule(start_type="min", start_color="FFFFFF", end_type="max", end_color="F4B183"))
```

| Rule | Use it for |
| --- | --- |
| `CellIsRule` | Compare a cell with a value or formula (`greaterThan`, `between`, `equal`, …) |
| `FormulaRule` | Any condition you can write as a formula, including whole-row highlights |
| `ColorScaleRule` | Shade from low to high (2 or 3 colours) |
| `DataBarRule` | In-cell bars sized by value |
| `IconSetRule` | Traffic-light or arrow icons |

In a `FormulaRule`, write the formula for the **first** cell of the range (`$B2`). The `$` locks the column, so every cell in the row checks column B.

## 14. Data validation dropdowns

A **Status** dropdown keeps the reviewer's responses consistent and easy to filter:

```python
from openpyxl.worksheet.datavalidation import DataValidation

status_dv = DataValidation(type="list", formula1='"Open,Cleared,Exception confirmed,Not applicable"',
                           allow_blank=False, showErrorMessage=True,
                           errorTitle="Invalid status", error="Choose a status from the list.")
exc_ws.add_data_validation(status_dv)
status_dv.add(f"I2:I{exc_ws.max_row}")

limit_dv = DataValidation(type="whole", operator="greaterThan", formula1="0",
                          showErrorMessage=True, error="The approval limit must be a positive whole number.")
summary_ws.add_data_validation(limit_dv)
limit_dv.add("B3")
print(status_dv.sqref)                    # I2:I43
```

Other validation types include `"decimal"`, `"date"` and `"textLength"`. A list can also point to a range, such as `formula1="=Lists!$A$1:$A$4"`, which suits longer lists.

## 15. Comments and hyperlinks

**Comments** work like review notes. **Hyperlinks** let a reviewer click from an exception straight to the source row:

```python
from openpyxl.comments import Comment
from openpyxl.worksheet.hyperlink import Hyperlink

exc_ws["A1"].comment = Comment("Tests run in Python on the client GL extract dated 31-Dec-2026.", "Saurabh S")

for r in range(2, exc_ws.max_row + 1):
    je_cell = exc_ws[f"B{r}"]
    je_id = je_cell.value
    first_row = next(i for i, line in enumerate(gl, start=2) if line["je_id"] == je_id)
    je_cell.hyperlink = Hyperlink(ref=je_cell.coordinate, location=f"'GL Data'!A{first_row}")   # internal link
    je_cell.font = Font(color="0563C1", underline="single")
    if exc_ws[f"A{r}"].value == "Unbalanced entry":
        exc_ws[f"J{r}"] = "Raised with client: credit side short by 500"
        exc_ws[f"J{r}"].comment = Comment("Client to post correcting entry before final.", "Reviewer")

print(exc_ws["B2"].hyperlink.location)    # 'GL Data'!A68
```

An internal link uses `location=` with the sheet name (quoted if it has spaces) and a cell. External links can simply be assigned as text: `cell.hyperlink = "https://example.com/policy.pdf"`.

## 16. Charts

openpyxl builds **native Excel charts** from cell ranges, so they update when the data changes. Here, monthly revenue from the GL goes onto the Summary sheet as a small table, with a column chart beside it, and exceptions by test get a bar chart:

```python
from openpyxl.chart import BarChart, Reference

monthly_revenue = defaultdict(float)
for line in gl:
    if line["account"] in ("4000", "4100"):
        monthly_revenue[line["date"].month] += line["credit"] - line["debit"]

chart_row = end + 6
summary_ws[f"A{chart_row}"] = "Month"
summary_ws[f"B{chart_row}"] = "Revenue"
for cell in summary_ws[chart_row][:2]:
    cell.style = "wp_header"
for m in range(1, 13):
    summary_ws[f"A{chart_row + m}"] = datetime(2026, m, 1).strftime("%b")
    summary_ws[f"B{chart_row + m}"] = round(monthly_revenue[m], 2)
    summary_ws[f"B{chart_row + m}"].number_format = "#,##0"

rev_chart = BarChart()
rev_chart.type = "col"
rev_chart.title = "Monthly revenue per GL (GBP)"
rev_chart.y_axis.title = "GBP"
rev_chart.y_axis.numFmt = "#,##0"
data = Reference(summary_ws, min_col=2, min_row=chart_row, max_row=chart_row + 12)       # include header for the series name
cats = Reference(summary_ws, min_col=1, min_row=chart_row + 1, max_row=chart_row + 12)
rev_chart.add_data(data, titles_from_data=True)
rev_chart.set_categories(cats)
rev_chart.legend = None
rev_chart.height, rev_chart.width = 7.5, 16
summary_ws.add_chart(rev_chart, "F3")

exc_chart = BarChart()
exc_chart.type = "bar"                                   # horizontal bars
exc_chart.title = "Exceptions by test"
exc_chart.add_data(Reference(summary_ws, min_col=2, min_row=start - 1, max_row=end), titles_from_data=True)
exc_chart.set_categories(Reference(summary_ws, min_col=1, min_row=start, max_row=end))
exc_chart.legend = None
exc_chart.height, exc_chart.width = 7.5, 16
summary_ws.add_chart(exc_chart, f"F{chart_row - 2}")

print(round(monthly_revenue[12]), round(monthly_revenue[11]))   # 754421 123237
```

December revenue is far above November's because of the three large year-end manual entries. That's visible at a glance in the chart.

Other chart types work the same way: `LineChart`, `PieChart`, `ScatterChart`, `AreaChart`, plus `BarChart(grouping="stacked")`. Note that the exception chart reads its counts from **formulas**, so it shows values only after Excel recalculates the file.

## 17. Layout: inserting, merging, grouping and hiding

```python
# insert a title row above the TB Rec table, then merge it across the table width
recon_ws.insert_rows(1)
recon_ws["A1"] = "Reconciliation of trial balance to general ledger, FY2026"
recon_ws["A1"].font = Font(bold=True, size=12, color=NAVY)
recon_ws.merge_cells("A1:E1")
recon_ws.freeze_panes = "A3"
print(recon_ws["A2"].value, recon_ws["E3"].value)   # Account =D2-C2: the formula moved down a row, but its references did not

# group and collapse detail columns, hide a helper column, colour the tabs
data_ws.column_dimensions.group("F", "H", hidden=True, outline_level=1)
exc_ws.column_dimensions["H"].hidden = True                  # GL Row helper column
summary_ws.sheet_properties.tabColor = NAVY
exc_ws.sheet_properties.tabColor = "C00000"
out.move_sheet("TB Rec", offset=-2)                          # move TB Rec next to Summary
print(out.sheetnames)                        # ['Summary', 'TB Rec', 'Exceptions', 'GL Data']
```

> [!WARNING]
> `insert_rows()` and `delete_rows()` move the cells, but **they don't update formulas**. After the insert, the formula that was in `E2` (`=D2-C2`) now sits in `E3` but still says `=D2-C2`, pointing at the header row. The fix is to rewrite the affected formulas after inserting:

```python
for r in range(3, recon_ws.max_row):
    recon_ws[f"E{r}"] = f"=D{r}-C{r}"
last_rec = recon_ws.max_row
for letter in "CDE":
    recon_ws[f"{letter}{last_rec}"] = f"=SUM({letter}3:{letter}{last_rec - 1})"
from openpyxl.formatting.formatting import ConditionalFormattingList
recon_ws.conditional_formatting = ConditionalFormattingList()               # clear the old rule, then re-add it for the new rows
recon_ws.conditional_formatting.add(f"E3:E{last_rec - 1}",
    CellIsRule(operator="notEqual", formula=["0"], fill=red_fill, font=Font(bold=True, color="9C0006")))
print(recon_ws["E3"].value, recon_ws[f"E{last_rec}"].value)   # =D3-C3 =SUM(E3:E15)
```

The same caution applies to conditional formatting, data validation, tables and charts. The simplest habit is to **lay out the sheet first and add formulas and rules last**.

Other layout tools: `ws.delete_cols(3)`, `ws.move_range("A2:E10", rows=1, cols=0)`, `ws.unmerge_cells("A1:E1")`, `ws.row_dimensions[5].hidden = True`, and `out.copy_worksheet(ws)` to duplicate a sheet within the same workbook.

## 18. Protection

Lock the workpaper's structure and formulas while leaving the reviewer's columns editable:

```python
from openpyxl.styles import Protection

# reviewer columns stay editable: Status and Reviewer Note
for r in range(2, exc_ws.max_row + 1):
    exc_ws[f"I{r}"].protection = Protection(locked=False)
    exc_ws[f"J{r}"].protection = Protection(locked=False)
exc_ws.protection.sheet = True
exc_ws.protection.password = "review"          # light protection against accidental edits
exc_ws.protection.autoFilter = False           # False = filtering is still allowed
exc_ws.protection.sort = False

summary_ws["B3"].protection = Protection(locked=False)    # the approval limit input stays editable
summary_ws.protection.sheet = True

out.security.lockStructure = True              # no adding, deleting or renaming sheets
print(exc_ws.protection.sheet, exc_ws["I2"].protection.locked)   # True False
```

Sheet protection guards against **accidental** changes. It isn't security, because the passwords are weak and easy to remove. Never rely on it for confidential data.

## 19. Print setup

```python
for sheet in (exc_ws, recon_ws):
    sheet.page_setup.orientation = "landscape"
    sheet.page_setup.paperSize = sheet.PAPERSIZE_A4
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0               # as many pages tall as needed
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.oddFooter.left.text = "&F – &A"          # file name – sheet name
    sheet.oddFooter.right.text = "Page &P of &N"

exc_ws.print_title_rows = "1:1"                    # repeat the header on every page
exc_ws.print_area = f"A1:J{exc_ws.max_row}"
print(exc_ws.print_title_rows)            # $1:$1
```

Header and footer codes include `&P` (page), `&N` (total pages), `&D` (date), `&F` (file name) and `&A` (sheet name).

## 20. Saving and checking the workpaper

```python
out.active = out.sheetnames.index("Summary")       # open on the Summary tab
path = OUTPUT / "je_testing_workpaper.xlsx"
out.save(path)

check = load_workbook(path)
print(check.sheetnames)                            # ['Summary', 'TB Rec', 'Exceptions', 'GL Data']
print(check["Exceptions"].max_row - 1, "exception rows |",
      list(check["Exceptions"].tables), "| defined names:", list(check.defined_names))

values = load_workbook(path, data_only=True)
print(values["Summary"][f"B{start}"].value)       # None: formulas have no results until Excel recalculates
```

**Recalculating:** opening the file in Excel calculates every formula. If the result must be calculated without Excel, LibreOffice can do it from the command line:

```bash
soffice --headless --convert-to xlsx --outdir recalculated output/je_testing_workpaper.xlsx
```

---

# Part 4: Going further

## 21. Large files: read-only and write-only modes

A full-year ledger can have millions of rows. The normal mode keeps every cell in memory, but two optimised modes don't:

```python
# read-only: streams rows instead of loading the whole sheet
ro = load_workbook(SOURCE, read_only=True)
ro_ws = ro["GL Detail"]
manual_value = 0.0
for row in ro_ws.iter_rows(min_row=header_row + 1, values_only=True):
    if row[col["Source"]] == "Manual":
        manual_value += to_number(row[col["Debit"]])
ro.close()                                    # read-only workbooks keep the file open until closed
print(round(manual_value, 2))                 # 1114743.56: the total of manual debits

# write-only: streams rows out, for very large outputs
from openpyxl.cell import WriteOnlyCell

wo = Workbook(write_only=True)
wo_ws = wo.create_sheet("Manual JEs")
header = [WriteOnlyCell(wo_ws, value=h) for h in ("JE ID", "Date", "Amount")]
for c in header:
    c.font = Font(bold=True)
wo_ws.append(header)
for line in gl:
    if line["source"] == "Manual" and line["debit"]:
        wo_ws.append([line["je_id"], line["date"], line["debit"]])
wo.save(OUTPUT / "manual_entries.xlsx")
print(load_workbook(OUTPUT / "manual_entries.xlsx")["Manual JEs"].max_row - 1)   # 102 manual entries
```

| Mode | Can do | Can't do |
| --- | --- | --- |
| `read_only=True` | Iterate rows quickly with low memory | Write, or jump to cells randomly (slow) |
| `write_only=True` | Append rows quickly with low memory | Read, or edit a cell once written |

In read-only mode, `ws.max_row` can be wrong for files written by some tools, so iterate rather than relying on it.

## 22. Editing an existing client file safely

```python
client = load_workbook(SOURCE)                  # default mode: formulas preserved as text
ws_c = client["GL Detail"]
ws_c["M4"] = "Auditor Flag"
ws_c["M4"].font = Font(bold=True, color="C00000")
flagged_rows = {e["gl_row"] for e in exceptions}
for r in flagged_rows:
    ws_c[f"M{r}"] = "Review"
client.save(OUTPUT / "client_gl_fy2026_flagged.xlsx")    # always save under a NEW name
print(len(flagged_rows))                      # 30 rows marked for review
```

**Rules for client files:**

- **Never overwrite the original.** Save to a new file and keep the source untouched as audit evidence.
- **Don't save after `data_only=True`.** That workbook has no formulas left, so saving replaces every formula with its last value, permanently.
- **Macros:** open `.xlsm` files with `load_workbook(path, keep_vba=True)` and save them as `.xlsm`, or the macros are lost.
- **Content openpyxl doesn't read is dropped on save,** including images, existing charts, shapes and some advanced features. Check before saving over anything that matters.
- **Formulas need two passes to see both versions:** load once normally (formulas as text) and once with `data_only=True` (the last calculated values).

## 23. What openpyxl can and can't do

| Task | openpyxl | Alternative |
| --- | --- | --- |
| Read and write `.xlsx` / `.xlsm` | ✅ | |
| Read old `.xls` files | ❌ | `pandas.read_excel` with `xlrd`, or convert to `.xlsx` first |
| Write formulas | ✅ | |
| Calculate formulas | ❌ | Open in Excel, or recalculate with LibreOffice |
| Styles, number formats, conditional formatting, validation | ✅ | |
| Tables, defined names, comments, hyperlinks | ✅ | |
| Create native charts | ✅ | |
| Keep existing charts and images when editing a file | ❌ (lost on save) | Edit with Excel or `xlwings` |
| Insert images | ✅ (needs Pillow) | `openpyxl.drawing.image.Image` |
| Create pivot tables | ❌ (existing ones are preserved) | Build the summary with pandas `pivot_table` and write the result |
| Auto-fit column widths | ❌ | Set widths, or estimate from text length |
| Fast bulk analysis | Slow | pandas |

## 24. Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| `InvalidFileException` for a `.xls` file | openpyxl only reads `.xlsx`-family files | Save as `.xlsx`, or use `pandas` with `xlrd` |
| Formula cells read as `None` with `data_only=True` | The file was written by openpyxl and never recalculated | Open and save in Excel, or recalculate with LibreOffice |
| Formulas show `#NAME?` in Excel | A newer function written without its prefix | Use `_xlfn.` (e.g. `=_xlfn.MAXIFS(...)`), or a classic function |
| Cross-sheet formula shows an error | Sheet name with spaces not quoted | `'GL Data'!A1` |
| Totals are wrong or `TypeError: can't add str and float` | Numbers stored as text | Convert with a helper like `to_number()` |
| Account `0100` reads as `100` | The cell was stored as a number | Read with `str()`, and store codes as text when writing |
| Formulas point to the wrong rows after `insert_rows` | openpyxl doesn't adjust formulas | Insert rows first, write formulas last |
| Merged cell value is `None` | Only the top-left cell of a merge holds the value | Read the top-left cell, or unmerge first |
| `PermissionError` when saving | The file is open in Excel | Close it, or save under a new name |
| Macros disappeared | `.xlsm` loaded without `keep_vba=True` | `load_workbook(path, keep_vba=True)` |
| Charts or images vanished from a client file | openpyxl doesn't read them, so they're dropped on save | Never save over the original |
| `ValueError` when adding a table | Duplicate table name, spaces in the name, or non-text headers | Use a unique name like `tblExceptions`, with text headers |
| Very slow on large files | The normal mode loads every cell | `read_only=True` / `write_only=True`, or pandas |

## Sources

**openpyxl documentation** (version 3.1)

- [Tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html): workbooks, worksheets, cells, `iter_rows`, saving and loading
- [Simple usage](https://openpyxl.readthedocs.io/en/stable/usage.html): writing workbooks, formulas, merged cells, and the warning that some content is lost when existing files are saved
- [Working with styles](https://openpyxl.readthedocs.io/en/stable/styles.html): fonts, fills, borders, alignment, number formats and named styles
- [Conditional formatting](https://openpyxl.readthedocs.io/en/stable/formatting.html): `CellIsRule`, `FormulaRule`, colour scales, data bars and icon sets
- [Validating cells](https://openpyxl.readthedocs.io/en/stable/validation.html): `DataValidation`
- [Worksheet tables](https://openpyxl.readthedocs.io/en/stable/worksheet_tables.html): `Table` and `TableStyleInfo`
- [Defined names](https://openpyxl.readthedocs.io/en/stable/defined_names.html): `DefinedName`, `quote_sheetname` and `absolute_coordinate` (the 3.1 API)
- [Charts](https://openpyxl.readthedocs.io/en/stable/charts/introduction.html): `BarChart`, `LineChart` and `Reference`
- [Comments](https://openpyxl.readthedocs.io/en/stable/comments.html)
- [Inserting and deleting rows and columns, moving ranges](https://openpyxl.readthedocs.io/en/stable/editing_worksheets.html): including the note that formulas aren't adjusted
- [Protection](https://openpyxl.readthedocs.io/en/stable/protection.html) and [print settings](https://openpyxl.readthedocs.io/en/stable/print_settings.html)
- [Optimised modes](https://openpyxl.readthedocs.io/en/stable/optimized.html): `read_only` and `write_only`
- [Working with pandas](https://openpyxl.readthedocs.io/en/stable/pandas.html): `dataframe_to_rows`

**pandas documentation**

- [`pandas.read_excel`](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html): `header`, `dtype` and the `openpyxl` engine

**Verification:** every snippet was run in order against the file created by `make_gl_workbook.py` on openpyxl 3.1.5, pandas 3.0.2 and Python 3.12. The finished workpaper was recalculated in LibreOffice to confirm every formula evaluates without errors. Printed values in comments are actual outputs.
