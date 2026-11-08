# EDA and Feature Engineering: Google Play Store Data: My Notes

*Nov 8, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **EDA and Feature Engineering: Google Play Store Dataset** lecture from **Krish Naik Academy**. The dataset is loaded from the course's [GitHub repository](https://github.com/krishnaik06/playstore-Dataset). I re-ran the cleaning steps on that file to check the figures below.

## Where I started

This was the most "real-world" dataset in the course so far. It looks tidy at first, but almost every column hides a problem: review counts written as `3.0M`, sizes in two units, install counts like `10,000+`, prices with `$` signs, and one row where **every value had slipped one column to the left**. The lecture worked through **data cleaning → EDA → insights**, and it felt very close to preparing a client's journal entry extract.

## The data in brief

**10,841 apps** with 13 columns, including **App, Category, Rating, Reviews, Size, Installs, Type** (free or paid), **Price, Content Rating, Genres** and **Last Updated**. Only `Rating` arrived as a number.

| Problem found | Where |
| --- | --- |
| Missing values | `Rating` (1,474), plus one each in `Type` and `Content Rating` |
| A **shifted row** | Row 10472: Category `1.9`, Rating `19.0` (impossible, since ratings max at 5), Reviews `3.0M` |
| Numbers stored as text | `Reviews`, `Size`, `Installs`, `Price` |
| **1,181 duplicate apps** | The same app listed more than once |

## The notebook, step by step

### 1. Setup and first look

| Code | What it does |
| --- | --- |
| `warnings.filterwarnings("ignore")` | Hides warning messages to keep output clean (but it also hides useful alerts) |
| `pd.read_csv("https://raw.githubusercontent.com/...")` | Reads a CSV **straight from a URL**, with no download needed |
| `df.shape`, `df.info()`, `df.describe()`, `df.isnull().sum()` | Size, column types, summary statistics and missing values. `describe()` showed a **maximum rating of 19**, the first clue to the bad row |

### 2. Clean `Reviews`: find what won't convert

```python
df["Reviews"].astype(int)                      # ValueError: invalid literal ... '3.0M'
df[~df["Reviews"].str.isnumeric()]             # ~ means NOT: shows the one non-numeric row (10472)
df_copy = df.copy()                            # work on a copy and keep the raw data intact
df_copy = df_copy.drop(df_copy.index[10472])   # remove the shifted row
df_copy["Reviews"] = df_copy["Reviews"].astype(int)
```

Trying the conversion and letting it **fail** is a quick way to find bad values. `str.isnumeric()` then pinpoints exactly which rows are the problem.

### 3. Clean `Size`: two units, plus text

```python
df_copy["Size"] = df_copy["Size"].str.replace("M", "000")              # megabytes -> kilobytes
df_copy["Size"] = df_copy["Size"].str.replace("k", "")                 # kilobytes stay as they are
df_copy["Size"] = df_copy["Size"].replace("Varies with device", np.nan)
df_copy["Size"] = df_copy["Size"].astype(float)
```

The aim is one unit (KB), with "Varies with device" becoming a missing value. **One catch:** replacing `M` with `000` only works for whole numbers. `19M` becomes `19000` correctly, but `8.7M` becomes `8.7000`, which is **8.7**, not 8,700. **3,608 sizes** have a decimal like this. Multiplying the number instead (`8.7 × 1000`) avoids it, as audit snippet 1 shows.

### 4. Clean `Installs` and `Price`: strip symbols in a loop

```python
chars_to_remove = ["+", ",", "$"]
cols_to_clean = ["Installs", "Price"]
for item in chars_to_remove:
    for cols in cols_to_clean:
        df_copy[cols] = df_copy[cols].str.replace(item, "")
df_copy["Installs"] = df_copy["Installs"].astype("int")     # "10,000+" -> 10000
df_copy["Price"] = df_copy["Price"].astype("float")         # "$4.99" -> 4.99
```

