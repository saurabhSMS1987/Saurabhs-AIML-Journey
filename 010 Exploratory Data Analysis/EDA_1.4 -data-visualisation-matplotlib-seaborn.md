# Data Visualisation with Matplotlib and Seaborn: Play Store Lecture + Audit Chart Gallery

*Nov 8, 2026 · Saurabh S*

> [!NOTE]
> **Source:** The lecture visuals come from the **EDA and Feature Engineering: Google Play Store Dataset** lecture from **Krish Naik Academy**. Function options are checked against the [seaborn](https://seaborn.pydata.org/api.html) and [Matplotlib](https://matplotlib.org/stable/api/index.html) documentation. All code was run on **seaborn 0.13.2, Matplotlib 3.10 and pandas 3.0**. The audit examples use simulated journal entry data.

## Where I started

My Play Store notes focused on cleaning the data. This document covers only the **charts**: how the lecture built them, what each line does, and how I'd use the same techniques on journal entry data. I wanted a single reference I can open whenever I need to turn a ledger into a picture for a workpaper or a client meeting.

---

# Part 1: The lecture's charts, explained

### 1. A grid of density plots for every numeric column

```python
plt.figure(figsize=(15, 15))
plt.suptitle("Univariate Analysis of Numerical Features", fontsize=20, fontweight="bold", alpha=0.8, y=1.)

for i in range(0, len(numeric_features)):
    plt.subplot(5, 3, i+1)
    sns.kdeplot(x=df_copy[numeric_features[i]], shade=True, color="r")
    plt.xlabel(numeric_features[i])
    plt.tight_layout()
```

| Piece | What it does |
| --- | --- |
| `plt.figure(figsize=(15, 15))` | Creates a blank canvas, 15 × 15 inches |
| `plt.suptitle(..., y=1.)` | Adds one title above **all** the charts. `y=1.` places it at the very top |
| `plt.subplot(5, 3, i+1)` | Picks cell number `i+1` in a grid of 5 rows × 3 columns. Subplot numbering starts at **1**, not 0 |
| `sns.kdeplot(..., shade=True)` | Draws a smooth density curve, filled in |
| `plt.tight_layout()` | Spaces the charts out so their labels don't overlap |

**What it showed:** Rating and Year are left-skewed, while Reviews, Size, Installs and Price are right-skewed, with long tails of very large values.

> [!TIP]
> On seaborn 0.13, `shade=True` gives a deprecation warning and will stop working in 0.14. Use `fill=True` instead.

### 2. Count plots for categorical columns

```python
plt.figure(figsize=(20, 15))
plt.suptitle("Univariate Analysis of Categorical Features", fontsize=20, fontweight="bold", alpha=0.8, y=1.)
category = ["Type", "Content Rating"]
for i in range(0, len(category)):
    plt.subplot(2, 2, i+1)
    sns.countplot(x=df[category[i]], palette="Set2")
    plt.xlabel(category[i])
    plt.xticks(rotation=45)
    plt.tight_layout()
```

`sns.countplot` counts how often each category appears and draws one bar per category. `palette="Set2"` picks a colour set, and `plt.xticks(rotation=45)` tilts long labels so they don't collide. **What it showed:** most apps are free, and most are rated "Everyone".

> [!TIP]
> Two notes for current versions. First, seaborn 0.13 warns when `palette` is used without `hue`. Write `sns.countplot(x=col, hue=col, palette="Set2", legend=False)` instead. Second, this cell plots `df`, the **raw** data, rather than the cleaned `df_copy`, so its counts include the duplicate apps.

### 3. A pie chart of category shares

```python
df_copy["Category"].value_counts().plot.pie(y=df_copy["Category"], figsize=(15, 16), autopct="%1.1f")
```

`.plot.pie()` is pandas' built-in plotting, which uses Matplotlib underneath. `autopct="%1.1f"` prints each slice's percentage to one decimal place. The `y=` argument only applies to DataFrames, so for a Series like this it has no effect.

**What it showed:** Family, Game and Tools have the most apps.

> [!TIP]
> With 33 categories, a pie chart is hard to read. Pies work best with **five slices or fewer**, and a sorted bar chart (the next example) is usually clearer.

### 4. A bar chart of the top 10 categories

```python
category = pd.DataFrame(df_copy["Category"].value_counts())
category.rename(columns={"Category": "Count"}, inplace=True)

plt.figure(figsize=(15, 6))
sns.barplot(x=category.index[:10], y="Count", data=category[:10], palette="hls")
plt.title("Top 10 App categories")
plt.xticks(rotation=90)
plt.show()
```

`category[:10]` keeps the first 10 rows, which are already sorted largest first. `plt.xticks(rotation=90)` turns the category names vertical.

> [!IMPORTANT]
> On pandas 2.0 and later, `value_counts()` names its result column **`count`**, not `Category`. The `rename` then does nothing, and `y="Count"` fails with *"Could not interpret value `Count`"*. I confirmed this on pandas 3.0. The fix is `df_copy["Category"].value_counts().rename_axis("Category").reset_index(name="Count")`.

### 5. Installs by category: a horizontal bar chart

```python
df_cat_installs = df_copy.groupby(["Category"])["Installs"].sum().sort_values(ascending=False).reset_index()
df_cat_installs.Installs = df_cat_installs.Installs / 1000000000      # convert to billions
df2 = df_cat_installs.head(10)
plt.figure(figsize=(14, 10))
sns.set_context("talk")
sns.set_style("darkgrid")

ax = sns.barplot(x="Installs", y="Category", data=df2)
ax.set_xlabel("No. of Installations in Billions")
ax.set_ylabel("")
ax.set_title("Most Popular Categories in Play Store", size=20)
```

| Piece | What it does |
| --- | --- |
| `groupby(...).sum().sort_values(...)` | Totals installs per category, largest first |
| `/ 1000000000` | Rescales to billions so the axis is readable |
| `x="Installs", y="Category"` | A numeric `x` with a text `y` makes the bars **horizontal**, which suits long labels |
| `sns.set_context("talk")` | Scales fonts and lines up for presentations (`paper` < `notebook` < `talk` < `poster`) |
| `sns.set_style("darkgrid")` | A grey background with a grid |
| `ax = ...`, then `ax.set_...` | Customises the specific chart through its **Axes** object |

> [!TIP]
> `set_context` and `set_style` change settings **globally**, so every chart drawn afterwards inherits them. That's why the next cell's `"poster"` setting carries over too. Either set the look once at the top of the notebook with `sns.set_theme(...)`, or use `with sns.axes_style("darkgrid"):` for a single chart.

### 6. The top 5 apps in each of four categories

```python
dfa = df_copy.groupby(["Category", "App"])["Installs"].sum().reset_index()
dfa = dfa.sort_values("Installs", ascending=False)
apps = ["GAME", "COMMUNICATION", "PRODUCTIVITY", "SOCIAL"]
sns.set_context("poster")
sns.set_style("darkgrid")

plt.figure(figsize=(40, 30))
for i, app in enumerate(apps):
    df2 = dfa[dfa.Category == app]
    df3 = df2.head(5)
    plt.subplot(4, 2, i+1)
    sns.barplot(data=df3, x="Installs", y="App")
    plt.xlabel("Installation in Millions")
    plt.ylabel("")
    plt.title(app, size=20)

plt.tight_layout()
plt.subplots_adjust(hspace=.3)
plt.show()
```

The loop filters to each category, keeps its 5 largest rows, and draws them in its own subplot. `plt.subplots_adjust(hspace=.3)` adds vertical space between the rows of charts. **What it showed:** Subway Surfers, Hangouts, Google Drive and Instagram lead their categories.

> [!TIP]
> Two small points. The installs aren't divided by a million here, so the "in Millions" axis label doesn't match the raw numbers. And a `4 × 2` grid for 4 charts leaves 4 empty spaces, where `2 × 2` would fit exactly.

### 7. Percentages as text

```python
for col in categorical_features:
    print(df[col].value_counts(normalize=True) * 100)
```

Not a chart, but the numbers behind one: `normalize=True` returns shares instead of counts, and `* 100` turns them into percentages.

---

# Part 2: The building blocks

| Concept | Lecture style | Recommended style | Why |
| --- | --- | --- | --- |
| Create charts | `plt.figure()` + `plt.subplot(r, c, i)` | `fig, axes = plt.subplots(r, c)` | Every chart gets its own named `ax`, which is clearer when there are several |
| Draw on a chart | Seaborn picks the "current" chart | `sns.barplot(..., ax=ax)` | No surprises about which chart gets drawn on |
| Titles and labels | `plt.title()`, `plt.xlabel()` | `ax.set_title()`, `ax.set_xlabel()` | Works the same for one chart or twenty |
| Overall title | `plt.suptitle()` | `fig.suptitle()` | |
| Spacing | `plt.tight_layout()` (inside the loop) | `fig.tight_layout()` (once, after the loop) | Only needs to run once, after everything is drawn |
| Look and feel | `sns.set_context()` + `sns.set_style()` | `sns.set_theme(style=..., context=...)` once | One place to change the whole look |
| Colours by category | `palette=...` alone | `hue=x, palette=..., legend=False` | Required from seaborn 0.14 |
| Values on bars | Not used | `ax.bar_label(container)` | Readers see exact numbers without reading the axis |
| Save | Not used | `fig.savefig("chart.png", dpi=120, bbox_inches="tight")` | `bbox_inches="tight"` stops titles being cut off |

---

# Part 3: Audit chart gallery: journal entries

The same chart types, applied to questions I actually ask about journal entries. The setup creates **3,000 simulated entries** for FY2026 across four entities, with a month-end posting spike, some Saturday-night manual postings and three large unapproved year-end revenue entries planted in it. Each example saves its chart as a PNG.

### Setup: the journal entry data

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="notebook")      # one global look, set once

