# Expense Tracker (Streamlit)

Log expenses by category and date, see which category you spend the most on,
and analyze spending within any date range.

## Files
- `app.py` – the Streamlit app (UI and charts)
- `database.py` – SQLite storage (creates `expenses.db` automatically)
- `requirements.txt` – Python dependencies
- `.streamlit/config.toml` – color theme

## Run it
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501.

## Features
- **Add expense:** date, amount, currency, category (or a new custom one), optional note
- **History:** see all entries, delete mistakes, download as CSV
- **By category:** totals, top category, bar and pie charts (all time)
- **Date range analysis:** quick ranges or custom dates, category breakdown and daily chart

## Currencies
Each expense stores its own currency. Set your usual one under **Settings** in the sidebar
so new expenses start with it. Since amounts in different currencies can't be added together
directly, the analysis tabs let you choose which currency to analyze.

To add more currencies, extend the `CURRENCIES` dictionary in `database.py`.

If you used the earlier version, your existing `expenses.db` is upgraded automatically and
old entries are marked as INR.