A nested loop applies every clean-up to every column, and the code stays short however many symbols or columns there are. Note that an install count like `10,000+` is a **lower bound**, so totals built from it are approximate.

### 5. Turn `Last Updated` into date features

```python
df_copy["Last Updated"] = pd.to_datetime(df_copy["Last Updated"])   # "January 7, 2018" -> a real date
df_copy["Day"] = df_copy["Last Updated"].dt.day
df_copy["Month"] = df_copy["Last Updated"].dt.month
df_copy["Year"] = df_copy["Last Updated"].dt.year
df_copy.to_csv("data/google_cleaned.csv")                          # save the cleaned version
```

`pd.to_datetime` understands written-out dates directly, which is simpler than the manual splitting in the flight-price lecture.

### 6. Remove duplicate apps

```python
df_copy[df_copy.duplicated("App")].shape                          # (1181, 16)
df_copy = df_copy.drop_duplicates(subset=["App"], keep="first")   # 10,840 -> 9,659 apps
```

`subset=["App"]` treats rows as duplicates when the **app name** matches, even if other columns differ. `keep="first"` keeps whichever copy appears first. In this data, **517** duplicated apps have copies with **different review counts**, so the copy kept is effectively arbitrary. Sorting first (for example, by most reviews) would make that choice deliberate.

### 7. Split features by type

```python
numeric_features = [f for f in df_copy.columns if df_copy[f].dtype != "O"]       # 9 numeric
categorical_features = [f for f in df_copy.columns if df_copy[f].dtype == "O"]   # 7 categorical
```

`"O"` is pandas' code for **object** (text) columns. Separating the two types lets each get the right chart.

### 8. Visual EDA

| Code | Chart | What it showed |
| --- | --- | --- |
| `value_counts(normalize=True) * 100` in a loop | Text output | The share of each category, in percent |
| `plt.subplot(5, 3, i+1)` + `sns.kdeplot(...)` in a loop | A **grid** of density curves | Rating and Year are **left-skewed**; Reviews, Size, Installs and Price are **right-skewed** |
| `sns.countplot(x=df["Type"])` | Bar counts | Most apps are free; most are rated "Everyone" |
| `value_counts().plot.pie(autopct="%1.1f")` | Pie chart | Each category's share, labelled with percentages |
| `sns.barplot(x=category.index[:10], y="Count", ...)` | Top-10 bar chart | Family, Game and Tools have the most apps |

`plt.subplot(rows, cols, position)` places several charts on one figure, and `plt.tight_layout()` stops their labels overlapping.

### 9. Answering business questions with `groupby`

```python
# Which category has the most installs?
df_copy.groupby("Category")["Installs"].sum().sort_values(ascending=False)

# Top 5 apps by installs within each popular category
dfa = df_copy.groupby(["Category", "App"])["Installs"].sum().reset_index().sort_values("Installs", ascending=False)
dfa[dfa.Category == "GAME"].head(5)

# How many apps have a perfect 5.0 rating?
(df_copy["Rating"] == 5.0).sum()                                  # 271
```

**Results from the lecture:** Game is the most-installed category, with Subway Surfers, Hangouts, Google Drive and Instagram leading their categories. **271 apps** have a perfect 5.0 rating, which I confirmed on the deduplicated data.

**A note on the saved outputs:** the category table in the notebook still includes the shifted row's `1.9` category and uses pre-deduplication counts (Family 1,972). That suggests some cells were run out of order. When I re-ran the steps in order, Game remained the most-installed category, but with **13.9 billion** installs, not the ~35 billion in the saved output. **Duplicate listings had more than doubled the total.**

## How this shows up in my audit work with journal entry data

Every problem in this dataset has a journal entry equivalent: amounts stored as text, shifted rows from a bad export, duplicate postings and unit mix-ups. These snippets apply the lecture's techniques to a small sample extract.