rng = np.random.default_rng(26)
n = 3_000
accounts = {"4000": "Revenue", "1200": "Receivables", "5000": "Cost of sales", "6000": "Salaries",
            "6100": "Rent", "6200": "Travel", "6300": "Consulting", "2100": "Accruals",
            "1000": "Cash", "2000": "Payables", "1999": "Suspense", "7000": "Bank charges"}
days = pd.date_range("2026-01-01", "2026-12-31", freq="D")
day_weights = np.where(days.is_month_end, 8.0, np.where(days.dayofweek >= 5, 0.05, 1.0))   # month-end spike, quiet weekends
day_weights = day_weights / day_weights.sum()

je = pd.DataFrame({
    "je_id": [f"JE{i:05d}" for i in range(n)],
    "entity": rng.choice(["UK01", "US01", "IN01", "SG01"], n, p=[0.35, 0.30, 0.25, 0.10]),
    "account": rng.choice(list(accounts), n),
    "source": rng.choice(["Automated", "Manual"], n, p=[0.8, 0.2]),
    "preparer": rng.choice(["A. Rao", "M. Gomez", "J. Lee", "S. Patel"], n),
    "amount": rng.lognormal(8.2, 1.1, n).round(2),
    "approval_lag_hrs": rng.gamma(2.0, 6.0, n).round(1),
})
je["posted_at"] = (pd.to_datetime(rng.choice(days, n, p=day_weights))
                   + pd.to_timedelta(rng.integers(8, 19, n), unit="h")
                   + pd.to_timedelta(rng.integers(0, 60, n), unit="m"))
