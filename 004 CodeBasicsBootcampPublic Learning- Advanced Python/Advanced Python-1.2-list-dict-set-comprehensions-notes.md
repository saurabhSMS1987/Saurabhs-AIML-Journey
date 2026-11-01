# List, Dict and Set Comprehensions: My Advanced Python Notes

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **List, Dict Comprehension** lecture from the **CodeBasics Advanced Python course**.

## Where I started

In my first Python course, building a list meant three steps: create an empty list, loop, and `append()`. This lecture showed how to fold all of that into one line with a **comprehension**, and that the one-liner is also faster. It's the same idea as the assignment I just finished, but here it was explained from the ground up.

## The data in brief

The examples used small values built in the notebook. There was no data file.

- The numbers 1 to 5, squared, and a 10-million-number range for a speed test.
- Share prices `[100, 120, 80, 50]` and earnings per share `[9, 15, 40, 2]`, for price-to-earnings (P/E) ratios.
- Shopping prices `[120, 99, 150, 80, 200]`, with a 10% discount on purchases over $100.
- Three names and ages, and five customer transactions (Mira, Mohan and Lucy).

## What I learnt

**The basic pattern:**

```python
# loop version
sqr_numbers = []
for n in numbers:
    sqr_numbers.append(n * n)

# comprehension version: same result, one line
sqr_numbers = [n * n for n in numbers]      # [1, 4, 9, 16, 25]
```

Read it as: *"give me `n * n` for each `n` in `numbers`."*

**Comprehensions are faster.** Squaring 10 million numbers took **0.77 seconds** with a loop and **0.50 seconds** with a list comprehension, about 35% faster in the lecture's run.

**The forms the lecture covered:**

| Form | Example | Result |
| --- | --- | --- |
| Transform | `[n * n for n in numbers]` | `[1, 4, 9, 16, 25]` |
| Two lists with `zip` | `[p / e for p, e in zip(price, eps)]` | P/E ratios: `[11.1, 8.0, 2.0, 25.0]` |
| If–else inside | `[p / e if e != 0 else -1 for p, e in zip(price, eps)]` | `-1` where earnings are 0, instead of a crash |
| Call a function | `[len(word) for word in words]` | `[5, 6, 6, 4]` |
| Filter with `if` | `[p * 0.9 for p in prices if p > 100]` | `[108.0, 135.0, 180.0]` |
| Dictionary | `{names[i]: ages[i] for i in range(len(names))}` | `{'Alice': 25, 'Bob': 30, 'Charlie': 35}` |
| Set | `{t["customer_name"] for t in transactions}` | `{'Mira', 'Mohan', 'Lucy'}` |

**Where the `if` goes changes its meaning:**

- `if` at the **end** (`for p in prices if p > 100`) is a **filter**: items that fail are left out, so 5 prices became 3.
- `if ... else` **before** `for` is a **choice**: every item stays, but gets one of two values. That's how the zero-earnings share got `-1` instead of a `ZeroDivisionError`.

## How this shows up in financial statement audit work

These snippets use small sample data built in the code.

**1. Pulling journal entries above the testing threshold** (a filter):

```python
journal_entries = [("JE01", 4_200), ("JE02", 98_000), ("JE03", 650), ("JE04", 125_000), ("JE05", 51_500)]

selected = [je_id for je_id, amount in journal_entries if amount > 50_000]
print(selected)   # ['JE02', 'JE04', 'JE05']: the high-value sample
```

**2. Ratios across entities, safely** (`zip` with if–else). Gross margin per subsidiary, with a subsidiary that has no revenue yet:

```python
entities = ["UK Ltd", "US Inc", "IN Pvt", "SG Pte"]
revenue = [1_250_000, 2_400_000, 0, 610_000]
gross_profit = [410_000, 864_000, 0, 140_000]

margin = [round(g / r * 100, 1) if r != 0 else None for g, r in zip(gross_profit, revenue)]
print(dict(zip(entities, margin)))   # {'UK Ltd': 32.8, 'US Inc': 36.0, 'IN Pvt': None, 'SG Pte': 23.0}
```

I used `None` rather than the lecture's `-1`. In audit work, `-1` could be mistaken for a real negative margin, while `None` clearly means "not calculable".

**3. Account-level flux analysis** (dictionary comprehensions):

```python
accounts = ["Revenue", "Receivables", "Inventory", "Payables"]
cy = [1_950_000, 640_000, 410_000, 300_000]
py = [1_820_000, 470_000, 405_000, 310_000]

change_pct = {acct: round((c - p) / p * 100, 1) for acct, c, p in zip(accounts, cy, py)}
flagged = {acct: pct for acct, pct in change_pct.items() if abs(pct) > 10}
print(flagged)   # {'Receivables': 36.2}: receivables grew far faster than revenue (7.1%)
```

**4. Segregation-of-duties check** (a set comprehension and a filtered list):

```python
entries = [
    {"je": "JE10", "preparer": "A. Rao",   "approver": "K. Wong"},
    {"je": "JE11", "preparer": "M. Gomez", "approver": "M. Gomez"},
    {"je": "JE12", "preparer": "J. Lee",   "approver": "K. Wong"},
    {"je": "JE13", "preparer": "CFO",      "approver": "CFO"},
]

approvers = {e["approver"] for e in entries}
self_approved = [e["je"] for e in entries if e["preparer"] == e["approver"]]
print(sorted(approvers))   # ['CFO', 'K. Wong', 'M. Gomez']
print(self_approved)       # ['JE11', 'JE13']: entries approved by the person who prepared them
```

**5. Cleaning vendor names before matching** (calling a function inside a comprehension):

```python
raw_vendors = ["  Acme Corp ", "ACME CORP", "Beta Ltd", "beta ltd  "]
clean = {v.strip().upper() for v in raw_vendors}
print(sorted(clean))   # ['ACME CORP', 'BETA LTD']: 4 records are really 2 vendors
```

## My reflection

What I liked most is how closely a comprehension reads like an audit procedure: *"select every entry where the amount exceeds the threshold"* becomes `[je for je, amount in entries if amount > threshold]`. That makes the code easier to review, which matters when someone else needs to follow my working.

The if–else example also stayed with me. Dividing by zero is a real risk with ratios, and handling it inside the comprehension keeps the whole calculation running. I'd just choose a placeholder that can't be mistaken for a real value, like `None` rather than `-1`.
