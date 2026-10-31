# Handling Missing Data with replace(): My Lecture 21 Notes

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Handling Missing Data – replace method** lecture from the **CodeBasics Python course**.

## Where I started

Last lecture dealt with gaps that pandas already recognised as missing (`NaN`). This one tackled a sneakier problem: missing data *disguised as real values*. A system writes `-99999` where it has no reading, and pandas happily treats it as a number. `replace()` turns those codes back into honest blanks, and it can also standardise labels and turn text into numbers.

## The data in brief

A small `weather_data.csv` with **7 rows** for 1–6 January 2017, and 4 columns: `day`, `temperature`, `windspeed` and `event`.

- **Placeholder codes** stand in for missing readings: `-99999` appears 4 times (2 temperatures, 2 windspeeds), and `-88888` once.
- `event` uses the text `"no event"` twice.
- **6 January appears twice**, which is a duplicate date nobody comments on in the lecture.

A second mini-dataset rates six students as poor, average, good or exceptional.

## What I learnt

**Why placeholders are dangerous:** while `-99999` sits in the temperature column, any average is meaningless. Two fake readings drag the mean far below zero.

| Pattern | Code | Effect |
| --- | --- | --- |
| One value | `df.replace(-99999, np.nan)` | Every `-99999` becomes missing |
| Several values | `df.replace([-99999, -88888], 0)` | Both codes become 0 |
| Per column | `df.replace({"temperature": -99999, "event": "no event"}, np.nan)` | Each column uses its own rule |
| Mapping | `df.replace({-99999: np.nan, "no event": "Sunny"})` | Each old value gets its own new value |
| List to list | `df.replace(["poor", "average", "good", "exceptional"], [1, 2, 3, 4])` | Ratings become scores |

Things I noticed along the way:

- **Replacing one code isn't enough.** After replacing `-99999`, the `-88888` was still sitting in the windspeed column. Check for *every* placeholder the system uses.
- **Replacing with 0 is risky.** A "0 °C" reading is a real temperature, so filling placeholders with `0` creates false data. `NaN` is the honest choice.
- **"no event" → "Sunny" is an assumption.** The lecture mapped it that way, but nothing in the data says those days were sunny.

> [!IMPORTANT]
> The notebook writes `np.NaN`. That alias was **removed in NumPy 2.0** and now raises an `AttributeError`. Use `np.nan`, in lower case.

## How this shows up in financial statement audit work

General ledger (GL) and trial balance (TB) extracts often contain placeholder codes, inconsistent labels and text-formatted amounts. These snippets use small sample tables built in the code.

**1. Placeholder amounts and dates in a GL extract.** Count them first, because they can be findings, then replace them.

```python
import pandas as pd
import numpy as np

gl = pd.DataFrame({
    "je_id":       ["JE01", "JE02", "JE03", "JE04", "JE05"],
    "amount":      [12500.00, 999999.99, 860.00, -1.00, 4300.00],
    "posted_date": ["2026-09-28", "2026-09-29", "9999-12-31", "2026-09-30", "1900-01-01"],
})

placeholders = {"amount": [999999.99, -1.00], "posted_date": ["9999-12-31", "1900-01-01"]}
for col, codes in placeholders.items():
    print(col, gl[col].isin(codes).sum())          # amount 2, posted_date 2

gl = gl.replace(placeholders, np.nan)
print(gl["amount"].sum())                          # 17660.0: placeholders no longer inflate the total
```

Before the cleanup, the fake `999999.99` would have added nearly a million to the GL total.

**2. Standardising account names for financial statement line item (FSLI) mapping.** The same account was keyed three different ways:

```python
tb = pd.DataFrame({
    "account": ["A/R", "Accts Rec", "Accounts receivable", "Inventory", "inventories"],
    "balance": [125000, 48000, 12500, 300000, 15000],
})

tb["account"] = tb["account"].replace({
    "A/R": "Accounts Receivable", "Accts Rec": "Accounts Receivable",
    "Accounts receivable": "Accounts Receivable", "inventories": "Inventory",
})
print(tb.groupby("account")["balance"].sum().to_dict())
# {'Accounts Receivable': 185500, 'Inventory': 315000}: now matches the financial statements line by line
```

**3. Turning risk ratings into scores (list to list).**

```python
risk = pd.DataFrame({"fsli": ["Revenue", "Cash", "Inventory", "Provisions"],
                     "inherent_risk": ["High", "Low", "Medium", "High"]})

risk["score"] = risk["inherent_risk"].replace(["Low", "Medium", "High"], [1, 2, 3])
print(risk.sort_values("score", ascending=False)["fsli"].tolist())
# ['Revenue', 'Provisions', 'Inventory', 'Cash']: focus testing in this order
```

**4. Accounting-format amounts, using `replace` with `regex=True`.** Brackets mean negative, and amounts may include commas and currency symbols:

```python
tb_raw = pd.Series(["$125,000.00", "(4,250.00)", "$860.00", "(1,200.50)"])

clean = (tb_raw.replace(r"[$,]", "", regex=True)           # remove $ and commas
               .replace(r"^\((.*)\)$", r"-\1", regex=True)  # (4250.00) becomes -4250.00
               .astype(float))
print(clean.tolist())       # [125000.0, -4250.0, 860.0, -1200.5]
print(clean.sum())          # 120409.5
```

**5. Replacing per column, so legitimate zeros stay.** A `0` in `quantity` may mean "not recorded", but a `0` in `amount` can be a genuine nil balance:

```python
inv = pd.DataFrame({"sku": ["S1", "S2", "S3"], "quantity": [120, 0, 45], "amount": [2400.0, 0.0, 900.0]})
inv = inv.replace({"quantity": 0}, np.nan)        # only quantity is changed
print(inv["quantity"].isnull().sum(), inv["amount"].eq(0).sum())   # 1 1: the nil balance is kept
```

## My reflection

This lecture changed how I look at "complete" data. An extract can have zero `NaN`s and still be full of missing information, hidden behind codes like `999999.99`, `9999-12-31` or `-1`. In a financial statement audit, those placeholders can inflate a balance or hide an unposted entry. So before I total anything, I'll ask the client which placeholder codes their system uses, and count them.

The lecture's own choices were a good warning too. Replacing placeholders with `0`, or "no event" with "Sunny", quietly adds assumptions. In audit, every replacement should be documented, so a reviewer can see exactly what changed and why.

Next, I want to practise:

- [ ] Profile a GL extract for placeholder amounts and dates before totalling it
- [ ] Build a mapping dictionary from client account names to FSLIs
- [ ] Clean accounting-format amounts with `regex=True` and agree the total to the TB
