# EDA and Feature Engineering: Flight Price Data: My Notes

*Nov 8, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **EDA and Feature Engineering: Flight Price Prediction** lecture from **Krish Naik Academy**. The dataset comes from [Kaggle](https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction). I re-ran the notebook's steps on the lecture's `flight_price.xlsx` to check every figure below.

## Where I started

The wine lecture was mostly *exploring* clean, numeric data. This one was messier and more realistic: almost every column arrived as **text**, such as dates like `24/03/2019`, times like `01:10 22 Mar`, durations like `2h 50m` and stops like `1 stop`. The lecture showed how to **engineer** those strings into numbers a model can use. That's exactly the kind of work journal entry extracts need before any analysis.

## The data in brief

**10,683 flights** on Indian domestic routes, with 11 columns. Only **Price** is numeric; everything else is text.

| Column | Example | What it holds |
| --- | --- | --- |
| Airline | `IndiGo` | 12 airlines |
| Date_of_Journey | `24/03/2019` | Day/month/year as text |
| Source, Destination | `Banglore` → `New Delhi` | 5 departure and 6 arrival cities |
| Route | `BLR → DEL` | The stops along the way |
| Dep_Time, Arrival_Time | `22:20`, `01:10 22 Mar` | Times, sometimes with a date attached |
| Duration | `2h 50m` | Flight length as text |
| Total_Stops | `non-stop`, `1 stop` | The number of stops, as words |
| Additional_Info | `No info` | Extra notes |
| Price | `3897` | ₹1,759 to ₹79,512, with a median of ₹8,372 |

Only **one row** (row 9039) had missing values, in both `Route` and `Total_Stops`.

## The notebook, step by step

### 1. Load and inspect

| Code | What it does |
| --- | --- |
| `import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns` | Loads the usual libraries. `%matplotlib inline` shows charts inside the notebook. |
| `df = pd.read_excel("flight_price.xlsx")` | Reads an **Excel** file, not a CSV this time |
| `df.head()`, `df.tail()` | Shows the first and last 5 rows |
| `df.info()` | Shows 11 columns, 10 of them text: a sign that feature engineering is needed |
| `df.describe()` | Summarises only `Price`, because it's the only numeric column |

### 2. Split the journey date into day, month and year

```python
df["Date"] = df["Date_of_Journey"].str.split("/").str[0]     # "24/03/2019" -> "24"
df["Month"] = df["Date_of_Journey"].str.split("/").str[1]    # -> "03"
df["Year"] = df["Date_of_Journey"].str.split("/").str[2]     # -> "2019"
df["Date"] = df["Date"].astype(int)                          # text -> number (same for Month, Year)
df.drop("Date_of_Journey", axis=1, inplace=True)             # remove the original column
```

`.str.split("/")` breaks each string into a list, and `.str[0]` picks an item from every row's list at once. `astype(int)` turns the text pieces into numbers. `axis=1` means "drop a **column**", not a row.

### 3. Split arrival and departure times into hours and minutes

```python
df["Arrival_Time"] = df["Arrival_Time"].apply(lambda x: x.split(" ")[0])   # "01:10 22 Mar" -> "01:10"
df["Arrival_hour"] = df["Arrival_Time"].str.split(":").str[0].astype(int)  # -> 1
df["Arrival_min"] = df["Arrival_Time"].str.split(":").str[1].astype(int)   # -> 10
# the same pattern turns Dep_Time into Departure_hour and Departure_min; both originals are then dropped
```

`apply()` with a `lambda` runs a small function on every value. Here it keeps only the time and discards the date some arrivals carry.

### 4. Turn stops into numbers and fill the one gap

```python
df["Total_Stops"].unique()   # ['non-stop', '2 stops', '1 stop', '3 stops', nan, '4 stops']
df["Total_Stops"].mode()     # '1 stop': the most common value
df["Total_Stops"] = df["Total_Stops"].map(
    {"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4, np.nan: 1})
df.drop("Route", axis=1, inplace=True)    # Route repeats what Total_Stops now captures
```

`map()` with a dictionary is a hand-written **ordinal encoding**, since stops have a natural order. Mapping `np.nan` to `1` fills the single missing value with the **mode**, in the same step. The result: 5,626 one-stop, 3,491 non-stop, 1,520 two-stop, 45 three-stop and 1 four-stop flight.

### 5. Start on Duration

```python
df["Duration"].str.split(" ").str[0].str.split("h").str[0]   # "2h 50m" -> "2"
```

This extracts the hours from text like `2h 50m`. In the notebook, the result is displayed but not yet saved into a column.

### 6. Check categories, then one-hot encode them

```python
df["Airline"].unique()            # 12 airlines
df["Source"].unique()             # 5 cities
df["Additional_Info"].unique()    # 10 different notes

from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
encoded = encoder.fit_transform(df[["Airline", "Source", "Destination"]]).toarray()
pd.DataFrame(encoded, columns=encoder.get_feature_names_out())    # 23 new 0/1 columns
```

Airline, source and destination have **no order**, so they get **one-hot encoding**: 12 + 5 + 6 = **23** columns, each named like `Airline_IndiGo`.

## Things I noticed when re-running it

Checking the data myself turned up a few points worth knowing before taking these steps further:

