# pandas DataFrame Basics: Notes

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **DataFrame Basics** lecture from the **CodeBasics Python course**.

## Where I started

Last lecture showed *why* pandas is worth learning. This one covered the everyday moves: checking a table's size, looking at rows, picking columns, filtering, summarising and setting an index for quick lookups. The lecture called one step "kinda doing SQL in pandas", and that's exactly how it felt, a bit like running queries on a spreadsheet.

## The data in brief

A tiny `weather_data.csv` file: **6 days** of weather (1–6 January 2017) with 4 columns: `day`, `temperature`, `windspeed` and `event` (Rain, Sunny or Snow).

- Temperatures range from **24 to 35**, with an average of **30.3**. The hottest day was 2 January.
- The events are Rain ×2, Sunny ×2 and Snow ×2.
- The `day` column is stored as **text** (`'1/2/2017'`), not as dates.

## What I learnt

A **DataFrame** is a table. A single column of it is a **Series** (`type(df['day'])` returns `Series`).

**Rows and columns:**

| Code | What it gives |
| --- | --- |
| `df.shape` | `(6, 4)`: rows and columns |
| `df.head()` / `df.tail(2)` | The first 5 rows, or the last 2 |
| `df[1:3]` | Rows 1 and 2, sliced like a list |
| `df.columns` | The column names |
| `df['day']` or `df.day` | One column, as a Series |
| `df[['day', 'temperature']]` | Several columns (note the double brackets) |

**Operations:**

```python
df['temperature'].max()                                    # 35
df[df['temperature'] > 32]                                 # rows that meet a condition
df[df['temperature'] == df['temperature'].max()]           # the whole row for the hottest day
df['temperature'].std()                                    # 3.83
df.describe()                                              # count, mean, std, min, quartiles, max
```

**`max()` on text** returned `'Sunny'`. That's only because "S" comes last in the alphabet, not because sunny was the most common event. `mean()` won't work on text at all.

**Index and `loc`:**

```python
df.set_index('day', inplace=True)    # 'day' becomes the row labels
df.loc['1/2/2017']                   # look a row up by its label
df.reset_index(inplace=True)         # put 'day' back as a normal column

df.set_index('event', inplace=True)
df.loc['Snow']                       # returns BOTH snow days: index labels don't have to be unique
```

The lecture compared an index to a **hash map**: a fast lookup by key. Unlike a database key, though, a pandas index allows duplicates.

`inplace=True` changes the DataFrame directly. The style most guides now recommend is `df = df.set_index('day')`, which does the same thing more visibly.

## How this shows up in healthcare audit work

These snippets use a small sample of hospital claims, built in the code so they run without any file.

```python
import pandas as pd

claims = pd.DataFrame({
    "claim_id":   ["CL1", "CL2", "CL3", "CL4", "CL5", "CL6"],
    "patient_id": ["P-778", "P-312", "P-778", "P-455", "P-901", "P-778"],
    "provider":   ["City Hospital", "Lakeside Clinic", "City Hospital",
                   "North Medical", "Lakeside Clinic", "Westside Surgery"],
    "billed":     [1450.0, 22800.5, 1450.0, 640.0, 9200.0, 3100.0],
    "stay_days":  [2, 9, 2, 1, 4, 1],
})
```

**1. First look at a new extract.**

```python
print(claims.shape)                    # (6, 5)
print(claims[["billed", "stay_days"]].describe().round(1))
# billed: mean 6440.1, max 22800.5 | stay_days: mean 3.2, max 9
```

`describe()` is a one-line analytical review. A maximum far above the 75th percentile, like 22,800.5 here, points straight to the item to look at first.

**2. Pulling out the claims to test.**

```python
high_value = claims[claims["billed"] > 5000]
print(high_value["claim_id"].tolist())                   # ['CL2', 'CL5']

top_claim = claims[claims["billed"] == claims["billed"].max()]
print(top_claim[["claim_id", "provider", "billed"]])     # CL2, Lakeside Clinic, 22800.5
```

**3. Looking up every claim for one patient with an index.** Because index labels don't have to be unique, one lookup returns all of a patient's claims, and that makes possible duplicate bills easy to spot.

```python
by_patient = claims.set_index("patient_id")
print(by_patient.loc["P-778", ["claim_id", "provider", "billed"]])
# CL1 City Hospital 1450.0 | CL3 City Hospital 1450.0 | CL6 Westside Surgery 3100.0
# CL1 and CL3: same patient, same provider, same amount, so check for a duplicate bill
```

**4. The `max()`-on-text trap.**

```python
print(claims["provider"].max())                    # Westside Surgery: just last alphabetically
print(claims["provider"].value_counts().head(2))   # City Hospital 2, Lakeside Clinic 2: the real answer to "who appears most"
```

## My reflection

The non-unique index surprised me most. I'm used to thinking of IDs as unique, so `df.loc['Snow']` returning two rows was a small shock. Then I realised that this is exactly how I'd want to pull every claim for one patient. The other lesson was the `'Sunny'` result. `max()` on text gave a confident answer to a question nobody asked, so I'll check that a column is numeric before summarising it.
