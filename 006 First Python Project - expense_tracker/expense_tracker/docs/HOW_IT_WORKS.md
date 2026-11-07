# How the Code Works: A Step-by-Step Guide

This guide walks through the Expense Tracker from the moment you launch it to the moment a chart appears on screen. The app is split into two Python files with separate jobs:

| File | Job |
|------|-----|
| `database.py` | Saves and loads expenses using SQLite. Knows nothing about the UI. |
| `app.py` | Draws the interface with Streamlit and turns data into charts. Never writes SQL. |

Keeping storage and interface apart means you could swap SQLite for another database, or Streamlit for another UI, without rewriting both.

---

## Step 1: Understand how Streamlit runs your script

Streamlit works differently from most UI frameworks. Every time you interact with the page (click a button, change a dropdown, pick a date), Streamlit **re-runs `app.py` from top to bottom**. Each widget call such as `st.selectbox(...)` both draws the widget and returns its current value.

That's why the code reads like a plain script with no event handlers: the values your widgets return on each run decide what gets shown.

## Step 2: Set up the page and the database

```python
st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")
db.init_db()
```

`init_db()` in `database.py` creates a file called `expenses.db` next to the code if it doesn't exist, with one table:

| Column | Type | Purpose |
|--------|------|---------|
| `id` | INTEGER | Unique number for each expense (assigned automatically) |
| `expense_date` | TEXT | Date stored as `YYYY-MM-DD` |
| `category` | TEXT | e.g. "Transport" |
| `amount` | REAL | Must be greater than 0 (enforced by a `CHECK` rule) |
| `currency` | TEXT | Code such as `INR` or `USD` |
| `note` | TEXT | Optional description |

Dates are stored as `YYYY-MM-DD` text on purpose: in that format, sorting the text alphabetically also sorts it by date, so SQL's `BETWEEN` works correctly for date ranges.

`init_db()` also handles **upgrades**. It checks whether the table already has a `currency` column (using `PRAGMA table_info`), and if it doesn't (from an older version of the app), it adds one with `ALTER TABLE`, filling old rows with the default currency. Existing data is never lost.

Because `CREATE TABLE IF NOT EXISTS` does nothing when the table already exists, it's safe to call `init_db()` on every re-run.

## Step 3: Read the default currency from the sidebar

```python
with st.sidebar:
    default_currency = st.selectbox("Default currency for new expenses", ...)
```

The value chosen here is used as the starting choice in the Add Expense form. It's stored in Streamlit's session state (via `key="default_currency"`), so it is remembered while the browser tab is open.

All currencies live in one dictionary in `database.py`:

```python
CURRENCIES = {"INR": ("₹", "Indian Rupee"), "USD": ("$", "US Dollar"), ...}
```

Helper functions in `app.py` read from it: `symbol()` gets the symbol, `money()` formats an amount like `₹1,250.00`, and `currency_label()` builds the dropdown text like `USD ($) · US Dollar`.

## Step 4: Create the four tabs

```python
tab_add, tab_history, tab_categories, tab_range = st.tabs([...])
```

Everything that follows is placed inside one of these tabs using `with tab_name:` blocks.

## Step 5: Log an expense (Add expense tab)

1. **Build the form.** The inputs sit inside `st.form(...)`. A form holds all its inputs back until you press the submit button, so the app doesn't re-run on every keystroke.
2. **Load categories.** `db.get_categories()` returns the ten built-in categories plus any custom ones you've used before, found by querying `SELECT DISTINCT category`.
3. **Allow a new category.** If you pick "➕ New category…", the app uses whatever you typed in the "New category name" box instead.
4. **Validate.** The app shows an error if the amount is zero or the new category name is empty.
5. **Save.** `db.add_expense(...)` runs an `INSERT` using `?` placeholders:

   ```python
   conn.execute("INSERT INTO expenses (...) VALUES (?, ?, ?, ?, ?)", (...))
   ```

   Placeholders let SQLite handle quoting safely, which prevents SQL injection and problems with text containing apostrophes.
6. **Confirm.** A success message shows exactly what was saved. `clear_on_submit=True` empties the form for the next entry.

## Step 6: View and manage expenses (History tab)

1. `db.get_expenses()` loads every expense into a **pandas DataFrame**, sorted newest first.
2. A display copy gets a formatted `Amount` column, so each row shows its own currency symbol.
3. A dropdown lists every expense; pressing **Delete** calls `db.delete_expense(id)` and then `st.rerun()` so the table refreshes immediately.
4. `st.download_button` exports everything as a CSV file.

## Step 7: Find your top spending category (By category tab)

1. **Pick a currency.** `pick_analysis_currency()` asks `db.get_used_currencies()` which currencies have data. If there's only one, it's chosen automatically; if there are several, a dropdown appears. Amounts in different currencies are never added together, since that would need exchange rates.
2. **Load that currency's expenses** with `db.get_expenses(currency=code)`.
3. **Summarize by category** in `category_summary()`:

   ```python
   df.groupby("category")["amount"].agg(Total="sum", Entries="count", Average="mean")
   ```

   This produces one row per category with its total, number of entries, and average. The rows are sorted so the biggest total comes first, and a `Share` column shows each category's percentage of all spending.
4. **Display it** in `show_category_breakdown()`:
   - Three metrics: total spent, highest category (the first row after sorting), and number of expenses
   - A horizontal bar chart and a donut chart, both made with Plotly
   - A table with a progress bar for each category's share

## Step 8: Analyze a date range (Date range analysis tab)

1. **Choose the range.** Quick options (last 7 days, last 30 days, this month, this year) are calculated with `timedelta`. "Custom" shows two date pickers.
2. **Check the dates.** If "From" is after "To", an error is shown instead of results.
3. **Filter in the database.** `db.get_expenses(start, end, currency=code)` builds its `WHERE` clause from whichever filters were given:

   ```sql
   WHERE expense_date BETWEEN ? AND ? AND currency = ?
   ```

   Filtering in SQL means only the needed rows are loaded.
4. **Reuse the same breakdown.** The filtered data goes through the same `show_category_breakdown()` function from Step 7, so both tabs look and behave the same.
5. **Show daily spending.** A stacked bar chart groups by both date and category, so you can see which days were expensive and why.
6. **Show the raw rows** inside an expandable section.

## Step 9: Theme

`.streamlit/config.toml` sets the colors (primary color, backgrounds, text). Streamlit reads this file automatically when the app starts; no code is needed.

---

## How data flows through the app

```
 You fill in the form
        │
        ▼
 app.py validates input ──► database.add_expense() ──► expenses.db
                                                          │
 You open an analysis tab                                 │
        │                                                 ▼
        ▼                                  database.get_expenses(filters)
 pick currency + date range ─────────────────────────────►│
                                                          ▼
                                                  pandas DataFrame
                                                          │
                                                          ▼
                                      category_summary() → groupby totals
                                                          │
                                                          ▼
                              show_category_breakdown() → metrics, charts, table
```