| Observation | Why it matters |
| --- | --- |
| **Year is always 2019**, and months run only from March to June | A column with one value tells a model nothing, so it can be dropped |
| **Arrival times with a date attached** (`01:10 22 Mar`) are overnight or next-day arrivals | Keeping only the time throws that information away. A "next day" flag would keep it |
| **Durations aren't all `Xh Ym`**: some are only hours (`19h`), and one is only minutes (`5m`) | Splitting on `h` turns `5m` into the text `"5m"`, which fails when converted to a number |
| **Labels aren't consistent**: `No info` (8,345 rows) vs `No Info` (3), and `Delhi` vs `New Delhi` as destinations | The same thing counted twice under different names, unless the labels are standardised |
| **220 rows are exact duplicates** | Worth checking, as in the wine lecture |

## How this shows up in my audit work with journal entry data

Journal entry extracts look a lot like this flight file: dates as text, times in their own columns, statuses as words and inconsistent labels. These snippets apply the lecture's techniques to a small sample extract.

```python
import numpy as np
import pandas as pd

je = pd.DataFrame({
    "je_id": ["JE01", "JE02", "JE03", "JE04", "JE05"],
    "posting_date": ["31/12/2026", "02/01/2027", "28/12/2026", "31/12/2026", "15/11/2026"],
    "posting_time": ["23:40", "09:15", "14:05", "18:30", "11:00"],
    "approval_lag": ["2d 5h", "45m", "1d", "6h 30m", None],
    "approval_level": ["Level 2", "Level 1", "Level 3", "Level 1", "Level 2"],
    "source": ["Manual", "manual", "Automated", "MANUAL ", "Automated"],
    "company_code": ["UK01"] * 5,
    "amount": [250_000, 4_200, 18_000, 98_000, 7_500],
})
```

**1. Dates and times into audit features (steps 2 and 3).** Instead of splitting strings by hand, `pd.to_datetime` with `dayfirst=True` reads `31/12/2026` correctly and unlocks weekday, month-end and after-hours flags:

```python
dt = pd.to_datetime(je["posting_date"] + " " + je["posting_time"], format="%d/%m/%Y %H:%M")
je["month"] = dt.dt.month
je["weekday"] = dt.dt.day_name()
je["posted_hour"] = dt.dt.hour
je["after_hours"] = je["posted_hour"].ge(20) | je["posted_hour"].lt(7)
je["period_end"] = dt.dt.is_month_end
je["after_year_end"] = dt > pd.Timestamp("2026-12-31 23:59")      # posted in the next period
print(je[["je_id", "weekday", "posted_hour", "after_hours", "period_end", "after_year_end"]].to_string(index=False))
# JE01: Thursday 23:40 on 31 Dec, both after hours and period end | JE02: posted in the next period
```

**2. Parsing durations safely (step 5).** Approval lag arrives as text like `2d 5h` or `45m`, the same problem as `Duration`. A regular expression handles any combination, including the minutes-only case that broke the simple split:

```python
parts = je["approval_lag"].str.extract(r"(?:(\d+)d)?\s*(?:(\d+)h)?\s*(?:(\d+)m)?").astype(float).fillna(0)
je["lag_hours"] = (parts[0] * 24 + parts[1] + parts[2] / 60).where(je["approval_lag"].notna())
print(je[["je_id", "approval_lag", "lag_hours"]].to_string(index=False))
# 2d 5h -> 53.0, 45m -> 0.75, 1d -> 24.0, 6h 30m -> 6.5, and None stays missing
```

**3. Ordered labels into numbers, with the gap flagged rather than filled (step 4).** The lecture filled one missing stop count with the mode. For audit data, a missing approval is a finding, so it's kept visible:

```python
level_map = {"Level 1": 1, "Level 2": 2, "Level 3": 3}
je["approval_level_num"] = je["approval_level"].map(level_map)
je["lag_missing"] = je["lag_hours"].isna()                         # flag it, don't impute it
print(je.loc[je["lag_missing"], "je_id"].tolist())                 # ['JE05']: no approval record
```

**4. Standardise labels and drop constant columns** (the `No info` / `No Info` and `Year` points):

```python
print(je["source"].unique().tolist())          # ['Manual', 'manual', 'Automated', 'MANUAL ']: one label, three spellings
je["source"] = je["source"].str.strip().str.title()
print(je["source"].value_counts().to_dict())   # {'Manual': 3, 'Automated': 2}

constant = [c for c in je.columns if je[c].nunique(dropna=False) == 1]
print(constant)                                 # ['company_code']: a single company, so no information for a model
```

Grouping on the raw `source` column would have reported three different "manual" categories, which would understate manual entries in every summary.

## My reflection

This lecture felt much closer to real work than the tidy wine data. Almost nothing arrived ready to use. Dates, times, durations and statuses all needed turning into numbers first, and the code for each was short once I understood `.str.split()`, `.str[n]`, `astype()`, `map()` and `apply()`.

Re-running the notebook myself also taught me something. The `5m` duration and the `No info` / `No Info` labels were small details that would have quietly broken or skewed a model. Client ledgers have exactly these quirks: a posting date in two formats, a source system spelt three ways, an approval timestamp missing. So my rule is to **profile every text column before converting it**, and to **flag gaps rather than fill them** whenever the gap itself could be the finding.