manual = je["source"] == "Manual"
late = manual & (rng.random(n) < 0.12)                       # some manual entries posted on Saturday nights
to_saturday = pd.to_timedelta((5 - je.loc[late, "posted_at"].dt.dayofweek) % 7, unit="D")
je.loc[late, "posted_at"] = je.loc[late, "posted_at"].dt.normalize() + to_saturday + pd.Timedelta(hours=23)
je["approver"] = np.where(manual, rng.choice(["K. Wong", "D. Smith", None], n, p=[0.47, 0.47, 0.06]), "SYSTEM")
je["account_name"] = je["account"].map(accounts)
je["status"] = np.where(je["approver"].isna(), "Unapproved", "Approved")

# planted issues: three large year-end manual revenue entries
big = je.sample(3, random_state=4).index
je.loc[big, ["account", "account_name", "source", "amount", "approver", "status", "entity"]] = \
    ["4000", "Revenue", "Manual", 250_000.0, None, "Unapproved", "UK01"]
je.loc[big, "posted_at"] = pd.Timestamp("2026-12-31 22:40")

je["hour"] = je["posted_at"].dt.hour
je["weekday"] = je["posted_at"].dt.day_name()
je["day_of_month"] = je["posted_at"].dt.day
je["month"] = je["posted_at"].dt.to_period("M").astype(str)
print(je.shape, je["source"].value_counts().to_dict())
```

### 1. Univariate grid: what do amounts and timings look like? (lecture chart 1)

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Journal entries: univariate view of numeric features", fontsize=16, fontweight="bold")

sns.kdeplot(data=je, x="amount", hue="source", log_scale=True, fill=True, common_norm=False, ax=axes[0, 0])
axes[0, 0].set_title("Amount (log scale): manual vs automated")

sns.histplot(data=je, x="hour", hue="source", multiple="stack", discrete=True, ax=axes[0, 1])
axes[0, 1].set_title("Posting hour")

sns.histplot(data=je, x="day_of_month", discrete=True, color="steelblue", ax=axes[1, 0])
axes[1, 0].set_title("Day of month posted")

sns.histplot(data=je, x="approval_lag_hrs", bins=30, kde=True, color="indianred", ax=axes[1, 1])
axes[1, 1].set_title("Hours from posting to approval")

fig.tight_layout()
fig.savefig("01_univariate_numeric.png", dpi=120, bbox_inches="tight")
plt.close(fig)
```

