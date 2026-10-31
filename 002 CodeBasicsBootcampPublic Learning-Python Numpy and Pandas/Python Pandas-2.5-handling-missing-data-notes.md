# Handling Missing Data in pandas: Notes

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Handling Missing Data – fillna, interpolate, dropna** lecture from the **CodeBasics Python course**.

## Where I started

Earlier lectures kept warning me that pandas silently skips missing values. This lecture finally showed what to *do* about them: fill them with a fixed value or an average, carry the previous value forward, estimate them from their neighbours, or drop the rows. Each method gave a different answer from the same data, and that was the real lesson for audit work.

## The data in brief

A small `weather_data.csv` with **9 days** of weather between 1 and 11 January 2017 (2 and 3 January are absent altogether). It has 3 columns: `temperature`, `windspeed` and `event`, with `day` read as real dates using `parse_dates` and set as the index.

- `temperature` is missing on **4 of 9** days, `windspeed` on **4**, and `event` on **2**.
- **9 January** is completely empty, and only **3 days** are complete.

## What I learnt

**`fillna`: fill gaps with a value.**

```python
df.fillna(0)                                    # every gap becomes 0, even in the text column
df.fillna({"temperature": df.temperature.mean(),   # a different rule per column
           "windspeed": df.windspeed.mean(),
           "event": "No Event"})
```

Filling temperature with `0` is clearly wrong, because it turns "unknown" into "freezing". The per-column dictionary is the sensible version.

**Carry values forward or backward:**

```python
df.ffill()             # copy the previous day's value down
df.bfill()             # copy the next day's value up
df.ffill(limit=1)      # fill at most one gap in a row, and leave longer gaps empty
```

> [!IMPORTANT]
> The lecture uses `df.fillna(method="ffill")`. That option was deprecated in pandas 2.1 and **removed in pandas 3.0**, where it now raises a `TypeError`. Use `df.ffill()` and `df.bfill()` instead.

The lecture also filled **across columns** with `axis="columns"`. That copied text like `'Snow'` into the windspeed column, which is a good example of an option that runs but makes no sense for this data.

**`interpolate`: estimate from the neighbours.** A missing value between 28 and 32 becomes 30, and between 32 and 34 the gaps fill in evenly as 32.67 and 33.33. It only works on numbers, so text columns stay empty.

**`dropna`: remove rows.**

| Code | Keeps | Rows left (of 9) |
| --- | --- | --- |
| `df.dropna()` | Only complete rows | 3 |
| `df.dropna(how="all")` | Rows with at least one value | 8 (drops 9 January) |
| `df.dropna(thresh=2)` | Rows with at least 2 values | 6 |

**Same gaps, different answers.** The temperature on 4 January came out as 0 (`fillna(0)`), 33.2 (the mean), 32 (`ffill`), 28 (`bfill`) or 30 (`interpolate`). None of these is the real figure; each is an assumption.

## How this shows up in healthcare audit work

These snippets use a small sample of claims and daily bed occupancy, built in the code so they run without any file.

```python
import pandas as pd
import numpy as np

claims = pd.DataFrame({
    "claim_id":         ["CL1", "CL2", "CL3", "CL4", "CL5", "CL6"],
    "diagnosis_code":   ["E11.9", None, "I10", "J18.9", None, None],
    "billed":           [1450.0, 22800.5, np.nan, 640.0, 9200.0, np.nan],
    "stay_days":        [2, 9, 3, np.nan, 4, np.nan],
    "discharge_status": ["Home", "Home", None, "Transferred", "Home", None],
})
```

**1. Measure the gaps before fixing anything.** Missing data is often a finding in itself.

```python
missing = claims.isnull().sum()
print((missing / len(claims) * 100).round(0).to_dict())
# {'claim_id': 0.0, 'diagnosis_code': 50.0, 'billed': 33.0, 'stay_days': 33.0, 'discharge_status': 33.0}

print(claims[claims["diagnosis_code"].isnull()]["claim_id"].tolist())
# ['CL2', 'CL5', 'CL6']: claims billed without a diagnosis code, a coding control weakness
```

**2. Drop only what can't be tested, and log it.** A claim with no billed amount can't be tested for value, but it should still be reported.

```python
untestable = claims[claims["billed"].isnull()]
testable = claims.dropna(subset=["billed"])         # drop rows missing *this* column only
print(untestable["claim_id"].tolist(), len(testable))   # ['CL3', 'CL6'] 4

print(len(claims.dropna(thresh=4)))                 # 4: claims with at least 4 of 5 fields populated
```

`subset=` is more useful in audit than a plain `dropna()`, which would remove any claim with *any* gap, here 5 of 6.

**3. Fill sensibly, and flag every fill.** Filled values are estimates, so they must stay visibly separate from real data.

```python
claims["status_filled"] = claims["discharge_status"].isnull()
claims = claims.fillna({"discharge_status": "Unknown", "diagnosis_code": "MISSING"})
print(claims[["claim_id", "discharge_status", "status_filled"]].tail(3).to_string(index=False))
# CL4 Transferred False | CL5 Home False | CL6 Unknown True
```

I'd never fill `billed` with an average in an audit. That would invent money. A flagged text label like `"Unknown"` is honest about what it is.

**4. Daily bed occupancy: carry forward vs interpolate.** The census report was missed for two days:

```python
census = pd.Series([180, np.nan, np.nan, 192, 195],
                   index=pd.date_range("2026-09-01", periods=5), name="beds_occupied")

print(census.ffill().tolist())          # [180.0, 180.0, 180.0, 192.0, 195.0]: assumes nothing changed
print(census.interpolate().tolist())    # [180.0, 184.0, 188.0, 192.0, 195.0]: assumes a steady rise
print(census.ffill(limit=1).tolist())   # [180.0, 180.0, nan, 192.0, 195.0]: fill one day at most
```

If billing for bed-days depends on the census, each method gives a different revenue figure, so the method used should be documented and reviewed.

## My reflection

The "same gap, five answers" moment is what I'll remember. Filling missing data isn't neutral. Every method builds an assumption into the numbers, and in an audit, an assumption hidden inside the data is worse than an honest gap. My rule from now on: measure the gaps first, log the rows I drop, flag the values I fill, and never fill an amount with an average.

The lecture code also reminded me that pandas keeps changing. `fillna(method="ffill")` now raises an error, so I'll check the version whenever older examples fail.
