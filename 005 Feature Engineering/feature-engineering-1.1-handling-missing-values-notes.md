# Handling Missing Values: Notes

*Nov 2, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Handling Missing Values** lecture notebook from my data science course. The examples use the Titanic dataset that ships with the **seaborn** library.

## Where I started

I first met missing values in the pandas lectures, through `fillna()` and `dropna()`. This lecture went a step further and asked **why** the data is missing in the first place. The answer decides which fix is safe. It's a question auditors ask instinctively: a gap isn't just a gap; it might be telling you something.

## The data in brief

The **Titanic** passenger dataset: **891 passengers** and 15 columns (age, class, fare, port of embarkation, deck, survival and so on). Four columns have gaps:

| Column | Missing | Share |
| --- | --- | --- |
| `deck` | 688 | 77.2% |
| `age` | 177 | 19.9% |
| `embarked` | 2 | 0.2% |
| `embark_town` | 2 | 0.2% |

## What I learnt

### Three reasons data goes missing

| Mechanism | Meaning | Example |
| --- | --- | --- |
| **MCAR**: missing completely at random | The gap has nothing to do with any value, seen or unseen | Survey answers lost at random |
| **MAR**: missing at random | The gap depends on *other* columns you can see | Some groups, such as by age or job, report income less often |
| **MNAR**: missing not at random | The gap depends on the *missing value itself* | Unhappy employees are more likely to hide their income |

MNAR is the dangerous one. The missing values are systematically different, so any fill or deletion biases the result.

### Option 1: delete

```python
df.dropna().shape          # (182, 15): keeps only complete rows
df.dropna(axis=1).shape    # (891, 11): drops every column with a gap
```

Dropping rows removed **80% of passengers**, mostly because of `deck`. Dropping columns removed `age`, which matters for the analysis. Deletion is simple, but it can throw away most of the data.

### Option 2: impute (fill in an estimate)

| Method | Code | Filled value | Best for |
| --- | --- | --- | --- |
| **Mean** | `df["age"].fillna(df["age"].mean())` | 29.70 | Numbers with a roughly normal spread |
| **Median** | `df["age"].fillna(df["age"].median())` | 28.0 | Numbers with outliers or skew |
| **Mode** | `df["embarked"].fillna(mode_value)` | `"S"` (Southampton) | Categories |

The lecture plotted `age` with a histogram (`sns.histplot(..., kde=True)`) first, to see its shape before choosing between the mean and the median. The mode was taken from the non-missing values only: `df[df["embarked"].notna()]["embarked"].mode()[0]`.

**A good habit from the lecture:** each fill went into a **new column** (`Age_mean`, `age_median`, `embarked_mode`), so the original `age` and `embarked` stayed untouched for comparison.

## How this shows up in financial statement audit work

In audit, the question "why is this missing?" often matters more than the fix. Missing approvals, descriptions or dates can be control failures, so they're profiled and investigated before anything is filled. These snippets use a small sample journal entry extract built in the code.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
n = 400
je = pd.DataFrame({
    "je_id": [f"JE{i:04d}" for i in range(n)],
    "amount": rng.lognormal(8.5, 1.1, n).round(2),
    "source": rng.choice(["Automated", "Manual"], n, p=[0.8, 0.2]),
    "description": rng.choice(["Accrual", "Reclass", "Payment", None], n, p=[0.3, 0.3, 0.35, 0.05]),
    "days_to_approve": rng.gamma(2, 1.5, n).round(0),
})
je["approver"] = np.where(je["source"] == "Automated", "SYSTEM", rng.choice(["K. Wong", "D. Smith"], n))
large_manual = (je["source"] == "Manual") & (je["amount"] > je["amount"].quantile(0.75))
je.loc[large_manual & (rng.random(n) < 0.6), "approver"] = None        # approvals missing mostly on big manual entries
je.loc[rng.random(n) < 0.1, "days_to_approve"] = np.nan
```

**1. Profile the gaps first, as the lecture did with `isnull().sum()`:**

```python
missing = pd.DataFrame({"missing": je.isnull().sum(), "share_%": (je.isnull().mean() * 100).round(1)})
print(missing[missing["missing"] > 0])
# description 13 (3.2%) | days_to_approve 38 (9.5%) | approver 8 (2.0%)
```

**2. Test the mechanism: are missing approvals random?** Compare entries *with* and *without* an approver. If the missing ones are systematically larger, the gap isn't random. It looks like **MNAR**, and it's a control finding:

```python
has_approver = je["approver"].notna()
print(je.groupby(has_approver)["amount"].median().round(0).rename({True: "approved", False: "no approver"}))
# no approver 17,070 vs approved 5,344: unapproved entries are about 3x larger
print(je.loc[~has_approver, "source"].value_counts().to_dict())   # {'Manual': 8}: every missing approval is on a manual entry
```

**3. Never delete rows from a test population.** Dropping every row with any gap shrinks the population, and the dropped rows are exactly the ones most worth testing:

```python
print(len(je), len(je.dropna()))                                   # 400 342: a blind dropna() discards 58 entries
untested = je[je.isnull().any(axis=1)]
print(untested["approver"].isnull().sum(), "of the discarded rows are entries with no approver")   # 8: all of them
```

**4. Impute only for analytics, in a new, flagged column.** Filling `days_to_approve` with the median is fine for a trend chart, but the original stays, and a flag records which values are estimates. Amounts and approvals are **never** imputed for testing:

```python
print(round(je["days_to_approve"].skew(), 2))                     # 1.41: right-skewed, so use the median, not the mean
je["days_to_approve_filled"] = je["days_to_approve"].fillna(je["days_to_approve"].median())
je["days_imputed"] = je["days_to_approve"].isnull()
je["description_filled"] = je["description"].fillna("MISSING")    # a visible label, not the mode
print(je["days_imputed"].sum(), je["description_filled"].eq("MISSING").sum())   # 38 13: every estimate is flagged
```

For descriptions I used a visible `"MISSING"` label rather than the mode. Filling a blank with the most common description, such as "Payment", would make an unexplained entry look explained.

## My reflection

The three mechanisms gave me words for something I already knew from audit work. A missing value is either noise (MCAR), explained by something I can see (MAR), or hiding something (MNAR). Missing approvals that cluster on large manual entries aren't a data cleaning problem. They're a finding.

The lecture's techniques (mean, median and mode imputation) are the right tools for **modelling and analytics**, where a complete dataset matters. For **testing**, my rule is the opposite: profile the gaps, ask why they exist, report them, and never fill or drop a row I'm meant to be testing.
