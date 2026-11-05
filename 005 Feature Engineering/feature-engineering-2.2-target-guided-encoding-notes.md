# Target Guided Ordinal Encoding: Notes

*Nov 4, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Target Guided Ordinal Encoding** lecture from **Krish Naik Academy**.

## Where I started

The last two lectures encoded categories by their names: alphabetically (label encoding) or by an order I chose (ordinal encoding). This lecture took a different approach: **let the data decide the order**. Each category is replaced by a number based on how the **target** behaves for that category, such as the average price per city. It's the final technique in the course's encoding series, after one-hot, label and ordinal.

## The data in brief

A small table of **6 prices across 4 cities**:

| City | Prices | Mean price |
| --- | --- | --- |
| London | 150 | 150.0 |
| New York | 200, 180 | 190.0 |
| Tokyo | 250 | 250.0 |
| Paris | 300, 320 | 310.0 |

The seaborn **tips** dataset (244 restaurant bills) was also loaded as a larger example to practise on.

## What I learnt

**Step 1: the mean of the target for each category.**

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["New York", "London", "Paris", "Tokyo", "New York", "Paris"],
    "price": [200, 150, 300, 250, 180, 320],
})
mean_price = df.groupby("city")["price"].mean().to_dict()
# {'London': 150.0, 'New York': 190.0, 'Paris': 310.0, 'Tokyo': 250.0}
```

**Step 2: replace each category with its mean.**

```python
df["city_encoded"] = df["city"].map(mean_price)
# New York -> 190.0, London -> 150.0, Paris -> 310.0, Tokyo -> 250.0
```

Now the encoded column moves **in step with the target**: cities with higher prices get higher numbers. That **monotonic relationship** is what makes this encoding useful to a model.

**Why use it:** one-hot encoding needs a column per category, which is impractical with hundreds of cities, vendors or products. Target guided encoding uses **one column**, however many categories there are.

**Two variations of the same idea:**

| Variation | Each category becomes | City example |
| --- | --- | --- |
| **Mean encoding** (the lecture's code) | Its average target value | London 150, New York 190, Tokyo 250, Paris 310 |
| **Ordinal ranking** | Its *rank* after sorting by the mean | London 0, New York 1, Tokyo 2, Paris 3 |

The lecture's text also mentions the **median**, which is safer when a category contains outliers.

**Two cautions this method needs:**

1. **Learn the means from training data only.** The encoding uses the target itself, so calculating it on data the model will later be tested on "leaks" the answer and makes results look better than they are.
2. **Small categories are noisy.** London's 150 rests on a single price, so one unusual value could swing it. Categories with few rows deserve less trust.

## How this shows up in financial statement audit work

With hundreds of vendors, accounts or users, target guided encoding can turn each one into a single, meaningful number: its **historical exception rate**. These snippets use simulated journal entries built in the code. The target is whether an entry turned out to be an issue (1) or not (0).

```python
import numpy as np

rng = np.random.default_rng(5)
vendor_risk = {"V01": 0.02, "V02": 0.03, "V03": 0.25, "V04": 0.05, "V05": 0.40}
rows = []
for year in (2025, 2026):
    for vendor, p in vendor_risk.items():
        n = 3 if vendor == "V05" else 60                    # V05 is a rarely used vendor
        rows += [{"year": year, "vendor": vendor, "issue": int(rng.random() < p)} for _ in range(n)]
je = pd.DataFrame(rows)
history, current = je[je["year"] == 2025], je[je["year"] == 2026]
```

**1. A vendor risk score from history.** The prior year's (FY2025) exception rate for each vendor becomes its encoded value:

```python
vendor_rate = history.groupby("vendor")["issue"].mean()
print(vendor_rate.round(3).to_dict())
# {'V01': 0.05, 'V02': 0.033, 'V03': 0.233, 'V04': 0.05, 'V05': 0.667}: V03 stands out among the regular vendors
```

**2. Apply it to the current year, never re-fitting on it.** The current year's outcomes are what we're testing, so they mustn't feed the encoding (no leakage). A vendor with no history gets the overall average:

```python
overall_rate = history["issue"].mean()
current = current.assign(vendor_score=current["vendor"].map(vendor_rate).fillna(overall_rate))
new_vendor = pd.Series(["V99"]).map(vendor_rate).fillna(overall_rate)
print(round(new_vendor[0], 3), "assigned to a vendor with no history")   # 0.099: the overall FY2025 rate
```

**3. The ordinal version: rank vendors by risk.**

```python
risk_rank = vendor_rate.rank(method="dense").astype(int) - 1     # 0 = lowest exception rate
print(risk_rank.sort_values().to_dict())
# {'V02': 0, 'V01': 1, 'V04': 1, 'V03': 2, 'V05': 3}: V01 and V04 tie, so they share a rank
```

**4. Smoothing for vendors with little history.** V05 has only 3 entries, so its raw rate is unreliable. Smoothing blends each vendor's rate with the overall rate, weighted by how many entries it has:

```python
stats = history.groupby("vendor")["issue"].agg(["mean", "count"])
weight = 10                                                      # behaves like 10 "average" entries
stats["smoothed"] = (stats["count"] * stats["mean"] + weight * overall_rate) / (stats["count"] + weight)
print(stats.round(3).to_string())
# V05: raw rate 0.667 from just 3 entries -> smoothed 0.230 | V03: 0.233 from 60 entries -> 0.214
```

With 60 entries, a vendor's own history dominates. With 3, its score is pulled towards the average until there's more evidence.

## My reflection

This encoding felt the most "audit-like" of the series. Turning each vendor or user into its **historical exception rate** is essentially what an experienced auditor carries in their head: "this supplier has caused problems before". The method just makes that memory explicit and consistent.

The two cautions matter just as much. Using this year's outcomes to score this year's entries would be circular, like grading a test with the answer key. And a vendor with three transactions shouldn't be labelled high-risk on such thin evidence. Learning from history and smoothing small groups keep the score honest.