**What it shows:** amounts are right-skewed, so a **log scale** makes them readable, and `hue="source"` compares manual with automated entries on the same axes. The posting-hour chart shows a **separate cluster of manual entries at 23:00**. Day-of-month posting **spikes on days 30–31**, and the approval-lag chart has a long tail of slow approvals.

### 2. Count plots with exact numbers: what's in the population? (lecture chart 2)

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
fig.suptitle("Journal entries: categorical features", fontsize=16, fontweight="bold")

for ax, col in zip(axes, ["source", "status", "entity"]):
    order = je[col].value_counts().index
    sns.countplot(data=je, x=col, hue=col, order=order, palette="Set2", legend=False, ax=ax)
    for container in ax.containers:
        ax.bar_label(container, fmt="{:,.0f}")            # print the count on each bar
    ax.set_xlabel("")
    ax.set_title(col.title())

fig.tight_layout()
fig.savefig("02_categorical_counts.png", dpi=120, bbox_inches="tight")
plt.close(fig)
print(je["status"].value_counts().to_dict())
```

**What it shows:** 2,399 automated vs 601 manual entries, **37 unapproved**, and UK01 as the largest entity. `ax.bar_label()` prints each count, so a reviewer doesn't have to read it off the axis.

### 3. A pie chart, used where it works: two slices (lecture chart 3)

```python
share = je["source"].value_counts()
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(share, labels=share.index, autopct="%1.1f%%", startangle=90,
       colors=sns.color_palette("Set2"), wedgeprops={"edgecolor": "white"})
ax.set_title("Share of journal entries by source")
fig.savefig("03_source_pie.png", dpi=120, bbox_inches="tight")
plt.close(fig)
print((share / share.sum() * 100).round(1).to_dict())
```

**What it shows:** an 80% / 20% split between automated and manual entries. With only two categories, a pie chart is perfectly readable.

### 4. Top 10 accounts by manual entry value (lecture charts 4 and 5)

```python
top_accounts = (je[je["source"] == "Manual"]
                .groupby("account_name")["amount"].sum()
                .sort_values(ascending=False)
                .head(10)
                .div(1_000)                                   # show in thousands
                .reset_index())

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_accounts, x="amount", y="account_name", hue="account_name",
            palette="Blues_r", legend=False, ax=ax)
for container in ax.containers:                              # one container per bar when hue is used
    ax.bar_label(container, fmt="{:,.0f}K", padding=3)
ax.set_xlabel("Manual journal entry value (thousands)")
ax.set_ylabel("")
ax.set_title("Top 10 accounts by value of manual entries", fontsize=14)
fig.savefig("04_top_accounts_manual.png", dpi=120, bbox_inches="tight")
plt.close(fig)
print(top_accounts.head(3).round(0).to_dict("records"))
```

**What it shows:** **Revenue leads with about 941K** of manual postings, more than twice the next account (Payables, at 427K). That's driven by the three planted 250K year-end entries, and it's exactly the kind of pattern this chart is meant to surface. Note that **Suspense** also appears in the top 10.

### 5. The 5 largest manual entries per entity, with unapproved entries in red (lecture chart 6)

```python
entities = ["UK01", "US01", "IN01", "SG01"]
manual_je = je[je["source"] == "Manual"]

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
for ax, entity in zip(axes.flat, entities):
    top5 = manual_je[manual_je["entity"] == entity].nlargest(5, "amount")
    colors = ["indianred" if s == "Unapproved" else "steelblue" for s in top5["status"]]
    sns.barplot(data=top5, x="amount", y="je_id", hue="je_id", palette=colors, legend=False, ax=ax)
    ax.set_title(f"{entity}: 5 largest manual entries (red = unapproved)", fontsize=12)
    ax.set_xlabel("Amount")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(lambda x, pos: f"{x/1000:,.0f}K")
