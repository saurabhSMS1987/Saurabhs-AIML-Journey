# Handling Imbalanced Datasets: Notes

*Nov 2, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Handling Imbalanced Dataset** lecture notebook from my data science course by Krish Naik Acaedmy. Resampling uses scikit-learn's [`sklearn.utils.resample`](https://scikit-learn.org/stable/modules/generated/sklearn.utils.resample.html), and the class-weight alternative follows the [scikit-learn `LogisticRegression` documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).

## Where I started

Most of the data I look at in audit is *imbalanced* by nature: thousands of normal journal entries and a handful of problems. This lecture explained why that's a challenge for machine learning. A model trained on 900 "normal" examples and only 100 "unusual" ones learns mostly what normal looks like. It showed two simple fixes, **upsampling** and **downsampling**, that even out the classes before training.

## The data in brief

A simulated dataset of **1,000 rows** with two numeric features and a `target` label:

| Class | Rows | Share | Features centred on |
| --- | --- | --- | --- |
| 0 (majority) | 900 | 90% | 0 |
| 1 (minority) | 100 | 10% | 2 |

`np.random.seed(123)` makes the random data identical every time the notebook runs.

## What I learnt

**Split by class first:**

```python
df_minority = df[df["target"] == 1]      # 100 rows
df_majority = df[df["target"] == 0]      # 900 rows
```

**1. Upsampling: grow the minority class.** `resample()` draws minority rows **with replacement**, so rows are reused, until there are as many as the majority:

```python
from sklearn.utils import resample

df_minority_upsampled = resample(df_minority, replace=True,
                                 n_samples=len(df_majority), random_state=42)
df_upsampled = pd.concat([df_majority, df_minority_upsampled])
df_upsampled["target"].value_counts()    # 0: 900, 1: 900
```

**2. Downsampling: shrink the majority class.** The lecture's notebook set this up but its final cell was left unfinished. The standard call samples the **majority** class **without replacement** down to the minority's size:

```python
df_majority_downsampled = resample(df_majority, replace=False,
                                   n_samples=len(df_minority), random_state=42)
df_downsampled = pd.concat([df_majority_downsampled, df_minority])
df_downsampled["target"].value_counts()  # 0: 100, 1: 100
```

| | Upsampling | Downsampling |
| --- | --- | --- |
| What changes | Minority rows are duplicated | Majority rows are removed |
| `replace=` | `True` (rows reused) | `False` (each row at most once) |
| Result here | 1,800 rows (900 + 900) | 200 rows (100 + 100) |
| Risk | The model memorises the duplicates | Useful information is thrown away |

`random_state=42` makes the resampling repeatable, the same idea as a fixed seed for an audit sample.

## How this shows up in financial statement audit work

Fraud and error detection is the classic imbalanced problem. A model that learns from past journal entries labelled "issue" or "no issue" sees very few issues. These snippets use simulated entries built in the code.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

rng = np.random.default_rng(7)
n = 5_000
je = pd.DataFrame({
    "log_amount": rng.normal(8, 1.2, n),
    "after_hours": rng.binomial(1, 0.05, n),
    "manual": rng.binomial(1, 0.2, n),
})
risk = -6 + 0.35 * je["log_amount"] + 2.2 * je["after_hours"] + 1.5 * je["manual"]
je["issue"] = rng.binomial(1, 1 / (1 + np.exp(-risk)))      # 1 = entry later found to be an error or irregular
```

**1. Measure the imbalance first.**

```python
print(je["issue"].value_counts().to_dict(), f"{je['issue'].mean():.1%}")   # {0: 4605, 1: 395} 7.9%: about 1 issue in 13 entries
```

**2. The accuracy trap.** A "model" that calls every entry normal looks highly accurate but finds **nothing**:

```python
always_normal = np.zeros(len(je))
print(f"accuracy {(always_normal == je['issue']).mean():.1%}, issues found 0 of {je['issue'].sum()}")
# accuracy 92.1%, issues found 0 of 395
```

For audit, **recall** (the share of real issues the model catches) matters far more than accuracy.

**3. Resample the training data only, after splitting.** Upsampling before the split would copy the same entries into both training and test data, which makes results look better than they are:

```python
X, y = je[["log_amount", "after_hours", "manual"]], je["issue"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

train = pd.concat([X_train, y_train], axis=1)
minority, majority = train[train["issue"] == 1], train[train["issue"] == 0]
train_up = pd.concat([majority, resample(minority, replace=True, n_samples=len(majority), random_state=42)])

plain = LogisticRegression().fit(X_train, y_train)
upsampled = LogisticRegression().fit(train_up[X.columns], train_up["issue"])

print(f"recall without resampling: {recall_score(y_test, plain.predict(X_test)):.0%}")
print(f"recall with upsampling:    {recall_score(y_test, upsampled.predict(X_test)):.0%}")
# recall without resampling: 8%  ->  with upsampling: 71%
```

**4. An alternative that keeps the data unchanged: class weights.** Instead of copying rows, tell the model that mistakes on the rare class cost more:

```python
weighted = LogisticRegression(class_weight="balanced").fit(X_train, y_train)
print(f"recall with class weights: {recall_score(y_test, weighted.predict(X_test)):.0%}")
print(f"entries flagged for review: {weighted.predict(X_test).sum()} of {len(X_test)}")
# recall with class weights: 71% | entries flagged for review: 402 of 1500
```

The trade-off: catching more real issues also flags more normal entries for review. In audit, a manageable number of extra reviews is usually better than a missed irregularity.

## My reflection

This lecture gave me a name for something I see in every engagement: the interesting cases are rare. The accuracy trap was the most useful lesson. A model can be "99% accurate" and still miss every problem, so for audit work I'll judge models on how many real issues they catch.

The rule about resampling only the training data also felt familiar. It's the same principle as keeping test evidence independent of the work it's checking: anything that leaks between the two makes the results look better than they really are.
