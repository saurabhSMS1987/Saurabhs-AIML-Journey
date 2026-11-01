# Python Sets and Frozensets: My Lecture 25 Notes

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Set & Frozenset** lecture from the **CodeBasics Advanced Python course**.

## Where I started

Lists keep everything, duplicates included. This lecture introduced the **set**, a collection that keeps only unique items and can compare two groups in one step: who appears in both, who appears in either, and who appears in one but not the other. For audit work, that last question is one I ask almost every day.

## The data in brief

The examples used small values built in the notebook. There was no data file.

- `[1, 2, 3, 2, 3, 4]` became `{1, 2, 3, 4}`.
- A food menu: Dosa, Idli and Biryani.
- **5 transactions** from 3 customers (Mira, Mohan and Lucy).
- **Two classes of 4 students each**, with only Mohan in both.

## What I learnt

**Creating a set:** `set([1, 2, 3, 2, 3, 4])` or `{1, 2, 3, 4}`. Duplicates disappear automatically.

**Sets are unordered.** `myset[0]` raised `TypeError: 'set' object is not subscriptable`, because there's no "first" item. Turning a set back into a list (`list(customers)`) gave `['Mira', 'Lucy', 'Mohan']`, in no particular order, so I shouldn't rely on it.

**Membership and changes:**

| Code | Result |
| --- | --- |
| `"Dosa" in menu` | `True`, and fast even for very large sets |
| `menu.add("Pizza")` | Adds one item |
| `menu.remove("Biryani")` | Removes an item, and raises a `KeyError` if it isn't there |
| `menu.discard("Biryani")` | Removes it without an error if it's missing (not in the lecture) |

**Frozenset:** an **immutable** set. `frozenset(["Dosa", "Idli", "Biryani"]).add("pizza")` raised an `AttributeError`, because a frozenset can't be changed after it's created.

**Comparing two sets** (class `a` = Mira, Mohan, Lucy, Ahmed; class `b` = Chen, Mohan, Radha, Maria):

| Operation | Operator | Method | Result |
| --- | --- | --- | --- |
| In both | `a & b` | `a.intersection(b)` | `{'Mohan'}` |
| In either | `a \| b` | `a.union(b)` | All 7 students |
| In `a` but not `b` | `a - b` | `a.difference(b)` | `{'Ahmed', 'Lucy', 'Mira'}` |

**Real-world pattern from the lecture:** loop through transactions and `add()` each customer name to an empty `set()`, which leaves the unique customers: Mira, Mohan and Lucy.

One small trap: `{}` creates an empty **dictionary**, not an empty set. Use `set()` instead.

## How this shows up in financial statement audit work

Many audit tests are really set questions. Which payees are missing from the approved list? Which employees are also suppliers? Which invoices appear twice? These snippets use small sample data built in the code.

**1. Payments to vendors that aren't in the vendor master.** This is the lecture's `a - b`:

```python
vendor_master = {"V001", "V002", "V003", "V004"}
paid_vendors = {"V001", "V003", "V009", "V012"}     # from the payments ledger

print(sorted(paid_vendors - vendor_master))   # ['V009', 'V012']: paid but never approved
print(sorted(vendor_master - paid_vendors))   # ['V002', 'V004']: approved but dormant, so consider deactivating them
```

**2. Employees who share a bank account with a vendor.** This is the lecture's `a & b`, a classic fictitious-vendor and conflict-of-interest test:

```python
employee_accounts = {"GB11-0001", "GB11-0002", "GB11-0003"}
vendor_accounts = {"GB22-7781", "GB11-0002", "GB22-9034"}

print(employee_accounts & vendor_accounts)    # {'GB11-0002'}: an employee is being paid as a vendor
```

**3. Unique customers in the revenue population.** This follows the lecture's transactions loop:

```python
sales = [
    {"invoice": "INV101", "customer": "C01", "amount": 12_500},
    {"invoice": "INV102", "customer": "C02", "amount": 8_400},
    {"invoice": "INV103", "customer": "C01", "amount": 3_100},
    {"invoice": "INV104", "customer": "C07", "amount": 92_000},
]

customers = set()
for sale in sales:
    customers.add(sale["customer"])

print(len(customers), sorted(customers))       # 3 ['C01', 'C02', 'C07']: agree to the AR confirmation population
```

**4. Spotting duplicate invoice numbers.** A set throws duplicates away, so comparing its size with the list's size reveals them:

```python
invoice_numbers = ["INV101", "INV102", "INV103", "INV102", "INV104", "INV101"]

print(len(invoice_numbers) - len(set(invoice_numbers)))   # 2: two invoice numbers appear more than once

seen, duplicates = set(), set()
for inv in invoice_numbers:
    if inv in seen:
        duplicates.add(inv)
    seen.add(inv)
print(sorted(duplicates))                       # ['INV101', 'INV102']: possible duplicate payments
```

**5. Frozensets for fixed rules and account pairs.** A frozenset can't be changed accidentally, and unlike a normal set it can be a dictionary key. That makes it useful for finding unusual debit and credit account combinations in journal entries, whichever side each account is on:

```python
RESTRICTED_ACCOUNTS = frozenset({"1999", "2999"})   # suspense accounts: fixed for the whole test

entries = [("JE1", "1200", "4000"), ("JE2", "4000", "1200"), ("JE3", "6300", "1999"), ("JE4", "1200", "4000")]

pair_counts = {}
for je_id, debit, credit in entries:
    pair = frozenset({debit, credit})               # {1200, 4000} is the same pair either way round
    pair_counts[pair] = pair_counts.get(pair, 0) + 1
    if pair & RESTRICTED_ACCOUNTS:
        print(f"{je_id}: posts to a suspense account")   # JE3

rare = [sorted(p) for p, n in pair_counts.items() if n == 1]
print(rare)                                          # [['1999', '6300']]: a pairing used only once, worth a look
```

## My reflection

Sets made several tests I usually build with VLOOKUPs and pivot tables feel almost trivial. "Paid but not approved" is just `paid - master`, and "employee and vendor" is just `employees & vendors`. The operators read like the audit question itself, which also makes the test easy for a reviewer to follow.

Two cautions I'll keep in mind. A set silently drops duplicates, which is great for finding unique values but means I must never use one to *count* transactions. And sets have no order, so any report that needs a stable order should use `sorted()`.
