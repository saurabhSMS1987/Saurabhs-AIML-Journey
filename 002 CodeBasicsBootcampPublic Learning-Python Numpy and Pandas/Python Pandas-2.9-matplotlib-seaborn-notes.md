# Data Visualisation with Matplotlib and Seaborn: Notes

*Oct 31, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Matplotlib, Seaborn Tutorial** lecture from the **CodeBasics Python course**.

## Where I started

After several lectures of filtering, grouping and merging, this one was about *showing* the results. It covered five chart types (line, pie, bar, histogram and scatter), each on a small dataset. The lesson I took away is that each chart type answers a different question, and picking the wrong one hides the answer.

## The data in brief

| File | Contents | What stood out |
| --- | --- | --- |
| `linechart.xlsx` | Quarterly sales in $ millions for Fridge, Dishwasher and Washing Machine, Q1 2022 to Q2 2023 (6 quarters) | Fridge sales peaked at 16.4 in Q4 2022, while washing machine sales fell steadily from 9.2 to 6.0. Totals: Fridge 80.9, Dishwasher 53.0, Washing Machine 45.6 |
| `histograms.xlsx` | Exam scores for 30 students | Median 66.5, but two scores of **0** and **9** sit far below the rest |
| `scatter_plot.xlsx` | Area in square feet and price for 10 houses | Price generally rises with area, except a **1,150 sq ft house priced at 41**, well below every house of similar size |

## What I learnt

| Chart | Answers | Lecture code |
| --- | --- | --- |
| **Line** | How does something change over time? | `plt.plot(df["Quarter"], df["Fridge"], label="Fridge")` |
| **Pie** | What share does each part make up? | `plt.pie(totals, labels=totals.index, autopct="%1.1f%%")` |
| **Bar / horizontal bar** | How do categories compare? | `df.set_index("Quarter").plot(kind="bar")` or `kind="barh"` |
| **Histogram** | How are values spread? | `plt.hist(scores)` or `sns.histplot(scores, kde=True)` |
| **Scatter** | Do two numbers move together? | `sns.scatterplot(data=df, x="area_square_ft", y="price")` |

**The two libraries:**

- **Matplotlib** (`plt`) is the foundation. Titles, axis labels, legends, figure size (`plt.figure(figsize=(12, 4))`) and label rotation (`plt.xticks(rotation=45)`) all come from it.
- **Seaborn** (`sns`) is built on Matplotlib and produces better-looking statistical charts with less code. `kde=True` adds a smooth curve over the histogram.

**Plotting from pandas directly:** `df.plot(kind="bar")` uses the DataFrame index for the x-axis. That's why the lecture set `Quarter` as the index first: it put the quarter names on the axis.

**Details I noticed:**

- **A missing import:** the notebook uses `sns.histplot` but never runs `import seaborn as sns`, so running it fresh, top to bottom, stops with a `NameError`. Add the import at the start.
- **Charts expose outliers that tables hide.** The 0 and 9 exam scores and the house priced at 41 are obvious on a chart, but easy to miss in a list of numbers.
- **Pie charts compare shares, not change.** The pie showed Fridge was 45.1% of total sales, but only the line chart showed washing machine sales falling.

## How this shows up in financial statement audit work

Charts are evidence in analytical procedures and quick ways to spot risks. These snippets use sample data built in the code, and each one saves its chart as an image for the audit file.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

**1. Line chart: monthly revenue, current year against prior year.** A spike in the final month is a classic revenue cut-off risk:

```python
months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
revenue = pd.DataFrame({
    "FY2025": [410, 425, 418, 432, 440, 455],
    "FY2026": [430, 441, 438, 450, 462, 610],      # $000s
}, index=months)

ax = revenue.plot(marker="o", figsize=(8, 4), title="Monthly revenue ($000s)")
ax.annotate("December spike: test cut-off", xy=(5, 610), xytext=(2, 580),
            arrowprops={"arrowstyle": "->"})
plt.tight_layout()
plt.savefig("revenue_trend.png")
plt.close()
```

**2. Bar chart: flux in operating expenses by account.** This is a visual version of the flux table from Lecture 22:

```python
opex = pd.DataFrame({
    "PY": [148, 61, 92, 40],
    "CY": [205, 98, 94, 41],                       # $000s
}, index=["Consulting", "Travel", "Rent", "Utilities"])

opex.plot(kind="barh", figsize=(7, 3), title="Operating expenses: PY vs CY ($000s)")
plt.tight_layout()
plt.savefig("opex_flux.png")
plt.close()
# Consulting (+39%) and Travel (+61%) stand out, while Rent and Utilities are flat
```

**3. Histogram: journal entries clustered below an approval limit.** If entries above 10,000 need a second approver, a pile-up just below 10,000 suggests entries are being split to avoid review:

```python
rng = np.random.default_rng(5)
je_amounts = np.concatenate([
    rng.gamma(2.0, 2_500, 950),                    # normal activity
    rng.uniform(9_500, 9_999, 50),                 # suspicious cluster
])

sns.histplot(je_amounts[je_amounts < 20_000], bins=40)
plt.axvline(10_000, color="red", linestyle="--", label="Approval limit")
plt.title("Journal entry amounts")
plt.legend()
plt.savefig("je_histogram.png")
plt.close()

near_limit = ((je_amounts >= 9_500) & (je_amounts < 10_000)).sum()
print(near_limit)    # 64: far more than a smooth distribution would place in a $500 band
```

**4. Scatter plot: revenue against units shipped by branch.** Like the house priced at 41, a branch that sits away from the trend line is the one to investigate:

```python
branches = pd.DataFrame({
    "branch":  ["North", "South", "East", "West", "Central", "Coastal"],
    "units":   [1200, 950, 1500, 800, 1100, 1000],
    "revenue": [600, 470, 760, 405, 545, 820],     # $000s
})

sns.scatterplot(data=branches, x="units", y="revenue")
for _, row in branches.iterrows():
    plt.annotate(row["branch"], (row["units"], row["revenue"]), fontsize=8)
plt.title("Revenue vs units shipped")
plt.savefig("revenue_vs_units.png")
plt.close()

branches["rev_per_unit"] = (branches["revenue"] * 1000 / branches["units"]).round(0)
print(branches.sort_values("rev_per_unit", ascending=False).head(1))
# Coastal: 820 revenue per unit against about 500 elsewhere, so check pricing and occurrence
```

## My reflection

This lecture reminded me that a good chart is often the fastest way to explain a finding to a client or an engagement partner. A December spike, or a cluster of entries just under an approval limit, is obvious in a picture and easy to lose in a spreadsheet.

The lecture's data made the same point without meaning to. The exam score of 0 and the house priced at 41 jumped out the moment they were plotted. So my habit now is to chart a population before testing it: a histogram for amounts, a line for trends and a scatter plot for any two figures that should move together. The outliers usually show me where to look first.
