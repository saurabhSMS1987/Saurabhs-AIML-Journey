# Expense Tracker: Summary

A personal expense tracker built with **Python** and **Streamlit**. Log what you spend by category, date and currency, then see where your money goes, either overall or within any date range.

## What it does

- **Logs expenses** with a date, amount, currency, category and optional note
- **Supports custom categories** alongside ten built-in ones
- **Supports 11 currencies**, with a default you can set in the sidebar
- **Shows your top spending category** with totals, averages and each category's share
- **Analyzes any date range** using quick presets (last 7 days, this month, and more) or custom dates
- **Visualizes spending** with bar, donut, and daily stacked charts
- **Manages history**: view all entries, delete mistakes, and export to CSV
- **Saves data locally** in a SQLite file, so nothing leaves your computer

## Tech stack

| Tool | Used for |
|------|----------|
| Python | Application logic |
| Streamlit | Web interface |
| SQLite | Local data storage (built into Python) |
| pandas | Grouping and summarizing data |
| Plotly | Interactive charts |

## Project structure

```
expense_tracker/
├── app.py                 # Interface, analysis and charts
├── database.py            # Data storage and queries
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Color theme
└── docs/
    ├── HOW_IT_WORKS.md    # Step-by-step code walkthrough
    ├── QUICK_REFERENCE.md # How to run the app
    ├── SUMMARY.md         # This file
    └── KEY_TAKEAWAYS.md   # What this project teaches
```

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for full setup steps and troubleshooting.

## Design choices

- **One currency at a time in analysis.** Adding different currencies together would give a meaningless total without exchange rates, so each currency is analyzed separately.
- **Automatic database upgrades.** Databases from earlier versions gain new columns automatically, with no data lost.
- **Storage kept apart from the interface.** All SQL lives in `database.py`, and all UI code lives in `app.py`.

## Possible next steps

- Monthly budgets per category with alerts when you go over
- Currency conversion using live exchange rates, for a combined total
- Editing existing expenses, not just deleting them
- Recurring expenses such as rent and subscriptions
- Importing expenses from a bank statement CSV
