# 📝 Customer Feedback Analyzer (Gen AI)

A two-part AI app for a restaurant owner: paste or upload customer reviews, click **Analyze**, and instantly see how customers feel, what they talk about, and what to fix first.

> 📚 **Learning source:** [CodeBasics.io](https://codebasics.io)

- **Backend (FastAPI, `api.py`):** uses Google Gemini to analyze one review and return a `label`, `score`, `theme` and `suggestion`.
- **Frontend (Streamlit, `app.py`):** the dashboard the owner uses. It sends every review to the backend, shows a summary, and saves results to a SQLite database.

The frontend calls *your own* backend, just like calling any external API. You're on both sides of the API.

## ⚠️ Before you start: add your API key
This project ships with a **placeholder** instead of a real key. The backend can't analyze anything until you replace it.

1. Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey).
2. Copy `sample.env` to a new file named **`.env`** in the same folder.
3. Open `.env` and replace `your_google_api_key_here` with your real key:
   ```text
   GOOGLE_API_KEY=AIza...your-real-key...
   ```
4. Save. **Never upload `.env` to GitHub.** It's already listed in `.gitignore`.

## Install

Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run it (two terminals)

| Terminal 1: backend | Terminal 2: frontend |
|---|---|
| `uv run fastapi dev api.py` | `uv run streamlit run app.py` |
| stays running | opens in your browser |

Start the **backend first**. (With pip, drop `uv run` and activate `.venv` in both terminals.)

- Dashboard: http://localhost:8501
- Backend docs and test page: http://127.0.0.1:8000/docs

Then click **📄 Load sample reviews** and **🔍 Analyze**.

## Features
- **Three ways to add reviews:** paste them, load `sample_reviews.txt` with one click, or upload a `.txt` or `.csv` file (you pick the column)
- **Per-review analysis:** sentiment, a 1 to 5 score, a one-word theme, and a short improvement tip for negative or neutral reviews
- **Summary:** reviews analyzed, average score, % positive, % negative, top theme and top complaint
- **Charts:** reviews per theme and sentiment breakdown
- **🛠️ What to fix first:** improvement tips grouped by theme, most common problem first
- **Filters:** by sentiment, theme, or a text search
- **Progress bar** while a batch is analyzed, and clear reasons for any review that fails
- **Downloads:** results and history as CSV
- **Database:** save each batch (with an optional name and timestamp), browse the full history, see the average score over time, filter by batch, or delete everything
- **Backend status** in the sidebar, including a warning if the key is still the placeholder
- **Safe by default:** failed reviews never stop the batch and are never saved; batches are capped at 100 reviews to protect your quota

## Files

| File | Purpose |
|------|---------|
| `api.py` | FastAPI backend that calls Gemini |
| `app.py` | Streamlit dashboard |
| `database.py` | SQLite code: create, save, load, delete |
| `feedback_utils.py` | Helpers: reading files, summaries, filters, CSV export |
| `sample_reviews.txt` | 10 example reviews to try |
| `sample.env` | API key template with a **placeholder** (copy to `.env`) |
| `pyproject.toml` / `uv.lock` / `.python-version` | Project setup for `uv` |
| `requirements.txt` | Packages for `pip` |
| `.streamlit/config.toml` | Dashboard colors |
| `docs/` | How it works, quick reference, summary, key takeaways |

`feedback.db` is created automatically the first time you run the app. It's in `.gitignore`, so your saved reviews stay on your computer.

## What each lesson gave you

| Skill | Used here for |
|---|---|
| FastAPI + uv | The backend service |
| Pydantic + structured output | Clean input and output: `label`, `score`, `theme`, `suggestion` |
| Loops, lists, dicts | Going through many reviews and collecting results |
| SQLite database | Saving every analyzed review to `feedback.db` |
| Error handling | One bad review never crashes the whole batch |
| Calling APIs | The frontend calling the backend |
| Reading files | Loading the sample file and uploaded `.txt` / `.csv` files |
| Streamlit | The dashboard |

## Documentation
- [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md): setup, usage and troubleshooting
- [docs/HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md): step-by-step code walkthrough
- [docs/SUMMARY.md](docs/SUMMARY.md): project overview
- [docs/KEY_TAKEAWAYS.md](docs/KEY_TAKEAWAYS.md): what this project teaches

## Credits
Project idea and original course materials: [CodeBasics.io](https://codebasics.io).
