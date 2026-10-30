# NumPy Basic Operations: My Lecture 15 Notes

*Oct 29, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **NumPy Basic Operations** lecture from the **CodeBasics Python course**.

## Where I started

Last lecture showed *why* NumPy is useful. This one showed how to work with it day to day: building tables of numbers, looking up and changing values, checking their size and type, and summarising them by row or by column. The quarterly revenue example felt just like a spreadsheet, so it was easy to picture the same steps on hospital billing data.

## What I learnt

**Dimensions.** A single row of revenues is 1-D (`ndim` is 1), and two quarters stacked as rows form a 2-D table (`ndim` is 2):

```python
rev = np.array([[10, 12, 9],     # Q1: months 1-3
                [15, 11, 13]])   # Q2: months 1-3
```

**Indexing.** `rev[1, 0]` means row 1, column 0: the first month of Q2, which is 15. Assigning `rev[1, 0] = 14` updates that value.

**Describing an array:**

| Attribute | Result for `rev` | Meaning |
| --- | --- | --- |
| `ndim` | `2` | Number of dimensions |
| `shape` | `(2, 3)` | 2 rows, 3 columns |
| `size` | `6` | Total number of values |
| `dtype` | `int32` (or `float64` if set) | Type of every value |
| `itemsize` | `4` (or `8` for `float64`) | Bytes per value |

**Creating arrays quickly:**

- `np.zeros((3, 4))` and `np.ones((3, 4))` create tables filled with 0s or 1s.
- `np.arange(20, 30, 2)` counts with a step: `[20, 22, 24, 26, 28]`.
- `np.linspace(10, 50, 10)` gives 10 evenly spaced values from 10 to 50, including both ends.

**Reshaping:**

- `flatten()` and `ravel()` both turn a table into one row. `flatten()` always makes a copy, while `ravel()` may share data with the original.
- `reshape(3, 2)` rearranges the same 6 values into 3 rows and 2 columns. `reshape(2, 4)` raised a `ValueError`, because 6 values can't fill 8 slots.

**Summarising.** `min()`, `max()`, `np.sort(rev, axis=None)` and the key idea, **axis**:

```python
rev.sum(axis=0)   # down the columns: [25, 23, 22], one total per month position
rev.sum(axis=1)   # across the rows:  [31, 39], one total per quarter
```

**Maths on every value:** `np.sqrt`, `np.square` and `np.std` (standard deviation, a measure of spread).

## How this shows up in healthcare audit work

Healthcare billing data is naturally a table: providers by month, procedures by department, patients by length of stay. These snippets use the lecture's tools on that kind of data.

**1. Billing totals by provider and by month.** `axis` gives both views of the same table.

```python
import numpy as np

# rows: City Hospital, Lakeside Clinic, North Medical | columns: Jan, Feb, Mar (in $000s)
billed = np.array([[420, 435, 410],
                   [180, 175, 390],
                   [300, 310, 305]])

print(billed.sum(axis=1))   # [1265  745  915]: total per provider
print(billed.sum(axis=0))   # [ 900  920 1105]: total per month
print(billed[1, 2])         # 390: Lakeside's March billing, more than double its usual
```

**2. Length-of-stay outliers with `np.std`.** Stays far above the average can point to upcoding or billing for unnecessary days.

```python
stays = np.array([3, 4, 2, 5, 3, 4, 21, 3, 4])   # days per inpatient admission
threshold = stays.mean() + 2 * stays.std()
print(stays[stays > threshold])                  # [21]: review this admission
```

`stays[stays > threshold]` is a NumPy shortcut that keeps only the values meeting the condition, like a filter in Excel. It isn't covered in this lecture, but it fits naturally here.

**3. The `dtype` trap with billed amounts.** Forcing whole numbers silently drops the cents, so small errors add up across thousands of claims.

```python
charges = [99.99, 150.50, 75.25]
print(np.array(charges, dtype=np.int32))         # [ 99 150  75]: cents lost
print(np.array(charges, dtype=np.float64))       # [ 99.99 150.5   75.25]: correct
```

**4. Highest charges first, for high-value testing.**

```python
claim_charges = np.array([1200, 18500, 640, 9200, 45000, 3100])
print(np.sort(claim_charges)[-3:])               # [ 9200 18500 45000]: top three to test
```

## My reflection

`axis` was the idea that clicked for me. The same table answers two different audit questions: which provider is billing the most, and which month spiked. One small argument switches between them. The `dtype` example was a good warning too. NumPy dropped the cents without any error. With healthcare charges across thousands of claims, that's how a reconciliation ends up off by an amount nobody can explain. So I'll check `dtype` before trusting any totals.
