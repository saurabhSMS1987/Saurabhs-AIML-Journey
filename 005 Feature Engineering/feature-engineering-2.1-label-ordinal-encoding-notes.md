# Label and Ordinal Encoding: My Feature Engineering Notes

*Nov 4, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Label and Ordinal Encoding** lecture from **Krish Naik Academy**. Options such as `handle_unknown` and `inverse_transform` come from the [scikit-learn preprocessing documentation](https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features).

## Where I started

The previous lecture's notebook introduced three encodings at once. This lecture zoomed in on the two that turn each category into a **single number**: **label encoding** and **ordinal encoding**. They look almost the same, but the difference between them, whether the numbers carry a real order, is the whole point.

## The data in brief

Two small examples built in the notebook:

- **Colours:** `red`, `blue`, `green` across 6 rows. They have no natural order.
- **Sizes:** `small`, `medium`, `large` across 6 rows. They have a clear order.

## What I learnt

**Label encoding:** each category gets a number, assigned in **alphabetical order**:

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.DataFrame({"color": ["red", "blue", "green", "green", "red", "blue"]})
lbl_encoder = LabelEncoder()
lbl_encoder.fit_transform(df["color"])     # [2, 0, 1, 1, 2, 0]
lbl_encoder.transform(["red"])             # [2]
lbl_encoder.transform(["blue"])            # [0]
lbl_encoder.transform(["green"])           # [1]
```

`blue=0, green=1, red=2` is just alphabetical. It doesn't mean green is "between" blue and red. `LabelEncoder` is built for a **single column**, typically the target being predicted. That's why the lecture saw a warning when it was given a table (`df[["color"]]`) rather than a column (`df["color"]`).

**Ordinal encoding:** you decide the order, and the numbers follow it:

```python
from sklearn.preprocessing import OrdinalEncoder

sizes = pd.DataFrame({"size": ["small", "medium", "large", "medium", "small", "large"]})
encoder = OrdinalEncoder(categories=[["small", "medium", "large"]])
encoder.fit_transform(sizes[["size"]]).ravel()     # [0, 1, 2, 1, 0, 2]
encoder.transform(pd.DataFrame({"size": ["small"]}))   # [[0.]]
```

Without the `categories=` list, `OrdinalEncoder` would also fall back to alphabetical order (`large=0, medium=1, small=2`), which turns the sizes upside down.

| | Label encoding | Ordinal encoding |
| --- | --- | --- |
| Order of numbers | Alphabetical | The order **you** specify |
| Designed for | The target (one column) | Input features (one or more columns) |
| Use when | You just need a number per class | The categories have a real ranking |
| Example | Outcome: `Issue` / `No issue` | Size: `small < medium < large` |

## How this shows up in financial statement audit work

Audit data is full of **ranked** categories: aging buckets, risk ratings, control assessments and impairment stages. Their order carries meaning, so it must survive encoding. These snippets use small sample data built in the code.

**1. IFRS 9 impairment stages and control ratings: order defined explicitly.**

```python
from sklearn.preprocessing import OrdinalEncoder

loans = pd.DataFrame({
    "ifrs9_stage": ["Stage 1", "Stage 3", "Stage 2", "Stage 1"],
    "control_rating": ["Effective", "Ineffective", "Needs improvement", "Effective"],
})
enc = OrdinalEncoder(categories=[
    ["Stage 1", "Stage 2", "Stage 3"],                         # performing -> credit-impaired
    ["Effective", "Needs improvement", "Ineffective"],          # better -> worse
])
loans[["stage_code", "control_code"]] = enc.fit_transform(loans)
print(loans.to_string(index=False))
# Stage 3 -> 2 and Ineffective -> 2: higher numbers always mean higher risk
```

**2. A new category next year shouldn't crash the model.** By default, an unseen value raises an error. `handle_unknown="use_encoded_value"` gives it a marker value instead, so it can be spotted and reviewed:

```python
risk_enc = OrdinalEncoder(categories=[["Low", "Medium", "High"]],
                          handle_unknown="use_encoded_value", unknown_value=-1)
risk_enc.fit(pd.DataFrame({"risk": ["Low", "Medium", "High"]}))
print(risk_enc.transform(pd.DataFrame({"risk": ["High", "Critical"]})).ravel())
# [ 2. -1.]: "Critical" wasn't in the agreed scale, so it's flagged with -1 for follow-up
```

**3. Label encoding the target, and decoding the model's answers.** `inverse_transform` turns numeric predictions back into words for the workpaper:

```python
from sklearn.preprocessing import LabelEncoder

outcome = pd.Series(["No issue", "Issue", "No issue", "Issue", "No issue"])
target_enc = LabelEncoder()
y = target_enc.fit_transform(outcome)
print(y, list(target_enc.classes_))                      # [1 0 1 0 1] ['Issue', 'No issue']

model_predictions = [0, 1, 1]                            # imagine these came from a trained model
print(list(target_enc.inverse_transform(model_predictions)))   # ['Issue', 'No issue', 'No issue']
```

**4. The trap: label-encoding an unordered feature.** Vendor names have no order, but label encoding gives them one anyway:

```python
vendors = pd.Series(["Zenith Ltd", "Acme Corp", "Midway Inc"])
print(dict(zip(vendors, LabelEncoder().fit_transform(vendors))))
# {'Zenith Ltd': 2, 'Acme Corp': 0, 'Midway Inc': 1}
```

A model would read "Zenith is twice Midway", which is meaningless. For unordered features like vendors or entities, one-hot encoding (from the last lecture) is the safer choice.

## My reflection

The lesson I'll keep is that encoding is a **judgement**, not a mechanical step. The same three words become very different numbers depending on whether I tell Python the order or let it sort them alphabetically. In audit analytics, where Stage 3 must outrank Stage 1 and "Ineffective" must outrank "Effective", leaving the order to the alphabet could quietly invert a risk model.

The `unknown_value=-1` option also felt very audit-minded. When a client's data contains a category nobody agreed on, I want it flagged and reviewed, not silently forced into the scale or crashing the whole run.
