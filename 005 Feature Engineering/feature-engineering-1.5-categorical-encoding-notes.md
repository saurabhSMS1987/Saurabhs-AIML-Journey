# Encoding Categorical Data: One-Hot, Label and Ordinal: My Feature Engineering Notes

*Nov 3, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Nominal / One-Hot Encoding** lecture from **Krish Naik Academy**. Encoder options such as `handle_unknown` and `min_frequency` come from the [scikit-learn preprocessing documentation](https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features).

## Where I started

Machine learning models work with numbers, but much of the data I deal with is **text categories**: entity, account type, journal source, risk rating. This lecture covered three ways to turn categories into numbers. The key lesson is that the right method depends on whether the categories have a **natural order**.

## The data in brief

Small examples built in the notebook:

- **Colours:** `red`, `blue`, `green` across 6 rows, used for one-hot and label encoding.
- **Sizes:** `small`, `medium`, `large` across 6 rows, used for ordinal encoding.
- The seaborn **tips** dataset (244 restaurant bills, with text columns like `sex`, `smoker`, `day` and `time`) was loaded as an example of real categorical data.

## What I learnt

The lecture introduced three encodings (a fourth, target-guided ordinal encoding, is coming up next):

| Encoding | Use when | `red, blue, green` becomes |
| --- | --- | --- |
| **One-hot (nominal)** | Categories have **no order** | Three 0/1 columns |
| **Label** | Each category just needs a number | `red=2, blue=0, green=1` (alphabetical) |
| **Ordinal** | Categories **have a natural order** | Numbers in the order you define |

**1. One-hot encoding:** one new column per category, with a 1 marking which applies:

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

df = pd.DataFrame({"color": ["red", "blue", "green", "green", "red", "blue"]})
encoder = OneHotEncoder()
encoded = encoder.fit_transform(df[["color"]]).toarray()
encoder_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out())
# columns: color_blue, color_green, color_red; "red" -> [0, 0, 1]
```

`fit_transform` learns the categories and encodes them, while `transform` reuses what was learnt on new data: `encoder.transform([["blue"]])` gives `[1, 0, 0]`.

**2. Label encoding:** one number per category:

```python
from sklearn.preprocessing import LabelEncoder

lbl_encoder = LabelEncoder()
lbl_encoder.fit_transform(df["color"])        # [2, 0, 1, 1, 2, 0]: blue=0, green=1, red=2
```

The numbers follow **alphabetical order**, so they suggest an order the colours don't really have. `LabelEncoder` is designed for the **target column** (the thing being predicted). That's why the lecture saw a warning when it was given a table (`df[["color"]]`) instead of a single column (`df["color"]`).

**3. Ordinal encoding:** numbers in a meaningful order that **you** specify:

```python
from sklearn.preprocessing import OrdinalEncoder

sizes = pd.DataFrame({"size": ["small", "medium", "large", "medium", "small", "large"]})
encoder = OrdinalEncoder(categories=[["small", "medium", "large"]])
encoder.fit_transform(sizes[["size"]]).ravel()  # [0, 1, 2, 1, 0, 2]: small < medium < large
```

**The rule of thumb:** no order means one-hot; a real order means ordinal. Label encoding is mainly for the target.

## How this shows up in financial statement audit work

Any model that scores journal entries or customers needs categorical fields turned into numbers. These snippets use small sample data built in the code.

**1. One-hot encoding journal entry attributes, safe for next year's data.** `handle_unknown="ignore"` means a new entity or source that appears later doesn't crash the model. It's simply encoded as all zeros:

```python
from sklearn.preprocessing import OneHotEncoder

je = pd.DataFrame({
    "entity": ["UK", "US", "IN", "US", "UK"],
    "source": ["Manual", "Automated", "Automated", "Manual", "Automated"],
})
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
features = pd.DataFrame(ohe.fit_transform(je), columns=ohe.get_feature_names_out())
print(features.columns.tolist())
# ['entity_IN', 'entity_UK', 'entity_US', 'source_Automated', 'source_Manual']

next_year = pd.DataFrame({"entity": ["SG"], "source": ["Manual"]})     # a new entity, never seen
print(ohe.transform(next_year))                                        # [[0. 0. 0. 0. 1.]]: no error
```

**2. Ordinal encoding where order matters: aging buckets and risk ratings.** Receivables aging and inherent risk have a real order, so the numbers should respect it:

```python
from sklearn.preprocessing import OrdinalEncoder

ar = pd.DataFrame({
    "aging": ["0-30", "91+", "31-60", "61-90", "0-30"],
    "risk":  ["Low", "High", "Medium", "High", "Low"],
})
ord_enc = OrdinalEncoder(categories=[["0-30", "31-60", "61-90", "91+"], ["Low", "Medium", "High"]])
ar[["aging_code", "risk_code"]] = ord_enc.fit_transform(ar[["aging", "risk"]])
print(ar.to_string(index=False))
# 91+ -> 3 and High -> 2: older and riskier balances get higher numbers
```

Label encoding would have sorted these alphabetically (`0-30, 31-60, 61-90, 91+` happens to work, but `High, Low, Medium` becomes `0, 1, 2`), which puts High *below* Low. That's exactly the kind of silent error that matters in a risk model.

**3. Many categories: hundreds of vendors.** One-hot encoding creates a column per vendor, which quickly becomes unwieldy. `min_frequency` groups rare vendors into one "infrequent" column:

```python
import numpy as np

rng = np.random.default_rng(1)
vendors = pd.DataFrame({"vendor": rng.choice([f"V{i:03d}" for i in range(200)], 1_000,
                                             p=np.r_[np.full(5, 0.12), np.full(195, 0.4 / 195)])})

plain = OneHotEncoder().fit(vendors)
grouped = OneHotEncoder(min_frequency=20, handle_unknown="infrequent_if_exist").fit(vendors)
print(len(plain.get_feature_names_out()), "->", len(grouped.get_feature_names_out()), "columns")   # 175 -> 6: five big vendors plus one "infrequent" column
print(grouped.get_feature_names_out()[-1])                             # vendor_infrequent_sklearn
```

**4. The target column: label encoding done right.** `LabelEncoder` belongs on the outcome being predicted, given a single column:

```python
from sklearn.preprocessing import LabelEncoder

outcome = pd.Series(["No issue", "Issue", "No issue", "No issue", "Issue"])
target_enc = LabelEncoder()
y = target_enc.fit_transform(outcome)
print(dict(zip(target_enc.classes_, range(len(target_enc.classes_)))), y)
# {'Issue': 0, 'No issue': 1} [1 0 1 1 0]
```

## My reflection

The order question is the real lesson. Encoding looks like a mechanical step, but choosing the wrong method quietly tells the model something false, such as "red is bigger than blue", or worse, "High risk is lower than Low risk". In audit analytics, where risk ratings and aging buckets drive conclusions, that's not a technicality.

The `handle_unknown="ignore"` option also felt very practical. Client data changes every year: new entities, new journal sources, new vendors. A model that crashes on the first unfamiliar value isn't much use for a recurring audit.
