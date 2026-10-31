"""
Creates a sample general ledger used by 'matplotlib-seaborn-gl-guide.md'.

All data is invented for practice. Run once:
    python make_gl_sample.py
Output: sample_data/gl_fy2025_fy2026.csv (one row per journal entry line).

Sign convention: debits are positive, credits are negative.
Built-in red flags for the charts to find:
  - a December revenue spike and large year-end manual entries without approval
  - one preparer splitting entries just below a 10,000 approval limit
  - weekend and late-night manual postings
  - round-number manual entries
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
OUT = Path(__file__).parent / "sample_data"
OUT.mkdir(exist_ok=True)

ACCOUNTS = {
    "1000": ("Cash", "Cash"),
    "1200": ("Accounts Receivable", "Receivables"),
    "1300": ("Inventory", "Inventory"),
    "2000": ("Accounts Payable", "Payables"),
    "4000": ("Product Revenue", "Revenue"),
    "4100": ("Service Revenue", "Revenue"),
    "5000": ("Cost of Goods Sold", "Cost of Sales"),
    "6000": ("Salaries", "Operating Expenses"),
    "6100": ("Rent", "Operating Expenses"),
    "6200": ("Travel", "Operating Expenses"),
    "6300": ("Consulting", "Operating Expenses"),
}
# (debit account, credit account, typical amount, monthly volume, source)
FLOWS = [
    ("1200", "4000", 9_000, 60, "Automated"),
    ("1200", "4100", 4_000, 30, "Automated"),
    ("1000", "1200", 11_000, 45, "Automated"),
    ("6000", "1000", 15_000, 6, "Automated"),
    ("6100", "2000", 12_000, 1, "Automated"),
    ("6200", "2000", 1_200, 12, "Manual"),
    ("6300", "2000", 6_000, 6, "Manual"),
    ("2000", "1000", 8_000, 15, "Automated"),
]
PREPARERS = ["A. Rao", "M. Gomez", "J. Lee", "S. Patel"]
APPROVERS = ["K. Wong", "D. Smith"]

rows, je_no = [], 0


def add_entry(date, hour, debit_acct, credit_acct, amount, source, preparer, approver, desc):
    global je_no
    je_no += 1
    posted_at = pd.Timestamp(date) + pd.Timedelta(hours=hour, minutes=int(rng.integers(0, 60)))
    for line, (acct, amt) in enumerate([(debit_acct, amount), (credit_acct, -amount)], start=1):
        name, fsli = ACCOUNTS[acct]
        rows.append({
            "je_id": f"JE{je_no:06d}", "line": line,
            "posting_date": pd.Timestamp(date).date(), "posted_at": posted_at,
            "entity": entity, "account": acct, "account_name": name, "fsli": fsli,
            "amount": round(amt, 2), "source": source,
            "preparer": preparer, "approver": approver, "description": desc,
        })


for year in (2025, 2026):
    for month in range(1, 13):
        days = pd.date_range(f"{year}-{month:02d}-01", periods=pd.Period(f"{year}-{month}").days_in_month)
        business_days = days[days.dayofweek < 5]
        growth = 1.06 if year == 2026 else 1.0
        for debit, credit, typical, volume, source in FLOWS:
            n = volume
            if debit == "1200" and month == 12 and year == 2026:
                n = int(volume * 1.15)
            for _ in range(n):
                entity = rng.choice(["UK", "US", "IN"], p=[0.3, 0.5, 0.2])
                amount = float(rng.lognormal(np.log(typical * growth), 0.6))
                date = rng.choice(business_days)
                hour = int(rng.integers(8, 19))
                preparer = rng.choice(PREPARERS) if source == "Manual" else "SYSTEM"
                approver = rng.choice(APPROVERS) if source == "Manual" else "SYSTEM"
                add_entry(date, hour, debit, credit, amount, source, preparer, approver,
                          f"{ACCOUNTS[credit if debit == '1200' else debit][0]} posting")
                if credit == "4000":   # every product sale also relieves inventory at about 60% of price
                    add_entry(date, hour, "5000", "1300", amount * rng.normal(0.60, 0.03),
                              "Automated", "SYSTEM", "SYSTEM", "Cost of goods sold")

# Red flag 1: large year-end manual revenue entries by the CFO, no approver
entity = "US"
for amount in [250_000, 180_000, 210_000]:
    add_entry("2026-12-31", 22, "1200", "4000", amount, "Manual", "CFO", None, "Year-end revenue adjustment")

# Red flag 2: one preparer splitting entries just below a 10,000 approval limit
for _ in range(40):
    entity = "UK"
    add_entry(rng.choice(pd.date_range("2026-01-01", "2026-12-31", freq="B")), int(rng.integers(9, 18)),
              "6300", "2000", float(rng.uniform(9_500, 9_990)), "Manual", "M. Gomez", "K. Wong",
              "Consulting fee")

# Red flag 3: weekend and late-night manual postings
for _ in range(25):
    entity = "IN"
    day = rng.choice(pd.date_range("2026-01-01", "2026-12-31", freq="W-SAT"))
    add_entry(day, int(rng.choice([22, 23, 1, 2])), "6200", "2000",
              float(rng.lognormal(np.log(3_000), 0.5)), "Manual", "S. Patel", "D. Smith", "Travel claim")

# Red flag 4: round-number manual entries
for amount in [5_000, 10_000, 20_000, 25_000, 50_000, 15_000, 30_000, 40_000]:
    entity = "US"
    add_entry(rng.choice(pd.date_range("2026-01-01", "2026-12-31", freq="B")), 17, "6300", "2000",
              float(amount), "Manual", "J. Lee", "K. Wong", "Consulting accrual")

gl = pd.DataFrame(rows).sort_values(["posted_at", "je_id", "line"]).reset_index(drop=True)
assert abs(gl["amount"].sum()) < 0.01, "ledger must balance"
gl.to_csv(OUT / "gl_fy2025_fy2026.csv", index=False)
print(f"{len(gl):,} GL lines, {gl['je_id'].nunique():,} journal entries written to {OUT}")
