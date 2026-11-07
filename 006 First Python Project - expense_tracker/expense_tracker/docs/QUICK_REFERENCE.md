# Quick Reference Guide: Running the Expense Tracker

## Requirements
- Python 3.10 or newer
- pip (comes with Python)

## First-time setup

| Step | macOS / Linux | Windows |
|------|---------------|---------|
| 1. Go to the project folder | `cd expense_tracker` | `cd expense_tracker` |
| 2. Create a virtual environment | `python3 -m venv venv` | `python -m venv venv` |
| 3. Activate it | `source venv/bin/activate` | `venv\Scripts\activate` |
| 4. Install packages | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| 5. Start the app | `streamlit run app.py` | `streamlit run app.py` |

The app opens automatically at **http://localhost:8501**.

## Every time after that

```bash
cd expense_tracker
source venv/bin/activate        # Windows: venv\Scripts\activate
streamlit run app.py
```

## Stop the app
Press **Ctrl + C** in the terminal.

## Required folder layout

```
expense_tracker/
├── app.py
├── database.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

`expenses.db` is created automatically on first run.

## Using the app

| I want to… | Go to |
|------------|-------|
| Set my usual currency | Sidebar → **Default currency for new expenses** |
| Log an expense | **➕ Add expense** tab → fill in → **Save expense** |
| Add a custom category | Category → **➕ New category…** → type the name |
| See or delete past expenses | **📋 History** tab |
| Export my data | **📋 History** → **Download as CSV** |
| See my top spending category | **📊 By category** tab |
| Analyze a time period | **📅 Date range analysis** → pick a range |

## Useful commands

| Task | Command |
|------|---------|
| Use a different port | `streamlit run app.py --server.port 8502` |
| Run without opening a browser | `streamlit run app.py --server.headless true` |
| Back up your data | Copy `expenses.db` somewhere safe |
| Start fresh (deletes all data) | Delete `expenses.db` |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `streamlit: command not found` | Activate the virtual environment, or run `python -m streamlit run app.py` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` with the environment active |
| `Port 8501 is already in use` | Close the other app, or use `--server.port 8502` |
| Theme colors not applied | Make sure `config.toml` is inside a folder named `.streamlit` |
| Error about `width` argument | Upgrade Streamlit: `pip install -U streamlit` (needs 1.50 or newer) |

## Customize

| Change | Where |
|--------|-------|
| Add a currency | `CURRENCIES` in `database.py` |
| Change the default currency | `DEFAULT_CURRENCY` in `database.py` |
| Edit the built-in categories | `DEFAULT_CATEGORIES` in `database.py` |
| Change chart colors | `CHART_COLORS` in `app.py` |
| Change the theme | `.streamlit/config.toml` |
