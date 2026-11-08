<<<<<<< HEAD
# EDA Code Walkthrough: Red Wine Quality, Step by Step
=======
# Exploratory Data Analysis (EDA): Red Wine Quality: Notes
>>>>>>> b9614953454b5457cb6529089c41ffb10ba36a37

*Nov 7, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **EDA with Red Wine Data** lecture from **Krish Naik Academy**. This file explains every coding step in the lecture notebook. My [EDA lecture notes](feature-engineering-eda-wine-quality-notes.md) cover the findings and their audit meaning.

## Where I started

The first time through this lecture, I focused on *what the data showed*. This time I wanted to understand *what each line of code does and why it's there*, because the same 20 or so lines will be my starting point for every new dataset, client ledgers included.

The data: **1,599 red wines**, 11 chemical measurements each, plus a **quality score from 3 to 8**.

## The notebook, cell by cell

### Stage 1: Load and first look

| Code | What it does | Why it matters |
| --- | --- | --- |
| `import pandas as pd` | Loads pandas with its usual short name | Every later step uses `pd` |
| `df = pd.read_csv("winequality-red.csv")` | Reads the CSV file into a DataFrame (a table) | All analysis runs on `df` |
| `df.head()` | Shows the first 5 rows | A quick sense of the columns and values |

### Stage 2: Inspect the structure

| Code | What it does | What it showed here |
| --- | --- | --- |
| `df.info()` | Lists each column's type and non-null count | 12 numeric columns (11 `float64`, quality `int64`), with no gaps |
| `df.describe()` | Gives count, mean, std, min, quartiles and max for every numeric column | Alcohol from 8.4 to 14.9, quality from 3 to 8, mean quality 5.64 |
| `df.shape` | Returns (rows, columns) | `(1599, 12)` |
| `df.columns` | Lists the column names | `fixed acidity` … `alcohol`, `quality` |
| `df["quality"].unique()` | Lists each distinct value of the target | `[5, 6, 7, 4, 8, 3]` |

### Stage 3: Check and clean data quality

| Code | What it does | What it showed here |
| --- | --- | --- |
| `df.isnull().sum()` | Counts missing values per column | All zeros: no missing data |
| `df[df.duplicated()]` | Shows rows that exactly repeat an earlier row | **240** duplicate rows |
| `df.drop_duplicates(inplace=True)` | Removes those repeats, changing `df` itself (`inplace=True`) | Only the first copy of each row is kept |
| `df.shape` | Re-checks the size after cleaning | `(1359, 12)`: 1,599 − 240 |

`duplicated()` marks the **second and later** copies of a row as `True`, so `drop_duplicates()` keeps the first one.

### Stage 4: Relationships between variables

| Code | What it does | What it showed here |
| --- | --- | --- |
| `df.corr()` | Calculates the correlation (−1 to +1) between every pair of columns | Alcohol vs quality **+0.48**, volatile acidity vs quality **−0.40** |
| `plt.figure(figsize=(10, 6))` | Creates a 10×6-inch canvas for the next chart | Room for a 12×12 grid |
| `sns.heatmap(df.corr(), annot=True)` | Draws the correlation table as a coloured grid, with values printed in each cell (`annot=True`) | Strong pairs stand out at a glance |

### Stage 5: Visualise

| Code | Type | What it shows |
| --- | --- | --- |
| `df.quality.value_counts().plot(kind="bar")` with `plt.xlabel`, `plt.ylabel`, `plt.show()` | **Univariate** | Wines per quality score. Most are 5 or 6, so the data is **imbalanced** |
| `for column in df.columns: sns.histplot(df[column], kde=True)` | **Univariate** | Each column's distribution, with a smooth density curve (`kde=True`) |
| `sns.histplot(df["alcohol"])` | **Univariate** | Alcohol alone: right-skewed, clustered around 9.5–11% |
| `sns.pairplot(df)` | **Multivariate** | A scatter plot for **every** pair of columns, with histograms on the diagonal |
| `sns.catplot(x="quality", y="alcohol", data=df, kind="box")` | **Bivariate** | Alcohol's spread at each quality level; it rises with quality |
| `sns.scatterplot(x="alcohol", y="pH", hue="quality", data=df)` | **Multivariate** | Two features, with a third shown as colour (`hue`) |

**Three coding details worth knowing:**

- **The histogram loop draws every column onto one chart,** because no new figure is created inside the loop. To get one chart per column, add `plt.figure()` before each `sns.histplot(...)`, followed by `plt.show()`.
- **`df.corr()` works here because every column is numeric.** With text columns, recent pandas versions need `df.corr(numeric_only=True)`.
- **`sns.pairplot` gets slow with many columns,** because 12 columns means 144 small plots. Passing a few chosen columns, as in `vars=["alcohol", "volatile acidity", "quality"]`, keeps it quick.

## How this shows up in financial statement audit work

The same five stages work on any client extract. These snippets apply them to a simulated journal entry file. Unlike the wine notebook, nothing is deleted.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(8)
n = 800
gl = pd.DataFrame({
    "je_id": [f"JE{i:05d}" for i in range(n)],
    "account": rng.choice(["4000", "5000", "6100", "6300"], n),
    "amount": rng.lognormal(8, 1, n).round(2),
    "source": rng.choice(["Automated", "Manual"], n, p=[0.85, 0.15]),
    "approver": rng.choice(["K. Wong", "D. Smith", None], n, p=[0.48, 0.48, 0.04]),
})
gl = pd.concat([gl, gl.iloc[[10, 250]]], ignore_index=True)   # two exact repeats, as in the wine data
```

**1. Stages 1–3 as one reusable profile,** the audit version of `info()`, `isnull()` and `duplicated()`:

```python
def profile(df, key):
    return {
        "rows": len(df),
        "missing_by_column": df.isnull().sum()[lambda s: s > 0].to_dict(),
        "exact_duplicate_rows": int(df.duplicated().sum()),
        "duplicate_keys": int(df[key].duplicated().sum()),
    }

print(profile(gl, "je_id"))
# {'rows': 802, 'missing_by_column': {'approver': 29}, 'exact_duplicate_rows': 2, 'duplicate_keys': 2}
```

**2. Stage 3, the audit way: list the duplicates, don't drop them.** `keep=False` shows **every** copy, not just the repeats:

```python
print(gl[gl.duplicated(keep=False)][["je_id", "account", "amount"]].to_string(index=False))
# JE00010 and JE00250 each appear twice: the same journal entry recorded twice
```

**3. Stage 4 on the ledger: totals by account.** This is what `describe()` and `corr()` become for a ledger:

```python
print(gl.groupby("account")["amount"].agg(["count", "sum", "median"]).round(0).to_string())
```

**4. Stage 5: the imbalance check,** the ledger version of the quality bar chart:

```python
print(gl["source"].value_counts().to_dict())                                # {'Automated': 680, 'Manual': 122}
print(gl.loc[gl["approver"].isnull(), "source"].value_counts().to_dict())   # {'Automated': 27, 'Manual': 2}
# 2 manual entries have no approver: those are the ones to follow up
```

## My reflection

Going through the notebook line by line showed me how much ground about 20 short commands cover: structure, quality, relationships and pictures, in that order. The order matters as much as the commands. Checking duplicates *before* calculating correlations is the same discipline as confirming the population is complete before testing it.

The coding details were useful too. The histogram loop that quietly overlays every chart and the `corr()` call that needs `numeric_only=True` on mixed data are exactly the kind of small surprises that would cost me time on a real engagement.
