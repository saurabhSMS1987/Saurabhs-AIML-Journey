# SMOTE (Synthetic Minority Oversampling): Notes

*Nov 3, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **SMOTE** lecture from **Krish Naik Academy**. SMOTE comes from the [imbalanced-learn library](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html).

## Where I started

In the last lecture, I balanced a dataset by **upsampling**, copying minority rows until the classes matched. The weakness was obvious: the model sees the same few rows again and again. **SMOTE** takes a smarter approach. Instead of copying rows, it creates **new, synthetic** minority examples that sit *between* real ones, so the minority class grows without exact duplicates.

## The data in brief

A dataset generated with scikit-learn's `make_classification`: **1,000 rows**, two features (`f1`, `f2`) and a `target` column.

| | Before SMOTE | After SMOTE |
| --- | --- | --- |
| Class 0 (majority) | 900 | 900 |
| Class 1 (minority) | 100 | 900 |
| Total rows | 1,000 | 1,800 |

The lecture drew scatter plots before and after. The 800 new minority points filled in the space *around* the original 100, rather than stacking on top of them.

## What I learnt

**How SMOTE works:** for each minority example, it finds its nearest minority neighbours (5 by default), picks one, and creates a new point somewhere on the line between the two. Every synthetic row is a blend of two real ones.

```python
from sklearn.datasets import make_classification
import pandas as pd

X, y = make_classification(n_samples=1000, n_redundant=0, n_features=2,
                           n_clusters_per_class=1, weights=[0.90], random_state=12)
final_df = pd.concat([pd.DataFrame(X, columns=["f1", "f2"]),
                      pd.DataFrame(y, columns=["target"])], axis=1)
final_df["target"].value_counts()          # 0: 900, 1: 100
```

```python
from imblearn.over_sampling import SMOTE

oversample = SMOTE()
X, y = oversample.fit_resample(final_df[["f1", "f2"]], final_df["target"])
X.shape                                    # (1800, 2)
len(y[y == 0]), len(y[y == 1])             # (900, 900)
```

**`fit_resample()`** both learns from the data and returns the balanced version, features and labels together.

**Installing it:** the lecture ran `pip install imblearn`. That's a small placeholder package that pulls in the real library, so `pip install imbalanced-learn` installs it directly.

| | Upsampling (last lecture) | SMOTE |
| --- | --- | --- |
| New minority rows | Exact copies | New, synthetic points between real neighbours |
| Risk of memorising duplicates | High | Lower |
| Works with | Any data | **Numeric features** (categorical columns need the `SMOTENC` variant) |
| Library | `sklearn.utils.resample` | `imblearn.over_sampling.SMOTE` |

## How this shows up in financial statement audit work

Labelled irregular journal entries are rare, so SMOTE can help train a model to recognise them. Two rules matter: use SMOTE **only to train models**, never to change a test population, and apply it **only to the training split**. These snippets use simulated entries built in the code.

```python
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(7)
n = 5_000
je = pd.DataFrame({
    "log_amount": rng.normal(8, 1.2, n),
    "hour_posted": rng.integers(0, 24, n),
    "days_to_period_end": rng.integers(0, 31, n),
})
risk = -9 + 0.5 * je["log_amount"] + 1.8 * ((je["hour_posted"] < 6) | (je["hour_posted"] > 21)) \
       + 1.2 * (je["days_to_period_end"] < 3)
je["issue"] = rng.binomial(1, 1 / (1 + np.exp(-risk)))
X, y = je.drop(columns="issue"), je["issue"]
```

**1. SMOTE on the training split only.** Split first, so the test set contains only real entries:

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
X_res, y_res = SMOTE(random_state=42).fit_resample(X_train, y_train)

print(y_train.value_counts().to_dict(), "->", y_res.value_counts().to_dict())
# {0: 3412, 1: 88} -> {0: 3412, 1: 3412}: 88 real issues become 3,412 for training
```

**2. Does it help the model catch more issues?**

```python
plain = LogisticRegression(max_iter=1000).fit(X_train, y_train)
smoted = LogisticRegression(max_iter=1000).fit(X_res, y_res)

print(f"recall without SMOTE: {recall_score(y_test, plain.predict(X_test)):.0%}")
print(f"recall with SMOTE:    {recall_score(y_test, smoted.predict(X_test)):.0%}")
print(f"entries flagged:      {smoted.predict(X_test).sum()} of {len(X_test)}")
# recall 0% -> 84%, with 594 of 1,500 entries flagged for review
```

**3. When there are very few known issues.** SMOTE needs at least `k_neighbors + 1` minority examples, 6 by default. With only a handful of confirmed irregularities, lower `k_neighbors`:

```python
few = je[je["issue"] == 0].head(300)
few = pd.concat([few, je[je["issue"] == 1].head(4)])        # only 4 known issues

try:
    SMOTE(random_state=42).fit_resample(few.drop(columns="issue"), few["issue"])
except ValueError as e:
    print("Default settings fail:", str(e)[:60], "...")    # Expected n_neighbors <= n_samples_fit ...

X_small, y_small = SMOTE(k_neighbors=2, random_state=42).fit_resample(few.drop(columns="issue"), few["issue"])
print(y_small.value_counts().to_dict())                     # {0: 300, 1: 300}
```

With so few real examples, every synthetic entry is built from the same handful of cases. The model will be narrow, so treat its output as one input to risk assessment, not a conclusion.

**4. Keep synthetic rows out of the evidence.** SMOTE puts its new rows *after* the originals. Tagging them makes clear that they're invented and must never be selected for testing or reported:

```python
X_res = X_res.assign(synthetic=[False] * len(X_train) + [True] * (len(X_res) - len(X_train)))
print(X_res["synthetic"].value_counts().to_dict())          # {False: 3500, True: 3324}
```

## My reflection

SMOTE solves the problem I noticed with upsampling. Instead of showing the model the same rare entries over and over, it fills in the space around them with plausible new examples. The scatter plots made that very clear.

But "synthetic" is the word I'll keep in mind. These rows were never posted by anyone. They're useful for teaching a model what an unusual entry looks like, and nothing more. In audit, evidence has to come from real transactions, so synthetic data belongs in model training and nowhere near a sample or a finding.
