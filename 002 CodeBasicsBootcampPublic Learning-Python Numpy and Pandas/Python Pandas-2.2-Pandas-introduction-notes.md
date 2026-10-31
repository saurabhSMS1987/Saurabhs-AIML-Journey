# pandas Introduction: My Lecture 18 Notes

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **pandas Introduction** lecture from the **CodeBasics Python course**.

## Where I started

The lecture answered one simple question twice: what are the lowest, highest and average IMDb ratings, overall and for Bollywood and Hollywood separately? First it used plain Python and the `csv` module, with a loop, a helper function and manual checks for `'NULL'`. Then it used pandas, and the same answers took a handful of short lines. That contrast sold me on pandas before I'd learnt a single command in depth.

## The data in brief

A small `movies.csv` file: **37 films** (20 Hollywood, 17 Bollywood) with 10 columns: title, industry, release year, IMDb rating, studio, budget, revenue, unit, currency and language.

Some quirks are worth noticing, because real extracts look just like this:

- **One missing rating** (*Sanju*) and **three missing studios**.
- Budget and revenue use **mixed units** (Thousands, Millions and Billions) and **mixed currencies** (USD for Hollywood, INR for Bollywood). The raw numbers can't be added or compared until they are converted.

**Results:**

| Group | Min rating | Max rating | Average |
| --- | --- | --- | --- |
| All movies | 1.9 | 9.3 | 7.92 |
| Bollywood | 1.9 | 8.4 | 7.66 |
| Hollywood | 6.8 | 9.3 | 8.13 |

## What I learnt

**A DataFrame** is pandas' table: named columns, numbered rows, and the right type for each column.

```python
import pandas as pd

df = pd.read_csv("movies.csv")     # one line replaces the csv loop
df.head()                          # first 5 rows
df.tail(5)                         # last 5 rows
df.sample(5)                       # 5 random rows
df[2:6]                            # rows 2 to 5, sliced like a list
df.shape                           # (37, 10): rows, columns
```

**Column statistics** use dot notation:

```python
df.imdb_rating.min(), df.imdb_rating.max(), df.imdb_rating.mean()   # (1.9, 9.3, 7.92)
```

**Filtering** works like NumPy's boolean masks, but with column names:

```python
df_b = df[df.industry == "Bollywood"]
df_b.imdb_rating.mean()            # 7.66
```

**Plain Python vs pandas:**

| Task | Plain Python | pandas |
| --- | --- | --- |
| Read the file | `csv.reader` plus a loop | `pd.read_csv()` |
| Skip missing values | Manual `!= 'NULL'` check | Done automatically |
| Filter by industry | `if` inside the loop | `df[df.industry == "Bollywood"]` |
| Min, max, average | A custom function | `.min()`, `.max()`, `.mean()` |

One detail I noticed: pandas skipped *Sanju*'s missing rating **silently** when it worked out the average. That's convenient, but it means the average is based on 36 films, not 37, and nothing warns you.

## How this shows up in healthcare audit work

These snippets use a small sample of hospital claims, built in the code so they run without any file.

```python
import pandas as pd

claims = pd.DataFrame({
    "claim_id":      ["H01", "H02", "H03", "H04", "H05", "H06", "H07", "H08"],
    "provider_type": ["Hospital", "Clinic", "Hospital", "Clinic",
                      "Hospital", "Clinic", "Hospital", "Hospital"],
    "length_of_stay":[3, 1, 21, 1, 4, None, 2, 5],
    "billed":        [12.4, 850, 96.0, 620, 18.9, 540, 9.8, 22.5],
    "unit":          ["Thousands", "Units", "Thousands", "Units",
                      "Thousands", "Units", "Thousands", "Thousands"],
})
```

**1. First look at a new extract.** `sample()` also gives a quick random selection for walkthroughs.

```python
print(claims.shape)                         # (8, 5)
print(claims.head(3))
print(claims.sample(2, random_state=1))     # fixed seed, so a reviewer gets the same 2 claims
```

**2. Length of stay: overall and by provider type.**

```python
los = claims.length_of_stay
print(los.min(), los.max(), round(los.mean(), 1))      # 1.0 21.0 5.3

hospitals = claims[claims.provider_type == "Hospital"]
print(hospitals.length_of_stay.max())                  # 21.0: one admission far above the rest
```

**3. Missing values that pandas quietly skips.** This is the *Sanju* lesson, applied to claims.

```python
print(claims.length_of_stay.isnull().sum())            # 1 claim has no length of stay
print(claims.length_of_stay.count())                   # 7: the average uses 7 claims, not 8
print(claims[claims.length_of_stay.isnull()].claim_id.tolist())   # ['H06']: follow up
```

**4. Mixed units, the movies budget problem.** Hospitals reported in thousands and clinics in dollars, so the raw totals mean nothing until they're converted.

```python
print(claims.billed.sum())                             # 2169.6: meaningless mix of units

claims["billed_usd"] = claims.billed
claims.loc[claims.unit == "Thousands", "billed_usd"] = claims.billed * 1000
print(claims.billed_usd.sum())                         # 161610.0: the real total billed
```

## My reflection

The side-by-side comparison made the case for pandas better than any explanation could. The more useful lesson for audit, though, came from the data itself. The mixed currencies and units in `movies.csv` are exactly what happens when extracts come from different systems, and pandas won't warn you before it adds thousands to dollars. The silently skipped *Sanju* rating was the same kind of lesson. So I'll check `isnull()` and the unit columns before trusting any total or average.

Next, I want to practise:

- [ ] Load a claims extract and check `shape`, `head()` and missing values first
- [ ] Compare average length of stay for hospitals and clinics using filters
- [ ] Standardise mixed units into one column before totalling billed amounts
