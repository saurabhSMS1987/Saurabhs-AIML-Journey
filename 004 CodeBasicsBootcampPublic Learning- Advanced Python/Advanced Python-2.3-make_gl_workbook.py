"""
Creates the sample client workbook used by 'openpyxl-gl-guide.md'.

All data is invented for practice. Run once:
    python make_gl_workbook.py
Output: sample_data/client_gl_fy2026.xlsx with three sheets:
  - "GL Detail"          one row per journal entry line, below a merged title block
  - "Trial Balance"      closing balance per account, as reported by the client
  - "Chart of Accounts"  account code, name, financial statement line item (FSLI) and type

Built-in issues for the guide to find:
  - large year-end manual revenue entries with no approver
  - one preparer's consulting entries clustered just below a 10,000 approval limit
  - weekend postings, a suspense-account posting and round-number accruals
  - one journal entry whose debits and credits don't balance
  - two amounts stored as text, as some client exports do
  - a Trial Balance that differs from the GL for one account
"""
import random
from datetime import date, datetime, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

random.seed(7)
OUT = Path(__file__).parent / "sample_data"
OUT.mkdir(exist_ok=True)

COA = [
    ("1000", "Cash at Bank", "Cash", "Asset"),
    ("1200", "Accounts Receivable", "Receivables", "Asset"),
    ("1300", "Inventory", "Inventory", "Asset"),
    ("1999", "Suspense", "Other", "Asset"),
    ("2000", "Accounts Payable", "Payables", "Liability"),
    ("2100", "Accrued Liabilities", "Accruals", "Liability"),
    ("4000", "Product Revenue", "Revenue", "Income"),
    ("4100", "Service Revenue", "Revenue", "Income"),
    ("5000", "Cost of Goods Sold", "Cost of Sales", "Expense"),
    ("6000", "Salaries", "Operating Expenses", "Expense"),
    ("6100", "Rent", "Operating Expenses", "Expense"),
    ("6200", "Travel", "Operating Expenses", "Expense"),
    ("6300", "Consulting", "Operating Expenses", "Expense"),
]
NAMES = {code: name for code, name, _, _ in COA}

# (debit account, credit account, typical amount, entries per month, source)
FLOWS = [
    ("1200", "4000", 8_000, 12, "Automated"),
    ("1200", "4100", 3_000, 6, "Automated"),
    ("5000", "1300", 5_000, 10, "Automated"),
    ("1000", "1200", 9_000, 8, "Automated"),
    ("6000", "1000", 15_000, 2, "Automated"),
    ("6100", "2000", 12_000, 1, "Automated"),
    ("6200", "2000", 900, 4, "Manual"),
    ("6300", "2000", 6_000, 2, "Manual"),
    ("2000", "1000", 7_000, 4, "Automated"),
]
PREPARERS = ["A. Rao", "M. Gomez", "J. Lee", "S. Patel"]
APPROVERS = ["K. Wong", "D. Smith"]

rows, je_no = [], 0


def add(day, debit_acct, credit_acct, amount, source, preparer, approver, desc, hour=None, credit_amount=None):
    global je_no
    je_no += 1
    hour = hour if hour is not None else random.randint(8, 18)
    posted_at = datetime.combine(day, datetime.min.time()) + timedelta(hours=hour, minutes=random.randint(0, 59))
    amount = round(amount, 2)
    credit_amount = round(credit_amount if credit_amount is not None else amount, 2)
    for line, (acct, dr, cr) in enumerate([(debit_acct, amount, None), (credit_acct, None, credit_amount)], start=1):
        rows.append([f"JE{je_no:05d}", line, day, posted_at, acct, NAMES[acct], dr, cr,
                     preparer, approver, source, desc])


def business_day(month):
    while True:
        d = date(2026, month, random.randint(1, 28))
        if d.weekday() < 5:
            return d


for month in range(1, 13):
    for debit, credit, typical, n, source in FLOWS:
        for _ in range(n):
            amount = random.lognormvariate(0, 0.5) * typical
            preparer = random.choice(PREPARERS) if source == "Manual" else "SYSTEM"
            approver = random.choice(APPROVERS) if source == "Manual" else "SYSTEM"
            add(business_day(month), debit, credit, amount, source, preparer, approver, f"{NAMES[credit if debit == '1200' else debit]} posting")

# red flags
for amount in (250_000, 180_000, 210_000):
    add(date(2026, 12, 31), "1200", "4000", amount, "Manual", "CFO", None, "Year-end revenue adjustment", hour=22)
for _ in range(15):
    add(business_day(random.randint(1, 12)), "6300", "2000", random.uniform(9_500, 9_990), "Manual", "M. Gomez", "K. Wong", "Consulting fee")
for _ in range(6):
    sat = date(2026, random.randint(1, 12), 1)
    sat += timedelta(days=(5 - sat.weekday()) % 7)
    add(sat, "6200", "2000", random.uniform(800, 4_000), "Manual", "S. Patel", "D. Smith", "Travel claim", hour=random.choice([23, 1]))
for amount in (10_000, 25_000, 50_000, 20_000):
    add(business_day(random.randint(1, 12)), "6300", "2100", amount, "Manual", "J. Lee", "K. Wong", "Consulting accrual", hour=17)
add(date(2026, 9, 15), "6200", "1999", 3_750, "Manual", "S. Patel", "D. Smith", "Unallocated expense")
add(date(2026, 6, 30), "6300", "2000", 5_000, "Manual", "A. Rao", "K. Wong", "Consulting fee", credit_amount=4_500)   # unbalanced

rows.sort(key=lambda r: (r[3], r[0], r[1]))

# two amounts stored as text, as some exports do
text_rows = [i for i, r in enumerate(rows) if r[6] and r[10] == "Automated"][:2]
for i in text_rows:
    rows[i][6] = f"{rows[i][6]:,.2f}"

wb = Workbook()
ws = wb.active
ws.title = "GL Detail"
ws["A1"] = "AtliQ Retail Ltd"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:L1")
ws["A2"] = "General Ledger Detail: 1 January to 31 December 2026 (GBP)"
ws.merge_cells("A2:L2")
ws["A1"].alignment = ws["A2"].alignment = Alignment(horizontal="left")
headers = ["JE ID", "Line", "Posting Date", "Posted At", "Account", "Account Name",
           "Debit", "Credit", "Preparer", "Approver", "Source", "Description"]
ws.append([])
ws.append(headers)
for r in rows:
    ws.append(r)
for cell in ws[4]:
    cell.font = Font(bold=True)

# trial balance per client: matches the GL except Product Revenue, which is overstated by 25,000
balances = {}
for r in rows:
    dr = float(str(r[6]).replace(",", "")) if r[6] is not None else 0.0
    cr = r[7] or 0.0
    balances[r[4]] = balances.get(r[4], 0.0) + dr - cr
tb = wb.create_sheet("Trial Balance")
tb.append(["Account", "Account Name", "Closing Balance"])
for code, name, _, _ in COA:
    bal = round(balances.get(code, 0.0), 2)
    if code == "4000":
        bal -= 25_000
    tb.append([code, name, bal])

coa = wb.create_sheet("Chart of Accounts")
coa.append(["Account", "Account Name", "FSLI", "Type"])
for row in COA:
    coa.append(list(row))

path = OUT / "client_gl_fy2026.xlsx"
wb.save(path)
print(f"{len(rows):,} GL lines ({je_no} journal entries) written to {path}")
