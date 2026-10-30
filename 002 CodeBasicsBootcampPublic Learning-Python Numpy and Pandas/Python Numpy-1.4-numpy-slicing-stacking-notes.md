# NumPy Slicing and Stacking: My Lecture 17 Notes

*Oct 29, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **NumPy Slicing, Stacking** lecture from the **CodeBasics Python course**.

## Where I started

This lecture was about getting the right piece of data out of an array and putting pieces back together. That means slicing rows and columns, stacking tables, splitting them and filtering with conditions. It finished by finding the largest transaction in a small dataset, which is close to what I do when selecting high-value items for testing.

## What I learnt

**Slicing.** It works like list slicing, with a second position for columns:

| Code | Result | Meaning |
| --- | --- | --- |
| `a[0:2]` | `[6, 7]` | First two items |
| `a[-2:]` | `[8, 9]` | Last two items |
| `b[1, 2]` | `6` | Row 1, column 2 |
| `b[0:2, 2]` | `[3, 6]` | Rows 0–1 of column 2 |
| `b[-1, 0:2]` | `[7, 8]` | Last row, first two columns |
| `b[:, 1:3]` | Columns 1–2 of every row | `:` means "all rows" |

**Stacking and splitting:**

- `np.vstack((c, e))` stacks tables **on top** of each other: more rows.
- `np.hstack((c, d))` places tables **side by side**: more columns.
- `np.hsplit(t, [3])` splits off columns from position 3, and `np.vsplit(t, [4])` splits off rows from position 4.

**Two things I noticed with stacking:**

1. NumPy arrays hold a single type. Mixing IDs, names, amounts and dates turned *everything* into text (`dtype='<U32'`), so `250.5` became `'250.5'`. The lecture needed `.astype(float)` before it could find the maximum.
2. `hstack` simply puts rows next to each other in order. It doesn't match them by customer ID; the ID column just appeared twice. If the two tables had been in a different order, the purchases would have been attached to the wrong customers without any error.

**Boolean filtering:**

```python
monthly_sales = np.array([30, 33, 35, 28, 42])
result = monthly_sales < 32       # [ True False False  True False]
monthly_sales[result]             # [30, 28]: only the matching values
monthly_sales[result] = -1        # replaces matching values in the original array
```

**argmax** returns the **position** of the largest value: `np.argmax(monthly_sales)` gives `4`. Combined with `.astype(float)`, the lecture found the largest transaction, David's `400.2`. Filtering with `transactions[transactions[:, 0] == "101"]` pulled out one customer's rows.

## How this shows up in healthcare audit work

These snippets use the same tools to slice, combine and filter healthcare billing data.

**1. Slicing a provider-by-month table.**

```python
import numpy as np

# rows: City Hospital, Lakeside Clinic, North Medical | columns: Jan–Jun billing ($000s)
billed = np.array([[420, 435, 410, 425, 430, 415],
                   [180, 175, 190, 185, 390, 410],
                   [300, 310, 305, 295, 300, 310]])

print(billed[:, 3:])       # Q2 only (Apr–Jun) for every provider
print(billed[1, -2:])      # [390 410]: Lakeside's last two months, roughly double its usual
```

**2. Combining monthly claim extracts safely.** `vstack` builds the full population, and a quick check confirms that two tables line up before `hstack`.

```python
jan = np.array([[5001, 1200.0], [5002, 860.0]])
feb = np.array([[5003, 4300.0], [5004, 950.0]])
population = np.vstack((jan, feb))              # 4 claims in one table

claim_ids = np.array([5001, 5002, 5003, 5004])
diagnosis = np.array([5001, 5003, 5002, 5004])  # same claims, different order!
print(np.all(claim_ids == diagnosis))           # False: sort or match before using hstack
```

**3. Filtering claims with a condition.**

```python
charges = np.array([1200, 18500, 640, -300, 45000, 0])

print(charges[charges > 10000])   # [18500 45000]: high-value claims to test
print(charges[charges <= 0])      # [-300    0]: zero or negative charges to investigate
```

**4. Finding the highest claim, and every claim for one patient.** This is the lecture's `argmax` and ID filter, applied to claims.

```python
claims = np.array([
    ["C-01", "P-778", "1450.00",  "2026-08-01"],
    ["C-02", "P-312", "22800.50", "2026-08-02"],
    ["C-03", "P-778", "1450.00",  "2026-08-01"],
])

top = np.argmax(claims[:, 2].astype(float))
print(claims[top])                            # C-02: the largest claim

print(claims[claims[:, 1] == "P-778"])        # C-01 and C-03: same patient, amount and date, so a possible duplicate bill
```

## My reflection

The `hstack` example is the one I'll remember. It's essentially a VLOOKUP that doesn't look anything up: it trusts that both tables are already in the same order. In audit, that's exactly how a reconciliation goes wrong without anyone noticing, so I'll always check that the IDs line up first. Boolean filtering felt like the most immediately useful tool. One line pulls out every claim above a threshold or every zero-value charge, and that is the core of exception testing.

Next, I want to practise:

- [ ] Stack three months of claim extracts with `vstack` and total the population
- [ ] Filter claims above a review threshold and claims with zero or negative charges
- [ ] Find possible duplicate bills by filtering on patient ID and comparing date and amount
