# Handling Outliers: Notes

*Nov 3, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Handling Outliers** lecture from **Krish Naik Academy**.

## Where I started

Outliers are a familiar idea from audit: the unusually large payment, the expense claim that doesn't fit the pattern. This lecture gave me a simple, standard way to define "unusual" with numbers instead of judgement alone: the **five-number summary**, the **interquartile range (IQR)** and the **box plot** that draws them.

## The data in brief

Two lists of student marks:

| | First list | Second list |
| --- | --- | --- |
| Values | 17 marks, from 32 to 99 | The same 17, plus `-100`, `-200`, `150`, `170` and `180` (22 in total) |
| Q1 / median / Q3 | 54 / 67 / 89 | 47.25 / 70.5 / 89.75 |
| IQR | 35 | 42.5 |
| Fences | 1.5 to 141.5 | -16.5 to 153.5 |
| Outliers | None | `-200`, `-100`, `170`, `180` |

In the second list, **150 isn't an outlier**. It's high, but it falls inside the upper fence of 153.5.

## What I learnt

**The five-number summary:** minimum, first quartile (Q1), median, third quartile (Q3) and maximum.

```python
import numpy as np

lst_marks = [45, 32, 56, 75, 89, 54, 32, 89, 90, 87, 67, 54, 45, 98, 99, 67, 74]
minimum, Q1, median, Q3, maximum = np.quantile(lst_marks, [0, 0.25, 0.50, 0.75, 1.0])
# (32.0, 54.0, 67.0, 89.0, 99.0)
```

**The IQR and the fences:**

```python
IQR = Q3 - Q1                       # 35.0: the spread of the middle 50%
lower_fence = Q1 - 1.5 * IQR        # 1.5
higher_fence = Q3 + 1.5 * IQR       # 141.5
```

Anything below the lower fence or above the higher fence counts as an **outlier**.

| Term | Meaning |
| --- | --- |
| Q1 (25th percentile) | A quarter of the values are below it |
| Median (50th percentile) | The middle value |
| Q3 (75th percentile) | Three quarters of the values are below it |
| IQR = Q3 − Q1 | The range of the middle half of the data |
| Fences = Q1 − 1.5×IQR and Q3 + 1.5×IQR | The boundaries for "normal" |

**The box plot draws all of this at once.** `sns.boxplot(lst_marks)` shows a box from Q1 to Q3, a line at the median, whiskers out to the furthest values inside the fences, and individual dots for outliers. The first list's plot had no dots. The second showed four.

**Why the IQR method works well:** it's based on quartiles, so the extreme values themselves don't shift the fences much. An average would be pulled towards the outliers it's trying to detect.

## How this shows up in financial statement audit work

The IQR method is a quick, explainable way to find unusual amounts in a population, a natural fit for analytical procedures and for selecting items to test. These snippets use simulated expense claims built in the code.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(3)
claims = pd.DataFrame({
    "claim_id": [f"EC{i:04d}" for i in range(600)],
    "category": rng.choice(["Meals", "Travel", "Hotel"], 600, p=[0.5, 0.2, 0.3]),
})
typical = claims["category"].map({"Meals": 60, "Travel": 450, "Hotel": 180})
claims["amount"] = (typical * rng.lognormal(0, 0.35, 600)).round(2)
claims.loc[[17, 230, 455], ["category", "amount"]] = [["Meals", 240.00], ["Hotel", 2_100.00], ["Travel", 4_250.00]]   # three unusual claims
```

**1. IQR fences on the whole population**, exactly as in the lecture:

```python
def iqr_fences(values):
    q1, q3 = np.quantile(values, [0.25, 0.75])
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

low, high = iqr_fences(claims["amount"])
overall = claims[(claims["amount"] < low) | (claims["amount"] > high)]
print(round(high, 2), len(overall))           # 509.4 51
print(overall["category"].value_counts().to_dict())   # {'Travel': 50, 'Hotel': 1}: almost all ordinary travel claims
```

**2. Fences per category.** One set of fences for everything mostly flags travel claims, simply because travel is expensive, and it misses a $240 *meal*, four times a typical meal but below the overall fence. Calculating fences within each category finds what's unusual *for its type*:

```python
grouped = claims.groupby("category")["amount"]
q1 = grouped.transform(lambda s: s.quantile(0.25))     # each claim gets its own category's Q1...
q3 = grouped.transform(lambda s: s.quantile(0.75))     # ...and Q3
iqr = q3 - q1
claims["category_outlier"] = (claims["amount"] < q1 - 1.5 * iqr) | (claims["amount"] > q3 + 1.5 * iqr)

by_category = claims[claims["category_outlier"]]
print(by_category.groupby("category").size().to_dict())   # {'Hotel': 5, 'Meals': 7, 'Travel': 2}: 14 in total
print(claims.loc[[17, 230, 455], ["claim_id", "category", "amount", "category_outlier"]].to_string(index=False))
# EC0017 Meals 240.0 True | EC0230 Hotel 2100.0 True | EC0455 Travel 4250.0 True: all three unusual claims caught
```

**3. A box plot per category for the workpaper:**

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
sns.boxplot(data=claims, x="category", y="amount", ax=ax)
ax.set_yscale("log")                       # categories differ a lot in scale
ax.set_title("Expense claims by category: dots are outliers")
fig.savefig("expense_outliers.png", dpi=150)
plt.close(fig)
```

**4. Skewed amounts: check on a log scale too.** Financial amounts are usually right-skewed, with many small values and a long tail of large ones. On the raw scale, the upper fence flags many ordinary large values. Taking logs first makes the shape more symmetric, so only the truly unusual stand out:

```python
meals = claims.loc[claims["category"] == "Meals", "amount"]
raw_low, raw_high = iqr_fences(meals)
log_low, log_high = iqr_fences(np.log(meals))
print(((meals < raw_low) | (meals > raw_high)).sum(), "flagged on the raw scale")   # 7
print(((np.log(meals) < log_low) | (np.log(meals) > log_high)).sum(), "flagged on the log scale")   # 5
```

## My reflection

The five-number summary gave me a clean, defensible definition of "unusual". It's a rule I can explain to a client or a reviewer in one sentence, which matters more in audit than a clever method nobody can follow. And the box plot shows the whole population and its outliers in one picture.

The big difference from the lecture's framing is what happens *next*. In data science, outliers are often removed or capped so they don't distort a model. In audit, an outlier is a **selection for testing**: I find out why it's unusual and never quietly delete it. The per-category example made that sharper. "Unusual" only means something relative to the right comparison group.
