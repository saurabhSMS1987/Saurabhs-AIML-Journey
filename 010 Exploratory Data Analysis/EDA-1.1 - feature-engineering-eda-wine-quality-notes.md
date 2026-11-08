# Exploratory Data Analysis (EDA): Red Wine Quality: My Notes

*Nov 7, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **EDA with Red Wine Data** lecture from **Krish Naik Academy**.

## Where I started

The earlier lectures taught individual techniques: handling missing values, outliers, imbalance and encoding. This one put them in order on a real dataset. **Exploratory data analysis** is the first pass over any new data: what's in it, what's wrong with it, and which variables matter, all before any modelling. It felt very familiar, because it's essentially the planning and risk-assessment stage of an audit, applied to a dataset.

## The data in brief

The **red "Vinho Verde" wine dataset**: **1,599 wines**, each with 11 chemical measurements (acidity, sugar, sulphur dioxide, pH, alcohol and so on) and a **quality score** from tasters, ranging from **3 to 8**.

| Check | Result |
| --- | --- |
| Rows × columns | 1,599 × 12 |
| Missing values | None |
| Duplicate rows | **240**, removed to leave **1,359** |
| Quality scores | 3–8, with a median of 6. Most wines score 5 or 6, so the data is **imbalanced** |

**What drives quality (correlation with the quality score):**

| Feature | Correlation | Reading |
| --- | --- | --- |
| Alcohol | **+0.48** | The strongest link: more alcohol, higher quality |
| Volatile acidity | **−0.40** | A vinegary taste lowers quality |
| Sulphates | +0.25 | A weak positive link |
| Citric acid | +0.23 | A weak positive link |
| Residual sugar | +0.01 | Almost no link |

## What I learnt

**An EDA checklist, in the order the lecture followed:**

```python
df = pd.read_csv("winequality-red.csv")

df.head()                     # 1. look at a few rows
df.info()                     # 2. column types and non-null counts
df.describe()                 # 3. mean, std, min, quartiles, max for each column
df.shape, df.columns          # 4. size and column names
df["quality"].unique()        # 5. what values does the target take? [5, 6, 7, 4, 8, 3]
df.isnull().sum()             # 6. missing values: none here
df[df.duplicated()]           # 7. duplicate rows: 240
df.drop_duplicates(inplace=True)
df.corr()                     # 8. how every pair of columns moves together
```

**Visual checks, from one variable to many:**

| Analysis | Chart | What it showed |
| --- | --- | --- |
| **Univariate** (one variable) | `df.quality.value_counts().plot(kind="bar")`, plus a `histplot` for each column | Quality is imbalanced; several features are right-skewed |
| **Bivariate** (two variables) | `sns.catplot(x="quality", y="alcohol", kind="box")` | Higher-quality wines tend to have more alcohol |
| **Multivariate** (several at once) | `sns.heatmap(df.corr(), annot=True)`, `sns.pairplot(df)`, a scatter of alcohol vs pH coloured by quality | How all the features relate at once |

**Relationships between features matter too,** not just with the target. Fixed acidity moves strongly with citric acid (+0.67) and density (+0.67), and against pH (−0.69). Free and total sulphur dioxide move together (+0.67). Features this closely linked carry overlapping information, which affects how a model should treat them.

## How this shows up in financial statement audit work

EDA is what I'd do first with any client extract: profile it, check its quality, then look for patterns and relationships before testing anything. These snippets apply the same checklist to a simulated journal entry extract.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(21)
n = 1_200
je = pd.DataFrame({
    "je_id": [f"JE{i:05d}" for i in range(n)],
    "preparer": rng.choice(["A. Rao", "M. Gomez", "J. Lee", "S. Patel"], n),
    "source": rng.choice(["Automated", "Manual"], n, p=[0.85, 0.15]),
    "amount": rng.lognormal(8.3, 1.0, n).round(2),
    "vendor": rng.choice([f"V{i:02d}" for i in range(40)], n),
})
dupes = je.sample(6, random_state=1).assign(je_id=lambda d: d["je_id"] + "-D")   # 6 re-keyed copies
je = pd.concat([je, dupes], ignore_index=True)
```

**1. The profiling checklist:**

```python
print(je.shape)                                   # (1206, 5)
print(je.isnull().sum().sum(), "missing values")  # 0 missing values
print(je["source"].value_counts(normalize=True).round(2).to_dict())   # {'Automated': 0.84, 'Manual': 0.16}: imbalanced, like wine quality
print(je["amount"].describe().round(0).to_dict())
```

**2. Duplicates: investigate them, never just drop them.** The lecture removed duplicate wines, which is fine for modelling. In audit, a duplicate can be a **duplicate payment**. Checking on the fields that matter, while ignoring the ID, catches entries re-keyed under a new number:

```python
key = ["vendor", "amount", "preparer"]
possible_dupes = je[je.duplicated(subset=key, keep=False)].sort_values(key)
print(len(possible_dupes), "entries in", possible_dupes.groupby(key).ngroups, "duplicate groups")
# 12 entries in 6 duplicate groups: every re-keyed copy found, each paired with its original
```

**3. Box plots by group, like quality vs alcohol.** Do some preparers post systematically larger manual entries?

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

manual = je[je["source"] == "Manual"]
g = sns.catplot(data=manual, x="preparer", y="amount", kind="box", height=4, aspect=1.6)
g.ax.set_yscale("log")
g.savefig("manual_amounts_by_preparer.png", dpi=120)
plt.close(g.figure)
print(manual.groupby("preparer")["amount"].median().round(0).to_dict())
# {'A. Rao': 5187.0, 'J. Lee': 4815.0, 'M. Gomez': 3238.0, 'S. Patel': 3862.0}: no preparer stands far apart
```

**4. Correlation between account balances: an analytical review.** As with the wine features, monthly balances that *should* move together, like revenue and receivables, can be checked with a correlation matrix and heatmap:

```python
months = 24
revenue = rng.normal(500_000, 60_000, months)
monthly = pd.DataFrame({
    "revenue": revenue,
    "cost_of_sales": revenue * 0.62 + rng.normal(0, 15_000, months),
    "receivables": revenue * 1.4 + rng.normal(0, 40_000, months),
    "payroll": rng.normal(120_000, 5_000, months),
})
print(monthly.corr().round(2)["revenue"].to_dict())
# {'revenue': 1.0, 'cost_of_sales': 0.91, 'receivables': 0.87, 'payroll': 0.28}
# cost of sales and receivables track revenue closely, while payroll barely does, as expected
```

If receivables stopped tracking revenue, that weaker correlation would be worth investigating: perhaps slower collections, or revenue recorded without real customers behind it.

## My reflection

The wine lecture was really a lesson in **asking questions before answering them**. Look at the shape, the gaps, the duplicates and the distributions first, and only then at relationships. That's the same order I follow when planning an audit: understand the population before choosing tests.

The one place I'd do things differently is duplicates. Dropping them is right for a wine-quality model, but in a ledger, a duplicate might be the most important row in the file. So my EDA habit for audit data is to **find them, list them and explain them**, never to delete them silently.