```python
import numpy as np
import pandas as pd

raw = pd.DataFrame({
    "je_id": ["JE01", "JE02", "JE03", "JE04", "JE05", "JE06", "JE02"],
    "posting_date": ["31/12/2026", "15/11/2026", "4,500.00", "02/12/2026", "20/12/2026", "28/12/2026", "15/11/2026"],
    "amount": ["$12,500.00", "(3,200.50)", "Manual", "1.2K", "2.5M", "980", "(3,200.50)"],
    "preparer": ["A. Rao", "M. Gomez", "15/12/2026", "J. Lee", "A. Rao", "M. Gomez", "M. Gomez"],
    "source": ["Manual", "Manual", "S. Patel", "Automated", "Manual", "Manual", "Manual"],
})
```

**1. Converting text amounts safely, the right way to do the `Size` clean-up.** It strips symbols, treats brackets as negative, and **multiplies** `K` and `M` suffixes instead of replacing letters:

```python
def to_amount(text):
    s = str(text).strip().replace("$", "").replace(",", "")
    negative = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    multiplier = {"K": 1_000, "M": 1_000_000}.get(s[-1:].upper(), 1)
    if multiplier > 1:
        s = s[:-1]
    try:
        value = float(s) * multiplier
    except ValueError:
        return np.nan                      # not a number at all: leave it for review
    return -value if negative else value

raw["amount_num"] = raw["amount"].map(to_amount)
print(raw[["je_id", "amount", "amount_num"]].to_string(index=False))
# $12,500.00 -> 12500.0 | (3,200.50) -> -3200.5 | 1.2K -> 1200.0 | 2.5M -> 2500000.0 | Manual -> NaN
```

**2. Finding shifted or corrupt rows,** the journal entry version of row 10472. A date that won't parse, or an amount that isn't a number, gives it away:

```python
dates = pd.to_datetime(raw["posting_date"], format="%d/%m/%Y", errors="coerce")   # bad dates become NaT
suspect = raw[dates.isna() | raw["amount_num"].isna()]
print(suspect[["je_id", "posting_date", "amount", "preparer"]].to_string(index=False))
# JE03: a number in the date column and a date in the preparer column, so every field slipped one place
```

Instead of quietly dropping it, as the lecture did with one app, a shifted row in a ledger goes back to the client: it may mean the whole export needs re-running.

**3. Duplicates and double counting.** The Play Store duplicates inflated game installs from 13.9 to 35.1 billion. Duplicate journal entries inflate balances in exactly the same way:

```python
clean = raw.drop(suspect.index)
dupes = clean[clean.duplicated(subset=["je_id"], keep=False)]
print(dupes[["je_id", "amount_num"]].to_string(index=False))          # JE02 appears twice
print(round(clean["amount_num"].sum(), 2), "->", round(clean.drop_duplicates("je_id")["amount_num"].sum(), 2))
# 2508279.0 -> 2511479.5: the duplicated credit had been counted twice
```

**4. Top-N within each group,** the lecture's "top 5 apps per category", applied to the largest manual entries per preparer:

```python
manual = clean[clean["source"] == "Manual"].drop_duplicates("je_id")
print(manual.sort_values("amount_num", ascending=False).groupby("preparer").head(1)[["preparer", "je_id", "amount_num"]]
      .to_string(index=False))
# A. Rao: JE05 at 2,500,000 (the "2.5M" entry, worth a closer look) | M. Gomez: JE06 at 980
```

## My reflection

This lecture showed how much work hides behind "the data looks fine". The shifted row was a single line among 10,841, yet it produced an impossible rating of 19. One wrong assumption in the `Size` clean-up quietly mis-scaled 3,608 values. And the duplicates more than doubled the headline insight about game installs. None of these raised an error. They just made the answers wrong.

That's the lesson I'm taking into journal entry work: **test every conversion**, **look at the rows that fail rather than dropping them**, and **check totals before and after deduplication**. In audit, a duplicated posting or a mis-scaled amount isn't a modelling nuisance. It's a misstatement.
