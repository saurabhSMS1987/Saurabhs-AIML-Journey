# pandas Cheat Sheet: Power & Utilities Examples

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Commands are based on the ***pandas Cheat Sheet*** by **Dataquest** ([dataquest.io/guide](https://www.dataquest.io/guide)). The Power & Utilities examples are my own, built on small sample data so every snippet runs as written.

The cheat sheet uses a Fortune 500 dataset. I've redone each section with data from a power utility (meter readings, bills, customers and outages), which is closer to the work I review.

## Sample data used throughout

```python
import pandas as pd
import numpy as np

readings = pd.DataFrame({
    "meter_id":     ["M001", "M002", "M003", "M004", "M005", "M006", "M007", "M008"],
    "customer_id":  ["C101", "C102", "C103", "C104", "C105", "C106", "C107", "C108"],
    "region":       ["North", "North", "South", "South", "East", "East", "West", "West"],
    "tariff":       ["Residential", "Commercial", "Residential", "Industrial",
                     "Residential", "Commercial", "Residential", "Industrial"],
    "reading_date": ["2026-09-30"] * 8,
    "kwh":          [420, 3150, np.nan, 18200, 0, 2875, 395, 21400],
    "bill_amount":  ["58.80", "441.00", "61.20", "2184.00", "0.00", "402.50", "55.30", "2568.00"],
})
```

Two problems are built in on purpose: meter M003 has a **missing reading**, and `bill_amount` arrived as **text**. Both are common in real billing extracts.

## 1. Importing data

| Command | Use |
| --- | --- |
| `pd.read_csv(file)` | Meter or billing extracts |
| `pd.read_excel(file)` | Tariff schedules, reconciliations |
| `pd.read_sql(query, conn)` | Customer information system (CIS) tables |
| `pd.read_json(...)` | Smart-meter API feeds |
| `pd.DataFrame(dict)` | Small test tables, like the one above |

```python
readings.to_csv("meter_readings_sep.csv", index=False)       # create a file to read back
df = pd.read_csv("meter_readings_sep.csv")
print(df.shape)                                              # (8, 7): 8 meters, 7 columns
```

## 2. Exporting data

```python
exceptions = df[df["kwh"] == 0]
exceptions.to_csv("zero_consumption_exceptions.csv", index=False)
exceptions.to_excel("zero_consumption_exceptions.xlsx", index=False)   # needs openpyxl
```

`to_sql`, `to_json` and `to_html` work the same way, so results can go straight to a database, an API or a report.

## 3. View and inspect

```python
df.head(3)                            # first 3 meters
df.tail(2)                            # last 2 meters
df.info()                             # columns, types and non-null counts: kwh has 7 of 8
df["tariff"].value_counts()           # Residential 4, Commercial 2, Industrial 2
df["kwh"].describe()                  # count, mean, min, max and quartiles of consumption
```

`df.info()` is the first thing I run on a new extract. It shows missing values and wrong types, such as `bill_amount` stored as text, before any analysis starts.

## 4. Selecting data

```python
df["kwh"]                                   # one column
df[["meter_id", "kwh"]]                     # several columns

df = df.set_index("meter_id")
df.loc["M004", "kwh"]                       # 18200.0: select by label
df.loc[["M002", "M006"], ["tariff", "kwh"]] # commercial meters only
df.iloc[0]                                  # first row, by position
df.iloc[2, 4]                               # third meter's kwh: nan (the missing reading)
```

`loc` selects by **name** (meter ID), and `iloc` selects by **position**. Label slices with `loc` include both ends, so `df.loc["M001":"M003"]` returns three meters.

## 5. Boolean filtering

```python
# industrial meters using more than 20,000 kWh
heavy = df[(df["tariff"] == "Industrial") & (df["kwh"] > 20000)]
print(heavy.index.tolist())                 # ['M008']

# zero readings: possible stopped meter, bypass or vacant premises
zero_use = df[df["kwh"] == 0]
print(zero_use.index.tolist())              # ['M005']

# missing readings: estimated bills need support
no_read = df[df["kwh"].isnull()]
print(no_read.index.tolist())               # ['M003']
```

Use `&` for "and", `|` for "or" and `~` for "not", and put each condition in brackets.

## 6. Data cleaning

```python
df["bill_amount"] = df["bill_amount"].astype(float)          # text to numbers
df["reading_date"] = pd.to_datetime(df["reading_date"])      # text to dates

df = df.rename(columns={"kwh": "kwh_used"})                  # clearer column name
df["tariff"] = df["tariff"].replace({"Residential": "RES",
                                     "Commercial": "COM",
                                     "Industrial": "IND"})   # shorter codes

flagged = df[df["kwh_used"].isnull()]                         # record the gap before filling it
df["kwh_used"] = df["kwh_used"].fillna(df["kwh_used"].median())
print(df.loc["M003", "kwh_used"])                            # 2875.0: median used as an estimate
```

`dropna()` removes rows with missing values, and `fillna()` replaces them. In audit, I record the missing rows *before* filling them, because the gap may be a finding in itself.

## 7. Sort, group and pivot

```python
df.sort_values("kwh_used", ascending=False).head(3)           # top 3 consumers

df.groupby("region")["bill_amount"].sum()
# East 402.5 | North 499.8 | South 2245.2 | West 2623.3

df.pivot_table(index="region", columns="tariff",
               values="kwh_used", aggfunc="sum", fill_value=0)

# effective rate per kWh, row by row
df["rate_per_kwh"] = df.apply(
    lambda row: row["bill_amount"] / row["kwh_used"] if row["kwh_used"] > 0 else np.nan,
    axis=1)
print(df["rate_per_kwh"].round(3).tolist())
# [0.14, 0.14, 0.021, 0.12, nan, 0.14, 0.14, 0.12]
```

The rate check stands out. M003 works out at about $0.02 per kWh because its bill ($61.20) doesn't fit the median reading used to fill the gap. That's a sign the estimate needs checking.

## 8. Join and combine

```python
# stack August and September readings (same columns)
aug = pd.DataFrame({"meter_id": ["M001", "M002"], "kwh": [410, 3020]})
sep = pd.DataFrame({"meter_id": ["M001", "M002"], "kwh": [420, 3150]})
both_months = pd.concat([aug, sep], ignore_index=True)       # 4 rows

# match bills to customer status, joining by key rather than position
customers = pd.DataFrame({
    "customer_id": ["C101", "C102", "C103", "C104", "C105", "C106", "C107", "C108"],
    "status": ["Active", "Active", "Active", "Active", "Closed", "Active", "Closed", "Active"],
})
billed = df.reset_index().merge(customers, on="customer_id", how="left")
print(billed[billed["status"] == "Closed"][["meter_id", "bill_amount"]])
# M005 0.00 and M007 55.30: M007 is still being billed on a closed account
```

Unlike NumPy's `hstack`, `merge` and `join` match rows **by key** (`customer_id`), so the row order doesn't matter.

## 9. Statistics

```python
df["bill_amount"].sum()             # 5770.8: total billed
df["kwh_used"].mean()               # average consumption
df["kwh_used"].median()
df["kwh_used"].std()
df.count()                          # non-null values in each column

# does demand follow temperature?
monthly = pd.DataFrame({
    "avg_temp_c": [12, 18, 24, 31, 29, 21],
    "system_mwh": [910, 860, 990, 1240, 1180, 950],
})
print(round(monthly["avg_temp_c"].corr(monthly["system_mwh"]), 2))   # 0.89: strong cooling load
```

A month that breaks a strong pattern like this is worth a closer look during analytical review.

## 10. Quick charts

```python
import matplotlib.pyplot as plt

df.groupby("region")["kwh_used"].sum().plot.bar(title="kWh by region")
plt.show()

monthly.plot.scatter(x="avg_temp_c", y="system_mwh", title="Temperature vs demand")
plt.show()
```

`plot.hist()`, `plot.barh()` and `plot.line()` follow the same pattern.

## Corrections to the cheat sheet

I tested the commands against pandas 3.0 and found a few that are out of date or worded loosely:

| Cheat sheet | Correct form | Why |
| --- | --- | --- |
| `df1.append(df2)` | `pd.concat([df1, df2])` | `append` was removed in pandas 2.0 |
| `df.shape()` | `df.shape` | `shape` is an attribute, not a method |
| `f500.to_datetime(...)` | `pd.to_datetime(...)` | `to_datetime` belongs to `pd`, not the DataFrame |
| `agg(np.mean)` | `agg("mean")` | Passing NumPy functions is deprecated |
| `dropna(axis=1, thresh=n)` "drops rows" | Drops **columns** | `axis=1` means columns |
| `pd.concat([df1, df2], axis=1)` "adds df1 to df2" | Adds **df2's** columns after df1's | The order is the other way round |

## What stuck with me

pandas feels like NumPy with labels. Columns have names, rows have IDs, and joins match records by key instead of by position. That fixes the `hstack` worry from the NumPy lectures. The closed-account example shows how much a single `merge` can uncover: a bill is still going out on an account that should have stopped billing.
