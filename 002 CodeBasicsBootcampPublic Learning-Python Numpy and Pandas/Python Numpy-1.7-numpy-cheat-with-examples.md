# NumPy Cheat Sheet: Insurance Examples

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Commands are based on the ***NumPy Cheat Sheet*** by **Dataquest** ([dataquest.io/guide](https://www.dataquest.io/guide)). The insurance examples are my own, built on small sample data so every snippet runs as written.

The cheat sheet uses NYC taxi data. I've redone each section with insurance claims and premiums, the kind of data I test in audit.

## Sample data used throughout

```python
import numpy as np

# columns: claim_id, line (0 = motor, 1 = property, 2 = health), paid, reserve, sum_insured
claims = np.array([
    [1001, 0,  42000,  5000,  50000],
    [1002, 1, 260000, 20000, 250000],
    [1003, 2,  18500,     0,  30000],
    [1004, 0,  95000, 10000, 100000],
    [1005, 1,      0, 75000, 500000],
    [1006, 2,  31000,  2000,  30000],
])
```

All columns are numbers, with the line of business stored as a code. Mixing text and numbers in one NumPy array turns *everything* into text, so numeric codes keep the maths working.

## 1. Importing and exporting

```python
np.savetxt("claims.csv", claims, delimiter=",", fmt="%d",
           header="claim_id,line,paid,reserve,sum_insured", comments="")

loaded = np.genfromtxt("claims.csv", delimiter=",", skip_header=1)
print(loaded.shape)                        # (6, 5)
print(np.array_equal(loaded, claims))      # True: the file round-trips exactly
```

`np.loadtxt` works for clean files. `np.genfromtxt` is more forgiving, because it turns blanks into `nan` instead of failing.

## 2. Creating arrays

```python
exceptions = np.zeros(3)                         # counters: [0. 0. 0.] for motor, property, health
deductibles = np.full(6, 1000)                   # standard $1,000 deductible on every claim
policy_years = np.arange(2020, 2027)             # 2020 ... 2026
premium_bands = np.linspace(0, 100000, 5)        # [0, 25000, 50000, 75000, 100000]

rng = np.random.default_rng(seed=42)             # fixed seed, so the sample can be re-performed
sample = rng.choice(claims[:, 0], size=3, replace=False)
print(sample)                                    # the same 3 claim IDs every run
```

For audit sampling, a **fixed seed** matters: a reviewer can re-run the code and get exactly the same sample. `np.random.rand` and `randint` still work, but `default_rng` is NumPy's recommended approach now.

## 3. Inspecting properties

```python
print(claims.shape)        # (6, 5): 6 claims, 5 columns
print(claims.size)         # 30 values
print(claims.dtype)        # int64

paid = claims[:, 2].astype(float)     # convert before dividing
print(paid.tolist()[:3])              # [42000.0, 260000.0, 18500.0]: back to a plain list
```

## 4. Copying, sorting and reshaping

```python
working = np.copy(claims)             # always test on a copy, never the source data

sorted_paid = np.sort(claims[:, 2])[::-1]
print(sorted_paid[:3])                # [260000  95000  42000]: largest first, for high-value testing

monthly_premium = np.array([110, 95, 120, 130, 125, 140, 150, 145, 135, 128, 118, 160])
quarters = monthly_premium.reshape(4, 3)      # 4 quarters × 3 months
print(quarters.sum(axis=1))                   # [325 395 430 406]: premium per quarter
print(quarters.T.shape)                       # (3, 4): transposed
```

**Copy or view?** A slice like `claims[:, 2]` is a *view*: changing it changes `claims` too. Use `np.copy()` whenever you plan to adjust figures, so the original extract stays untouched.

## 5. Adding and removing elements

```python
late_claim = np.array([[1007, 0, 12000, 0, 40000]])
working = np.append(working, late_claim, axis=0)   # a claim reported after the cut-off
working = np.delete(working, 4, axis=0)            # remove claim 1005 (withdrawn)
print(working[:, 0])                               # [1001 1002 1003 1004 1006 1007]
```

Without `axis=0`, `np.append` flattens everything into one long row, which is a common surprise.

## 6. Combining and splitting

```python
q1_paid = np.array([42000, 260000, 18500])
q2_paid = np.array([95000, 0, 31000])
half_year = np.concatenate((q1_paid, q2_paid))     # 6 claims

batches = np.split(half_year, 3)                   # 3 equal batches for 3 reviewers
print([b.tolist() for b in batches])               # [[42000, 260000], [18500, 95000], [0, 31000]]
```

`np.split` needs the array to divide evenly. For uneven splits, use `np.array_split`.

## 7. Indexing, slicing and conditions

```python
paid, reserve, limit = claims[:, 2], claims[:, 3], claims[:, 4]

over_limit = claims[paid > limit]
print(over_limit[:, 0])                            # [1002 1006]: paid above the sum insured

big_motor = claims[(claims[:, 1] == 0) & (paid > 50000)]
print(big_motor[:, 0])                             # [1004]

nil_paid_open = claims[(paid == 0) | (reserve > 50000)]
print(nil_paid_open[:, 0])                         # [1005]: nothing paid, large reserve

not_health = claims[~(claims[:, 1] == 2)]
print(len(not_health))                             # 4
```

Use `&` for "and", `|` for "or" and `~` for "not", and put each condition in brackets.

## 8. Scalar maths: one number applied to every value

```python
indexed_limits = np.multiply(limit, 1.05)          # 5% inflation indexation
print(indexed_limits[:2])                          # [ 52500. 262500.]

loss_ratio = np.divide(paid.sum(), 1_250_000) * 100
print(round(loss_ratio, 1))                        # 35.7 (% of $1.25m earned premium)
```

## 9. Vector maths: value by value

```python
net_paid = np.subtract(paid, deductibles)          # claim minus deductible
incurred = np.add(paid, reserve)                   # paid + outstanding reserve
print(incurred)                                    # [ 47000 280000  18500 105000  75000  33000]

system_incurred = np.array([47000, 280000, 18500, 105000, 75000, 33500])
print(np.array_equal(incurred, system_incurred))   # False: the reconciliation has a break
print(np.abs(incurred - system_incurred))          # [  0   0   0   0   0 500]: claim 1006 is out by 500

print(np.ceil(4_830_000 / 250_000))                # 20.0: a sample size always rounds up
print(np.round([0.5, 1.5, 2.5, 3.5]))              # [0. 2. 2. 4.]: see the rounding note below
```

**Rounding note:** `np.round` uses *banker's rounding*, where halves round to the nearest even number. So 2.5 becomes 2, not 3. That's sound statistically, but it can create small differences against systems or Excel, which round halves up.

## 10. Statistics

```python
print(paid.mean())                                 # 74416.66... average paid claim
print(paid.std().round(0))                         # spread of claim sizes
print(np.var(paid).round(0))

by_line = np.array([[42000, 95000, 61000],         # rows: motor, property, health
                    [260000, 0, 120000],           # columns: Q1, Q2, Q3 paid
                    [18500, 31000, 27000]])
print(by_line.max(axis=1))                         # [ 95000 260000  31000]: largest quarter per line
print(np.mean(by_line, axis=0).round(0))           # average across lines, per quarter

premium = np.array([900, 1200, 750, 1500, 1100, 2000])
claim_cost = np.array([300, 650, 200, 900, 400, 1300])
print(np.corrcoef(premium, claim_cost)[0, 1].round(2))   # 0.99: pricing tracks risk
```

## 11. Working with data: flag and assign

```python
flags = np.zeros(len(claims), dtype=int)
flags[paid > limit] = 1                                  # 1 = exception
print(np.column_stack((claims[:, 0], flags)))
# [[1001 0] [1002 1] [1003 0] [1004 0] [1005 0] [1006 1]]

print(f"{flags.sum()} of {len(flags)} claims exceed the sum insured")   # 2 of 6
```

## Corrections to the cheat sheet

I tested every command on NumPy 2.x, and a few lines are wrong or easy to misread:

| Cheat sheet | What actually happens | Use instead |
| --- | --- | --- |
| `arr.corrcoef()` | Raises an error: arrays have no `corrcoef` method | `np.corrcoef(a, b)` |
| `np.divide(arr, 4)` "returns `nan` for division by zero" | `x / 0` gives `inf`; only `0 / 0` gives `nan` | Check for zeros before dividing |
| `np.hsplit(arr, 5)` "splits on index 5" | `5` means *5 equal parts* | `np.hsplit(arr, [5])` to split at index 5 |
| `arr.view(dtype)` | Reinterprets the raw bytes and doesn't convert values | `arr.astype(dtype)` to convert |
| `np.round(arr)` "to the nearest integer" | Halves go to the nearest **even** number | Be aware when reconciling to other systems |
| `arr.resize((5, 6))` | Fails if other variables refer to `arr` | `np.resize()` returns a new array, but repeats values instead of padding with 0 |

## What stuck with me

Most of this cheat sheet is a few steps: select a column, compare it with another and pull out the exceptions. The details are what catch people out: views that change the source data, banker's rounding and `np.append` without an axis. In audit, those are exactly the issues that turn a clean reconciliation into an unexplained difference.