fig.tight_layout()
fig.subplots_adjust(hspace=0.35)
fig.savefig("05_top5_per_entity.png", dpi=120, bbox_inches="tight")
plt.close(fig)
print(manual_je[manual_je["entity"] == "UK01"].nlargest(3, "amount")[["je_id", "amount", "status"]].to_dict("records"))
```

**What it shows:** UK01's top three are the **250K unapproved year-end entries**, highlighted in red. The other entities' largest entries are all approved. Colouring by a status column adds a second dimension of information without another chart.

### 6. Heatmap: when are manual entries posted?

```python
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
grid = (je[je["source"] == "Manual"]
        .pivot_table(index="weekday", columns="hour", values="je_id", aggfunc="count", fill_value=0)
        .reindex(order))

fig, ax = plt.subplots(figsize=(12, 4.5))
sns.heatmap(grid, cmap="YlOrRd", annot=True, fmt="d", linewidths=0.5, cbar_kws={"label": "Manual entries"}, ax=ax)
ax.set_title("When are manual entries posted? (weekday × hour)", fontsize=14)
ax.set_xlabel("Hour of day")
ax.set_ylabel("")
fig.savefig("06_weekday_hour_heatmap.png", dpi=120, bbox_inches="tight")
plt.close(fig)
print(int(grid.loc["Saturday", 23]), "manual entries posted on Saturdays at 23:00")
```

**What it shows:** weekday daytime postings spread evenly, but **62 manual entries were posted on Saturdays at 23:00**, which stands out immediately in dark red. The lecture used a heatmap for correlations, and here the same function turns a timing test into one picture.

### 7. Trend line with highlights: month-end and year-end activity

```python
daily = je.set_index("posted_at").resample("D")["amount"].agg(["count", "sum"])
daily["is_month_end"] = daily.index.is_month_end

fig, ax = plt.subplots(figsize=(13, 4.5))
sns.lineplot(x=daily.index, y=daily["count"], color="grey", linewidth=1, ax=ax)
sns.scatterplot(x=daily.index[daily["is_month_end"]], y=daily.loc[daily["is_month_end"], "count"],
                color="crimson", s=60, zorder=3, label="Month-end", ax=ax)
ax.axvspan(pd.Timestamp("2026-12-24"), pd.Timestamp("2026-12-31"), color="orange", alpha=0.2, label="Year-end week")
ax.set_title("Daily journal entry volume: month-end spikes", fontsize=14)
ax.set_xlabel("")
ax.set_ylabel("Entries per day")
ax.legend()
fig.savefig("07_daily_volume.png", dpi=120, bbox_inches="tight")
plt.close(fig)
print(round(daily.loc[daily["is_month_end"], "count"].mean(), 1), "vs", round(daily.loc[~daily["is_month_end"], "count"].mean(), 1))
```

**What it shows:** about **67 entries on a typical month-end day vs about 6 on other days**, with month-ends marked in red and the year-end week shaded. `ax.axvspan()` shades a date range, which is a simple way to draw attention to a cut-off period.

---

## Which chart for which audit question?

| Audit question | Chart | Function |
| --- | --- | --- |
| What's the shape of amounts? Any extreme values? | Histogram or density, on a log scale | `sns.histplot`, `sns.kdeplot(log_scale=True)` |
| How is the population split by source, status or entity? | Count plot with labels | `sns.countplot` + `ax.bar_label` |
| What's the share of two or three groups? | Pie chart | `ax.pie(autopct=...)` |
| Which accounts or preparers carry the most value? | Sorted horizontal bar chart | `sns.barplot(x=value, y=label)` |
| What are the largest items in each entity? | A grid of bar charts | `plt.subplots(r, c)` + a loop |
| When are entries posted? | Heatmap of weekday × hour | `pivot_table` + `sns.heatmap` |
| Is there unusual period-end activity? | Line chart with shaded periods | `sns.lineplot` + `ax.axvspan` |

## My reflection

Working through the lecture's charts line by line showed me that most of the effort isn't the chart itself, but the **grouping and sorting before it**, plus the small finishing touches: a log scale, a rotated label, a number printed on a bar. Those are what turn a chart from "something drawn" into "something a reviewer can read in five seconds".

It was also a lesson in keeping code current. Three of the lecture's patterns (`shade=True`, a `palette` without `hue`, and the `value_counts()` column name) now warn or fail on current versions. For audit work, where the same script may be re-run next year, I'd rather write the version that will keep working.
