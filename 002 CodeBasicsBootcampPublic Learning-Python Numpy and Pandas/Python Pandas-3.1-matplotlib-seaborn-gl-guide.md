# Matplotlib and Seaborn for General Ledger Analysis: A Practical Guide

*Oct 31, 2026 · Saurabh S*

> [!NOTE]
> **Sources:** Chart behaviour and syntax come from the official documentation: the **Matplotlib** [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html), [Axes guide](https://matplotlib.org/stable/users/explain/axes/index.html), [Plot types gallery](https://matplotlib.org/stable/plot_types/index.html) and API reference; the **seaborn** [User guide and tutorial](https://seaborn.pydata.org/tutorial.html) and [API reference](https://seaborn.pydata.org/api.html); and the **pandas** [Chart visualization guide](https://pandas.pydata.org/docs/user_guide/visualization.html). The Benford's law expected frequencies follow Mark Nigrini's *Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection* (Wiley, 2012). The full list is in [Sources](#sources). Every example was run and checked on **Matplotlib 3.10, seaborn 0.13.2, pandas 3.0 and Python 3.12**. The general ledger is invented sample data.

A general ledger holds the full story of a company's year, but thousands of rows of journal entries are hard to read as a table. Charts turn that population into something you can scan in seconds: a revenue spike in December, entries piling up just below an approval limit, postings at 2 a.m. on a Saturday. This guide covers Matplotlib and seaborn from the basics to multi-chart dashboards, with every example built on general ledger data.

## How to use this guide

1. Run `python make_gl_sample.py` to create `sample_data/gl_fy2025_fy2026.csv`. It holds about 11,500 GL lines (5,700 journal entries) over two years, with a few red flags hidden in it.
2. Run the [setup block](#setup) once. Every later snippet uses its variables and saves its chart to a `charts` folder.

**Sign convention:** debits are positive and credits are negative, as in most ledger extracts. Revenue is therefore negative in the GL, and the examples flip its sign before charting it.

## Contents

**Part 1: Foundations**
1. [Setup](#setup)
2. [The two ways to use Matplotlib](#1-the-two-ways-to-use-matplotlib)
3. [Choosing the right chart for an audit question](#2-choosing-the-right-chart-for-an-audit-question)

**Part 2: Matplotlib**

4. [Line charts: trends over time](#3-line-charts-trends-over-time)
5. [Bar charts: comparing categories](#4-bar-charts-comparing-categories)
6. [Waterfall (bridge) chart](#5-waterfall-bridge-chart)
7. [Histograms: how amounts are spread](#6-histograms-how-amounts-are-spread)
8. [Scatter plots: two measures together](#7-scatter-plots-two-measures-together)
9. [Box plots](#8-box-plots)
10. [Pie and donut charts, used sparingly](#9-pie-and-donut-charts-used-sparingly)
11. [Benford's law first-digit test](#10-benfords-law-first-digit-test)
12. [Two y-axes](#11-two-y-axes)
13. [Date axes and highlighted periods](#12-date-axes-and-highlighted-periods)
14. [Multi-chart dashboards](#13-multi-chart-dashboards)
15. [Formatting: currency, labels, styles and colours](#14-formatting-currency-labels-styles-and-colours)
16. [Saving charts for the audit file](#15-saving-charts-for-the-audit-file)

**Part 3: seaborn**

17. [How seaborn thinks](#16-how-seaborn-thinks)
18. [Distributions](#17-distributions)
19. [Categories: counts, totals and spreads](#18-categories-counts-totals-and-spreads)
20. [Heatmaps](#19-heatmaps)
21. [Relationships and trends](#20-relationships-and-trends)
22. [Regression plots](#21-regression-plots)
23. [Multi-chart grids](#22-multi-chart-grids)
24. [The seaborn objects interface](#23-the-seaborn-objects-interface)
25. [Themes, palettes and mixing with Matplotlib](#24-themes-palettes-and-mixing-with-matplotlib)

**Part 4: Getting it right**

26. [Audit-ready chart checklist](#25-audit-ready-chart-checklist)
27. [Troubleshooting](#26-troubleshooting)
28. [Sources](#sources)

---

# Part 1: Foundations

## Setup

```python
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import seaborn as sns

gl = pd.read_csv("sample_data/gl_fy2025_fy2026.csv",
                 dtype={"account": str},                       # account codes are IDs, not numbers
                 parse_dates=["posting_date", "posted_at"])
gl["year"] = gl["posting_date"].dt.year
gl["month"] = gl["posting_date"].dt.month

# one row per journal entry (line 1 is always the debit side)
je = gl[gl["line"] == 1].copy()
je["weekday"] = je["posted_at"].dt.day_name()
je["hour"] = je["posted_at"].dt.hour
je["is_weekend"] = je["posted_at"].dt.dayofweek >= 5

CHARTS = Path("charts")
CHARTS.mkdir(exist_ok=True)

def save(fig, name):
    """Save a figure for the audit file, then close it to free memory."""
    fig.savefig(CHARTS / name, dpi=150, bbox_inches="tight")
    plt.close(fig)

usd_k = mtick.FuncFormatter(lambda x, _: f"${x / 1e3:,.0f}K")   # 125000 -> $125K
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
```

## 1. The two ways to use Matplotlib

Matplotlib has two interfaces. The documentation calls them **explicit** (object-oriented) and **implicit** (pyplot):

```python
# implicit (pyplot): quick, but every call changes "the current" chart
plt.plot([1, 2, 3], [10, 20, 15])
plt.title("Quick look")
plt.close()

# explicit (object-oriented): you hold the figure and axes, so nothing is ambiguous
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
ax.plot([1, 2, 3], [10, 20, 15])
ax.set_title("Controlled chart")
save(fig, "01_interfaces.png")
```

This guide uses the **explicit** style, which the Matplotlib documentation recommends for anything beyond a quick look. It's clearer once a figure has several charts.

**Anatomy of a figure:**

| Part | What it is | Set with |
| --- | --- | --- |
| `Figure` | The whole canvas: one image or page | `plt.subplots(figsize=(w, h))` |
| `Axes` | One chart area inside the figure | `fig, ax = plt.subplots()` |
| `Axis` | The x or y scale, with its ticks | `ax.xaxis`, `ax.yaxis` |
| Title and labels | Text describing the chart | `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()` |
| Legend | Key to the series | `ax.legend()` |
| Ticks | Marks and labels on an axis | `ax.set_xticks()`, `ax.yaxis.set_major_formatter()` |

`layout="constrained"` makes Matplotlib space labels and titles so they don't overlap. The documentation now prefers it to the older `tight_layout()`.

## 2. Choosing the right chart for an audit question

| Audit question | Chart | Section |
| --- | --- | --- |
| How did revenue move month by month, against the prior year? | Line | 3 |
| Which accounts or line items changed most? | Grouped bar | 4 |
| What explains the change in profit from last year? | Waterfall | 5 |
| Are entries clustering just below an approval limit? | Histogram | 6, 17 |
| Who posts at unusual hours, and for how much? | Scatter, heatmap | 7, 19 |
| Are manual entries larger or more variable than automated ones? | Box, violin, strip | 8, 18 |
| Do first digits follow the expected pattern? | Benford bar chart | 10 |
| When during the year does posting activity spike? | Date-axis line | 12 |
| Does one account track another, as COGS should track revenue? | Regression plot | 21 |
| Which preparer, entity or month stands out? | Heatmap | 19 |

---

# Part 2: Matplotlib

## 3. Line charts: trends over time

**Monthly revenue, current year (CY) against prior year (PY), with an expectation band:**

```python
revenue = (gl[gl["fsli"] == "Revenue"]
           .pivot_table(index="month", columns="year", values="amount", aggfunc="sum")
           * -1)                                               # credits -> positive revenue

fig, ax = plt.subplots(figsize=(9, 4), layout="constrained")
ax.plot(revenue.index, revenue[2025], marker="o", label="FY2025 (PY)", color="grey")
ax.plot(revenue.index, revenue[2026], marker="o", label="FY2026 (CY)", color="tab:blue")

# expectation: PY plus 6% growth, with a +/-25% tolerance band for normal monthly swings
expected = revenue[2025] * 1.06
ax.fill_between(revenue.index, expected * 0.75, expected * 1.25,
                color="tab:green", alpha=0.15, label="Expected range (PY +6%, ±25%)")

ax.annotate("December above the expected range:\ntest revenue cut-off",
            xy=(12, revenue.loc[12, 2026]), xytext=(7.5, revenue[2026].max() * 0.97),
            arrowprops={"arrowstyle": "->"})
ax.set_xticks(range(1, 13), MONTHS)
ax.yaxis.set_major_formatter(usd_k)
ax.set_title("Monthly revenue: FY2026 vs FY2025")
ax.legend(loc="upper left")
save(fig, "03_revenue_trend.png")

print((revenue[2026] > expected * 1.25).loc[lambda s: s].index.tolist())   # [12]: only December breaches
```

**Useful line options:** `marker="o"`, `linestyle="--"`, `linewidth=2`, `ax.axhline(y)` for a fixed threshold, `ax.axvline(x)` for a date marker, and `ax.fill_between()` for ranges.

## 4. Bar charts: comparing categories

**Grouped bars: operating expenses by account, PY against CY, with value labels:**

```python
opex = (gl[gl["fsli"] == "Operating Expenses"]
        .pivot_table(index="account_name", columns="year", values="amount", aggfunc="sum")
        .sort_values(2026))

y = np.arange(len(opex))
height = 0.4
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
py_bars = ax.barh(y - height / 2, opex[2025], height, label="FY2025", color="grey")
cy_bars = ax.barh(y + height / 2, opex[2026], height, label="FY2026", color="tab:blue")
ax.bar_label(cy_bars, labels=[f"{c:+.0%}" for c in opex[2026] / opex[2025] - 1], padding=3)

ax.set_yticks(y, opex.index)
ax.xaxis.set_major_formatter(usd_k)
ax.set_title("Operating expenses by account (labels show % change)")
ax.legend()
save(fig, "04_opex_flux.png")
```

`ax.bar_label()` writes values or custom labels on each bar. Here it shows the year-on-year change, so the biggest movers stand out without reading the axis.

**Stacked bars: monthly manual entry value by entity:**

```python
manual = (je[(je["source"] == "Manual") & (je["year"] == 2026)]
          .pivot_table(index="month", columns="entity", values="amount", aggfunc="sum", fill_value=0))

fig, ax = plt.subplots(figsize=(9, 4), layout="constrained")
bottom = np.zeros(len(manual))
for entity in manual.columns:
    ax.bar(manual.index, manual[entity], bottom=bottom, label=entity)
    bottom += manual[entity].to_numpy()

ax.set_xticks(range(1, 13), MONTHS)
ax.yaxis.set_major_formatter(usd_k)
ax.set_title("FY2026 manual journal entries by entity")
ax.legend(title="Entity")
save(fig, "04_manual_stacked.png")
```

pandas can draw the same chart in one line: `manual.plot(kind="bar", stacked=True)`.

## 5. Waterfall (bridge) chart

A bridge explains how one figure becomes another, a format audit committees know well. This one goes from PY operating profit to CY operating profit:

```python
pl = gl[gl["fsli"].isin(["Revenue", "Cost of Sales", "Operating Expenses"])]
by_fsli = pl.pivot_table(index="fsli", columns="year", values="amount", aggfunc="sum") * -1   # profit view

py_profit = by_fsli[2025].sum()
steps = {
    "Revenue": by_fsli.loc["Revenue", 2026] - by_fsli.loc["Revenue", 2025],
    "Cost of sales": by_fsli.loc["Cost of Sales", 2026] - by_fsli.loc["Cost of Sales", 2025],
    "Operating expenses": by_fsli.loc["Operating Expenses", 2026] - by_fsli.loc["Operating Expenses", 2025],
}
cy_profit = py_profit + sum(steps.values())

labels = ["FY2025 profit", *steps, "FY2026 profit"]
values = [py_profit, *steps.values(), cy_profit]
bottoms = [0]
running = py_profit
for change in steps.values():
    bottoms.append(running if change >= 0 else running + change)
    running += change
bottoms.append(0)
heights = [abs(v) for v in values]
colours = ["grey"] + ["tab:green" if v >= 0 else "tab:red" for v in steps.values()] + ["tab:blue"]

fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
bars = ax.bar(labels, heights, bottom=bottoms, color=colours)
def bridge_label(i, v):
    if i in (0, len(values) - 1):
        return f"${v / 1e3:,.0f}K"                       # opening and closing totals
    return f"{'+' if v >= 0 else '-'}${abs(v) / 1e3:,.0f}K"  # movements, e.g. +$1,243K

ax.bar_label(bars, labels=[bridge_label(i, v) for i, v in enumerate(values)],
             label_type="center", color="white")
ax.yaxis.set_major_formatter(usd_k)
ax.set_title("Operating profit bridge: FY2025 to FY2026")
save(fig, "05_profit_bridge.png")

print(round(py_profit / 1e3), round(cy_profit / 1e3))   # 2650 2733 ($000s)
```

Each bar starts where the previous one ended (`bottom=`), with increases in green and decreases in red. The final bar must equal reported CY profit, which makes the chart a reconciliation as well as a picture.

## 6. Histograms: how amounts are spread

**JE amounts on a log scale, with the 10,000 approval limit marked:**

```python
amounts = je.loc[je["year"] == 2026, "amount"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")

bins = np.logspace(np.log10(amounts.min()), np.log10(amounts.max()), 60)
ax1.hist(amounts, bins=bins, color="tab:blue")
ax1.set_xscale("log")                                 # amounts span $10s to $250K
ax1.axvline(10_000, color="red", linestyle="--", label="Approval limit $10K")
ax1.set_title("All FY2026 entries (log scale)")
ax1.legend()

manual_amounts = je.loc[(je["year"] == 2026) & (je["source"] == "Manual"), "amount"]
near = manual_amounts[(manual_amounts >= 8_000) & (manual_amounts < 12_000)]
ax2.hist(near, bins=np.arange(8_000, 12_001, 250), color="tab:orange", edgecolor="white")
ax2.axvline(10_000, color="red", linestyle="--")
ax2.set_xticks(range(8_000, 12_001, 1_000))
ax2.xaxis.set_major_formatter(usd_k)
ax2.set_title("Zoom: manual entries between 8K and 12K")   # two "$" in one string would trigger math text
save(fig, "06_je_histogram.png")

print(((manual_amounts >= 9_500) & (manual_amounts < 10_000)).sum(),
      ((manual_amounts >= 10_000) & (manual_amounts < 10_500)).sum())
# 42 3: manual entries pile up just *below* the limit, and very few sit just above it
```

**Key options:** `bins=` takes a number or a list of edges, `density=True` shows proportions instead of counts, `cumulative=True` gives a running total, and `histtype="step"` draws outlines for overlaying groups.

## 7. Scatter plots: two measures together

**Manual entries: hour posted against amount, coloured by weekend:**

```python
manual_cy = je[(je["source"] == "Manual") & (je["year"] == 2026)]

fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
for weekend, colour, label in [(False, "tab:blue", "Weekday"), (True, "tab:red", "Weekend")]:
    subset = manual_cy[manual_cy["is_weekend"] == weekend]
    ax.scatter(subset["hour"], subset["amount"], c=colour, label=label,
               s=np.clip(subset["amount"] / 500, 10, 300), alpha=0.6, edgecolors="none")

ax.axvspan(-0.5, 6.5, color="grey", alpha=0.1)
ax.axvspan(19.5, 23.5, color="grey", alpha=0.1, label="Outside 7am-8pm")
ax.set_yscale("log")
ax.yaxis.set_major_formatter(usd_k)
ax.set_xlim(-0.5, 23.5)
ax.set_xlabel("Hour posted")
ax.set_title("Manual journal entries by hour posted")
ax.legend()
save(fig, "07_hour_scatter.png")

odd = manual_cy[(manual_cy["hour"] < 7) | (manual_cy["hour"] > 19) | manual_cy["is_weekend"]]
print(len(odd), odd["preparer"].value_counts().to_dict())   # 28 {'S. Patel': 25, 'CFO': 3}
```

`s=` sets marker size and `c=` sets colour. Both can come from a column, so one chart can show four dimensions at once.

## 8. Box plots

**Manual against automated entry amounts:**

```python
cy = je[je["year"] == 2026]
groups = [cy.loc[cy["source"] == s, "amount"] for s in ["Automated", "Manual"]]

fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
ax.boxplot(groups, tick_labels=["Automated", "Manual"], showfliers=True)
ax.set_yscale("log")
ax.yaxis.set_major_formatter(usd_k)
ax.set_title("JE amounts by source (FY2026)")
save(fig, "08_boxplot_source.png")
```

The box shows the middle 50% of entries, the line inside is the median, and the dots beyond the whiskers are outliers. Those outliers are often the first entries to select for testing. (`tick_labels=` replaced the older `labels=` argument in Matplotlib 3.9.)

## 9. Pie and donut charts, used sparingly

```python
rev_by_entity = gl[(gl["fsli"] == "Revenue") & (gl["year"] == 2026)].groupby("entity")["amount"].sum() * -1

fig, ax = plt.subplots(figsize=(5, 5), layout="constrained")
ax.pie(rev_by_entity, labels=rev_by_entity.index, autopct="%1.1f%%", startangle=90,
       wedgeprops={"width": 0.4})                     # width < 1 turns a pie into a donut
ax.set_title("FY2026 revenue by entity")
save(fig, "09_revenue_donut.png")
```

Pies show **shares at one point in time**, and only work with a few slices. They can't show change, and people misjudge angles, so a sorted bar chart is usually clearer.

## 10. Benford's law first-digit test

In many naturally occurring financial datasets, the leading digit `1` appears about 30.1% of the time and `9` only about 4.6%. Large deviations can point to invented or manipulated figures. It's a screening test, not proof.

```python
digits = je.loc[je["source"] == "Manual", "amount"].abs().astype(str).str.lstrip("0.").str[0].astype(int)
actual = digits.value_counts(normalize=True).sort_index()
expected = pd.Series(np.log10(1 + 1 / np.arange(1, 10)), index=range(1, 10))

fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.bar(actual.index, actual, color="tab:blue", label="Actual (manual entries)")
ax.plot(expected.index, expected, color="red", marker="o", label="Benford expected")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xticks(range(1, 10))
ax.set_xlabel("First digit")
ax.set_title("Benford's law: first digit of manual entry amounts")
ax.legend()
save(fig, "10_benford.png")

print(round(actual[9] * 100, 1), round(expected[9] * 100, 1))   # 11.8 4.6: more than twice as many 9s as expected
```

The excess of 9s comes from the entries split just below $10,000. Section 6 found the same pattern from a different angle.

## 11. Two y-axes

**Monthly JE count (bars) and value (line):**

```python
monthly = je[je["year"] == 2026].groupby("month").agg(count=("je_id", "size"), value=("amount", "sum"))

fig, ax1 = plt.subplots(figsize=(9, 4), layout="constrained")
ax1.bar(monthly.index, monthly["count"], color="lightgrey", label="Number of entries")
ax1.set_ylabel("Number of entries")

ax2 = ax1.twinx()                                    # second y-axis sharing the same x-axis
ax2.plot(monthly.index, monthly["value"], color="tab:blue", marker="o", label="Value")
ax2.yaxis.set_major_formatter(usd_k)
ax2.set_ylabel("Value")

ax1.set_xticks(range(1, 13), MONTHS)
fig.legend(loc="upper left", bbox_to_anchor=(0.08, 0.95))
ax1.set_title("FY2026 journal entries: volume and value")
save(fig, "11_twin_axis.png")
```

Use two y-axes carefully: the chart can suggest a relationship purely through how the two scales are set. Label both axes clearly.

## 12. Date axes and highlighted periods

**Daily posting value with quarter-ends highlighted:**

```python
daily = je[je["year"] == 2026].groupby("posting_date")["amount"].sum()

fig, ax = plt.subplots(figsize=(11, 4), layout="constrained")
ax.plot(daily.index, daily.values, linewidth=0.8)
for q_end in pd.to_datetime(["2026-03-31", "2026-06-30", "2026-09-30", "2026-12-31"]):
    ax.axvspan(q_end - pd.Timedelta(days=3), q_end + pd.Timedelta(days=1), color="orange", alpha=0.3)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.yaxis.set_major_formatter(usd_k)
ax.set_title("Daily posted value, FY2026 (quarter-ends shaded)")
save(fig, "12_daily_postings.png")

print(daily.idxmax().date(), round(daily.max() / 1e3))   # 2026-12-31 778: the year-end spike ($000s)
```

`mdates.MonthLocator()` puts one tick per month, and `DateFormatter("%b")` shows short month names. Other useful locators are `WeekdayLocator()` and `YearLocator()`.

## 13. Multi-chart dashboards

`plt.subplots(rows, cols)` makes a grid. `subplot_mosaic` lets you lay out named panels of different sizes:

```python
fig, axs = plt.subplot_mosaic([["trend", "trend"],
                               ["source", "hours"]],
                              figsize=(11, 7), layout="constrained")

axs["trend"].plot(revenue.index, revenue[2026], marker="o", label="FY2026")
axs["trend"].plot(revenue.index, revenue[2025], marker="o", color="grey", label="FY2025")
axs["trend"].set_xticks(range(1, 13), MONTHS)
axs["trend"].yaxis.set_major_formatter(usd_k)
axs["trend"].set_title("Revenue trend")
axs["trend"].legend()

cy["source"].value_counts().plot(kind="bar", ax=axs["source"], rot=0, color=["tab:blue", "tab:orange"])
axs["source"].set_title("Entries by source")

axs["hours"].hist(manual_cy["hour"], bins=range(25), color="tab:red")
axs["hours"].set_title("Manual entries by hour posted")

fig.suptitle("FY2026 general ledger overview", fontsize=14)
save(fig, "13_dashboard.png")
```

Use `sharex=True` or `sharey=True` in `plt.subplots()` when panels should use the same scale, so they can be compared fairly.

## 14. Formatting: currency, labels, styles and colours

**Number formatters:**

| Need | Code |
| --- | --- |
| `$125K` | `mtick.FuncFormatter(lambda x, _: f"${x/1e3:,.0f}K")` |
| `$1,250,000` | `mtick.StrMethodFormatter("${x:,.0f}")` |
| `25%` from 0.25 | `mtick.PercentFormatter(1.0)` |
| `1.25M` | `mtick.EngFormatter()` |

**Labels and text:**

```python
fig, ax = plt.subplots(figsize=(7, 3), layout="constrained")
ax.bar(MONTHS, revenue[2026], color="tab:blue")
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
ax.tick_params(axis="x", labelrotation=45)                  # rotate crowded labels
ax.text(0.01, 0.95, "Source: GL extract FY2026", transform=ax.transAxes, fontsize=8, va="top")
ax.spines[["top", "right"]].set_visible(False)              # cleaner look
ax.grid(axis="y", alpha=0.3)
save(fig, "14_formatting.png")
```

`transform=ax.transAxes` positions text relative to the chart (0 to 1) rather than the data, so a source note stays in the corner whatever the values are.

**Styles:** apply a whole look at once, for one chart or globally:

```python
print(len(plt.style.available) > 10)        # True: list the options with plt.style.available

with plt.style.context("ggplot"):           # applies only inside this block
    fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
    ax.plot(revenue.index, revenue[2026])
    save(fig, "14_style_ggplot.png")

plt.rcParams["font.size"] = 10              # global settings live in rcParams
```

**Colours:** use named colours (`"tab:blue"`), hex codes (`"#1f77b4"`) or colormaps. For data with a natural order, such as aging buckets or risk levels, use a *sequential* colormap like `"Blues"`. For data with a meaningful midpoint, such as variance against budget, use a *diverging* one like `"RdBu"`. The Matplotlib colormap guide recommends perceptually uniform maps like `"viridis"` and warns against rainbow maps like `"jet"`.

## 15. Saving charts for the audit file

```python
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
ax.plot(revenue.index, revenue[2026])
fig.savefig(CHARTS / "15_revenue.png", dpi=200, bbox_inches="tight")   # images for reports
fig.savefig(CHARTS / "15_revenue.pdf", bbox_inches="tight")            # sharp at any zoom, good for workpapers
fig.savefig(CHARTS / "15_revenue.svg", bbox_inches="tight")            # editable vector graphics
plt.close(fig)
```

- `dpi` controls image resolution: 150 to 200 suits most reports.
- `bbox_inches="tight"` trims empty margins.
- **Always close figures** in loops with `plt.close(fig)`. Matplotlib warns once more than 20 figures are open, and memory grows quickly when charting one figure per account or entity.

---

# Part 3: seaborn

## 16. How seaborn thinks

seaborn is built on Matplotlib. It works directly with pandas DataFrames, picks sensible statistics and colours, and splits data by a column with a single `hue=` argument.

**Three ideas from the seaborn documentation:**

1. **Long-form data:** one row per observation, with columns for each variable. A GL extract is already in this shape.
2. **Semantic mappings:** `hue=`, `size=`, `style=`, `col=` and `row=` map a column to colour, size, marker shape or separate panels.
3. **Axes-level vs figure-level functions:**

| Kind | Examples | Returns | Use when |
| --- | --- | --- | --- |
| Axes-level | `histplot`, `scatterplot`, `boxplot`, `heatmap`, `regplot` | A Matplotlib `Axes` | Placing a chart inside your own figure with `ax=` |
| Figure-level | `displot`, `relplot`, `catplot`, `lmplot`, `pairplot`, `jointplot` | A seaborn grid object | Splitting into panels with `col=` / `row=` |

```python
sns.set_theme(style="whitegrid", palette="colorblind")   # one line for a consistent look
```

## 17. Distributions

**Histogram by source, on a log scale:**

```python
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
sns.histplot(data=cy, x="amount", hue="source", log_scale=True, element="step",
             stat="density", common_norm=False, ax=ax)
ax.axvline(10_000, color="red", linestyle="--")
ax.set_title("JE amounts by source (each source scaled separately)")
save(fig, "17_histplot.png")
```

- `stat="density"` with `common_norm=False` scales each group on its own, so a small group of manual entries isn't dwarfed by thousands of automated ones.
- `kde=True` adds a smooth curve.
- `multiple="stack"` stacks groups instead of overlaying them.

**KDE and ECDF:**

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
sns.kdeplot(data=cy, x="amount", hue="source", log_scale=True, fill=True, common_norm=False, ax=ax1)
ax1.set_title("Smoothed distribution (KDE)")

sns.ecdfplot(data=cy, x="amount", hue="source", log_scale=True, ax=ax2)
ax2.axvline(10_000, color="red", linestyle="--")
ax2.set_title("Share of entries at or below each amount (ECDF)")
save(fig, "17_kde_ecdf.png")

print(round((cy.loc[cy["source"] == "Manual", "amount"] < 10_000).mean() * 100, 1))
# % of manual entries under the approval limit
```

An **ECDF** answers questions like "what share of entries fall below $10,000?" without any bin choices. It's often easier to read precisely than a histogram.

**Facets with the figure-level `displot`:**

```python
g = sns.displot(data=cy, x="amount", col="entity", log_scale=True, height=3, aspect=1.1)
g.set_titles("{col_name}")
g.figure.suptitle("JE amounts by entity", y=1.05)
g.savefig(CHARTS / "17_displot_entity.png", dpi=150, bbox_inches="tight")
plt.close(g.figure)
```

## 18. Categories: counts, totals and spreads

**Counts: manual entries by weekday:**

```python
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
fig, ax = plt.subplots(figsize=(8, 3.5), layout="constrained")
sns.countplot(data=manual_cy, x="weekday", order=order, color="tab:blue", ax=ax)
ax.set_title("FY2026 manual entries by weekday posted")
save(fig, "18_countplot_weekday.png")

print(manual_cy["weekday"].value_counts().reindex(order).fillna(0).astype(int).to_dict())
```

**Totals: expense by account, using `estimator="sum"`:**

```python
exp_cy = gl[(gl["fsli"] == "Operating Expenses") & (gl["year"] == 2026)]
fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
sns.barplot(data=exp_cy, y="account_name", x="amount", estimator="sum", errorbar=None,
            order=exp_cy.groupby("account_name")["amount"].sum().sort_values(ascending=False).index, ax=ax)
ax.xaxis.set_major_formatter(usd_k)
ax.set_title("FY2026 operating expenses by account")
save(fig, "18_barplot_sum.png")
```

`sns.barplot` shows the **mean** with a confidence interval by default. For ledger totals, always set `estimator="sum"` and `errorbar=None`. (`errorbar=` replaced the older `ci=` argument in seaborn 0.12.)

**Spreads: amounts by preparer, comparing box, violin and strip plots:**

```python
people = manual_cy[manual_cy["preparer"] != "CFO"]
fig, axs = plt.subplots(1, 3, figsize=(14, 4), layout="constrained", sharey=True)

sns.boxplot(data=people, x="preparer", y="amount", ax=axs[0], log_scale=True)
axs[0].set_title("Box: median, quartiles, outliers")

sns.violinplot(data=people, x="preparer", y="amount", ax=axs[1], log_scale=True, cut=0)
axs[1].set_title("Violin: full shape of the distribution")

sns.stripplot(data=people, x="preparer", y="amount", ax=axs[2], log_scale=True, alpha=0.5, jitter=0.25)
axs[2].axhline(10_000, color="red", linestyle="--")
axs[2].set_title("Strip: every entry as a dot")
save(fig, "18_spread_by_preparer.png")
```

The strip plot makes M. Gomez's band of entries just under $10,000 visible as a dense line of dots. Box plots summarise that detail away. `sns.swarmplot` is similar, but spreads the dots so none overlap. It works best with a few hundred points or fewer.

**`catplot`** is the figure-level version: `sns.catplot(data=..., x=..., y=..., kind="box", col="entity")`.

## 19. Heatmaps

**When are manual entries posted? Weekday × hour:**

```python
grid = (manual_cy.pivot_table(index="weekday", columns="hour", values="je_id", aggfunc="count", fill_value=0)
        .reindex(index=order, columns=range(24), fill_value=0))

fig, ax = plt.subplots(figsize=(12, 4), layout="constrained")
sns.heatmap(grid, cmap="Reds", linewidths=0.5, linecolor="white", cbar_kws={"label": "Entries"}, ax=ax)
ax.set_title("FY2026 manual entries: weekday × hour posted")
save(fig, "19_heatmap_weekday_hour.png")
```

**Preparer × month value, with numbers printed in each cell:**

```python
pm = manual_cy.pivot_table(index="preparer", columns="month", values="amount", aggfunc="sum", fill_value=0) / 1e3

fig, ax = plt.subplots(figsize=(12, 3.5), layout="constrained")
sns.heatmap(pm, annot=True, fmt=",.0f", cmap="Blues", cbar_kws={"label": "$000s"}, ax=ax)
ax.set_xticks(np.arange(12) + 0.5, MONTHS)
ax.set_title("Manual entry value by preparer and month ($000s)")
save(fig, "19_heatmap_preparer_month.png")
```

**Correlation between monthly account totals:**

```python
monthly_accts = (gl[gl["fsli"].isin(["Revenue", "Cost of Sales", "Operating Expenses", "Receivables"])]
                 .assign(period=lambda d: d["posting_date"].dt.to_period("M"))
                 .pivot_table(index="period", columns="fsli", values="amount", aggfunc="sum"))
corr = monthly_accts.corr()

fig, ax = plt.subplots(figsize=(5, 4), layout="constrained")
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, center=0, square=True, ax=ax)
ax.set_title("Correlation of monthly totals")
save(fig, "19_heatmap_corr.png")
```

Use a **diverging** map centred on 0 (`center=0`, `vmin=-1`, `vmax=1`) for correlations, so red and blue mean the same strength in each direction. Revenue (a credit) and cost of sales (a debit) correlate *negatively* here purely because of the sign convention. The December 2026 outlier also weakens the relationship, a reminder that a single month can distort a correlation.

## 20. Relationships and trends

**`lineplot` sums by month and splits by entity in one call:**

```python
rev_lines = gl[(gl["fsli"] == "Revenue") & (gl["year"] == 2026)].assign(revenue=lambda d: -d["amount"])

fig, ax = plt.subplots(figsize=(9, 4), layout="constrained")
sns.lineplot(data=rev_lines, x="month", y="revenue", hue="entity", estimator="sum",
             errorbar=None, marker="o", ax=ax)
ax.set_xticks(range(1, 13), MONTHS)
ax.yaxis.set_major_formatter(usd_k)
ax.set_title("FY2026 monthly revenue by entity")
save(fig, "20_lineplot_entity.png")
```

Without `estimator="sum"`, seaborn would plot the *average* revenue line amount per month, which is a very different chart.

**`scatterplot` with four encodings:**

```python
fig, ax = plt.subplots(figsize=(9, 4), layout="constrained")
sns.scatterplot(data=manual_cy, x="posted_at", y="amount", hue="preparer", style="is_weekend",
                size="amount", sizes=(15, 250), alpha=0.7, ax=ax)
ax.set_yscale("log")
ax.yaxis.set_major_formatter(usd_k)
ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)
ax.set_title("Manual entries through FY2026")
save(fig, "20_scatter_encodings.png")
```

The three large CFO entries on 31 December stand out at the right edge of the chart.

**`relplot`** is the figure-level version with facets: `sns.relplot(data=..., x=..., y=..., col="entity", kind="line")`.

## 21. Regression plots

Cost of goods sold (COGS) should move with product revenue. Fitting the line on the **prior year**, a period already audited, and then plotting the current year against it shows which months break the pattern. It's the same approach as the regression lecture's substantive analytical procedure:

```python
pairs = (gl[gl["account"].isin(["4000", "5000"])]
         .assign(period=lambda d: d["posting_date"].dt.to_period("M"))
         .pivot_table(index="period", columns="account_name", values="amount", aggfunc="sum")
         .rename(columns={"Product Revenue": "revenue", "Cost of Goods Sold": "cogs"}))
pairs["revenue"] = -pairs["revenue"]
py_pairs = pairs[pairs.index.year == 2025]
cy_pairs = pairs[pairs.index.year == 2026]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
ax1.scatter(cy_pairs["revenue"], cy_pairs["cogs"], color="tab:orange", label="FY2026 months", zorder=3)
sns.regplot(data=py_pairs, x="revenue", y="cogs", ci=95, truncate=False, ax=ax1,
            label="FY2025 months and fitted line")
dec = cy_pairs.loc["2026-12"]
ax1.annotate("Dec 2026: revenue up,\nCOGS not", (dec["revenue"], dec["cogs"]),
             xytext=(-170, 40), textcoords="offset points",
             arrowprops={"arrowstyle": "->", "color": "black"})
ax1.xaxis.set_major_locator(mtick.MaxNLocator(5))        # fewer ticks, so labels don't collide
ax1.xaxis.set_major_formatter(usd_k)
ax1.yaxis.set_major_formatter(usd_k)
ax1.set_title("Monthly COGS vs product revenue")
ax1.legend(loc="upper left", fontsize=8)

sns.residplot(data=py_pairs, x="revenue", y="cogs", ax=ax2)
ax2.xaxis.set_major_formatter(usd_k)
ax2.set_title("FY2025 residuals: random scatter, so a straight line fits")
save(fig, "21_regplot.png")

slope, intercept = np.polyfit(py_pairs["revenue"], py_pairs["cogs"], 1)
expected_cogs = slope * dec["revenue"] + intercept
print(round(slope, 2), round((dec["cogs"] - expected_cogs) / 1e3))
# 0.63 -407: FY2025 COGS ran at about 63% of revenue, and Dec 2026 COGS is ~$407K below that pattern
```

December 2026 sits far below the line: product revenue nearly doubled, but COGS barely moved. That's consistent with revenue recorded without any goods leaving inventory, such as the unsupported year-end manual entries. `regplot` keeps `ci=` for its confidence band. `sns.lmplot(..., hue=, col=)` is the figure-level version, which fits a separate line per group.

## 22. Multi-chart grids

**`pairplot`: every pair of monthly totals at once:**

```python
monthly_wide = monthly_accts.copy()
monthly_wide["Revenue"] = -monthly_wide["Revenue"]
monthly_wide["year"] = monthly_wide.index.year.astype(str)

g = sns.pairplot(monthly_wide, hue="year", corner=True, height=2)
g.savefig(CHARTS / "22_pairplot.png", dpi=120, bbox_inches="tight")
plt.close(g.figure)
```

`corner=True` drops the duplicate upper half of the grid.

**`jointplot`: one relationship plus each variable's own distribution:**

```python
g = sns.jointplot(data=manual_cy, x="hour", y="amount", kind="scatter", height=5,
                  marginal_kws={"bins": 24})
g.ax_joint.set_yscale("log")
g.savefig(CHARTS / "22_jointplot.png", dpi=120, bbox_inches="tight")
plt.close(g.figure)
```

**`FacetGrid`: any chart, repeated per group:**

```python
g = sns.FacetGrid(cy, col="entity", row="source", height=2.6, aspect=1.4, sharey=False)
g.map_dataframe(sns.histplot, x="amount", log_scale=True, bins=30)
g.set_titles("{row_name} | {col_name}")
g.savefig(CHARTS / "22_facetgrid.png", dpi=120, bbox_inches="tight")
plt.close(g.figure)
```

## 23. The seaborn objects interface

Since version 0.12, seaborn also has a newer, composable interface, `seaborn.objects`. A chart is built by adding layers:

```python
import seaborn.objects as so

plot = (
    so.Plot(rev_lines, x="month", y="revenue", color="entity")
    .add(so.Line(marker="o"), so.Agg("sum"))          # sum revenue per month and entity
    .label(title="FY2026 revenue by entity", x="Month", y="Revenue")
)
plot.save(CHARTS / "23_objects_interface.png", dpi=120, bbox_inches="tight")
```

The classic functions above remain fully supported. The objects interface is useful once you want to stack several layers, such as dots plus a trend line, on one chart.

## 24. Themes, palettes and mixing with Matplotlib

```python
sns.set_theme(style="ticks", context="notebook")   # style: darkgrid, whitegrid, dark, white, ticks
                                                   # context: paper, notebook, talk, poster (scales fonts)
print(sns.color_palette("colorblind").as_hex()[:3])   # a palette designed to be readable with colour-blindness

fig, ax = plt.subplots(figsize=(7, 3), layout="constrained")
sns.barplot(data=exp_cy, x="account_name", y="amount", estimator="sum", errorbar=None,
            hue="account_name", palette="Blues_d", legend=False, ax=ax)   # seaborn draws on our Matplotlib Axes...
ax.yaxis.set_major_formatter(usd_k)                                     # ...so every Matplotlib tool still works
sns.despine(ax=ax)                                                      # remove top and right borders
ax.set_title("Operating expenses, FY2026")
save(fig, "24_mixing.png")
```

**Palettes:**

| Data | Palette type | Examples |
| --- | --- | --- |
| Unordered categories (entities, sources) | Qualitative | `"colorblind"`, `"tab10"`, `"Set2"` |
| Ordered values (aging buckets, risk scores) | Sequential | `"Blues"`, `"rocket"`, `"mako"` |
| Values around a midpoint (variances, correlations) | Diverging | `"RdBu"`, `"vlag"`, `"coolwarm"` |

In seaborn 0.13, passing `palette=` without `hue=` raises a `FutureWarning`. Set `hue=` to the same column and add `legend=False`, as shown above.

---

# Part 4: Getting it right

## 25. Audit-ready chart checklist

A chart in an audit file is evidence, so it must be accurate, clear and reproducible.

- **Title says what and when:** "FY2026 manual JEs by preparer", not "Chart 3".
- **Units on every axis:** $, $000s, count or %.
- **Sign convention handled:** credits flipped where needed, and the method stated.
- **The y-axis starts at zero for bar charts.** A cut-off axis exaggerates differences. Line charts may zoom in, but say so.
- **The right statistic:** totals use `estimator="sum"`, not seaborn's default mean.
- **Population stated:** which entities, periods and sources are included, and any filters applied.
- **A source note:** the extract name and date, added with `ax.text(..., transform=ax.transAxes)`.
- **Readable colours:** a colour-blind-safe palette, with red and green not the only way meaning is shown.
- **Outliers kept:** never drop extreme values to tidy a chart. They are often the finding.
- **Reproducible:** the script and data extract are saved with the chart, so a reviewer can regenerate it.
- **Tied to the numbers:** totals on the chart agree to the trial balance.

## 26. Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| Nothing appears when running a script | No interactive display | Call `plt.show()`, or save with `fig.savefig()` |
| `NameError: name 'sns' is not defined` | Missing import | `import seaborn as sns` |
| Labels overlap or are cut off | Default spacing | `layout="constrained"`, `labelrotation=45`, `bbox_inches="tight"` |
| `RuntimeWarning: More than 20 figures have been opened` | Figures never closed | `plt.close(fig)` after saving |
| Bar chart shows averages, with error bars | seaborn's default estimator | `estimator="sum", errorbar=None` |
| `FutureWarning` about `palette` without `hue` | seaborn 0.13 change | Add `hue=` with `legend=False` |
| `TypeError` for `ci=` in `barplot` or `lineplot` | Replaced in seaborn 0.12 | Use `errorbar=None` or `errorbar=("ci", 95)` |
| `labels=` warning in `ax.boxplot` | Renamed in Matplotlib 3.9 | `tick_labels=` |
| `PendingDeprecationWarning: vert: bool will be deprecated` from `sns.boxplot` or `sns.violinplot` | seaborn 0.13.2 still uses an argument Matplotlib 3.10 plans to change | Harmless, and the chart is correct. It comes from inside seaborn, not your code |
| `Pandas4Warning: The copy keyword is deprecated` from `seaborn.objects` | seaborn 0.13.2 predates pandas 3.0 | Harmless. It will go away when seaborn is updated |
| Text between two `$` signs turns into italic maths, e.g. a title like "$8K to $12K" | Matplotlib reads `$...$` as math text | Escape with `\$`, or put `$` in only one place in the string |
| Revenue plotted as negative | Credits are stored as negatives | Multiply by -1 before plotting |
| A few huge entries squash everything else | Wide range of amounts | `ax.set_yscale("log")` or `log_scale=True` |
| Account codes plotted as numbers (4000.0) | Codes read as numbers | `dtype={"account": str}` when reading |
| Months in the wrong order | Sorted alphabetically | Use month numbers, or `order=` / `reindex()` |

## Sources

**Matplotlib documentation**

- [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html): figure anatomy, and explicit vs implicit interfaces
- [Axes and subplots](https://matplotlib.org/stable/users/explain/axes/index.html), [Subplot mosaic](https://matplotlib.org/stable/users/explain/axes/mosaic.html) and [Constrained layout guide](https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html)
- [Plot types gallery](https://matplotlib.org/stable/plot_types/index.html)
- [`Axes.bar_label`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar_label.html), [`Axes.boxplot`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html) and [`Axes.twinx`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.twinx.html)
- [Tick formatters](https://matplotlib.org/stable/gallery/ticks/tick-formatters.html) and [`matplotlib.dates`](https://matplotlib.org/stable/api/dates_api.html)
- [Choosing colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html) and the [Style sheets reference](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html)
- [`Figure.savefig`](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html)

**seaborn documentation**

- [User guide and tutorial](https://seaborn.pydata.org/tutorial.html), including the [overview of plotting functions](https://seaborn.pydata.org/tutorial/function_overview.html) (axes-level vs figure-level) and [data structures](https://seaborn.pydata.org/tutorial/data_structure.html) (long-form data)
- [Statistical estimation and error bars](https://seaborn.pydata.org/tutorial/error_bars.html), covering `errorbar=` replacing `ci=`
- [Choosing color palettes](https://seaborn.pydata.org/tutorial/color_palettes.html) and [Controlling figure aesthetics](https://seaborn.pydata.org/tutorial/aesthetics.html)
- [The seaborn.objects interface](https://seaborn.pydata.org/tutorial/objects_interface.html)
- [API reference](https://seaborn.pydata.org/api.html)

**pandas documentation**

- [Chart visualization](https://pandas.pydata.org/docs/user_guide/visualization.html): `DataFrame.plot`

**Audit analytics**

- Mark J. Nigrini, *Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection* (Wiley, 2012): expected first-digit frequencies, log₁₀(1 + 1/d)

**Verification:** every snippet was run in order against the file created by `make_gl_sample.py` on Matplotlib 3.10.8, seaborn 0.13.2, pandas 3.0.2 and Python 3.12, with warnings treated as errors. Printed values in comments are actual outputs.
