# Quick Reference Guide: Customer Feedback Analyzer

📚 Learning source: [CodeBasics.io](https://codebasics.io)

## Requirements
- Python 3.12 or newer
- `uv` (recommended: `pip install uv`) or `pip`
- A Google Gemini API key (free tier available)
- An internet connection

## Step 1: Replace the API key placeholder ⚠️

| Step | macOS / Linux | Windows |
|------|---------------|---------|
| Copy the template | `cp sample.env .env` | `copy sample.env .env` |
| Edit it | Any text editor | Notepad or any editor |

In **`.env`**, change:
```text
GOOGLE_API_KEY=your_google_api_key_here
```
to your real key (from [Google AI Studio](https://aistudio.google.com/apikey)):
```text
GOOGLE_API_KEY=AIza...your-real-key...
```
No quotes or spaces needed. Save the file.

> 🔒 `.env` is in `.gitignore`, so it won't be uploaded. Never put your real key in `sample.env` or any `.py` file.

## Step 2: Install

| Option | Command |
|--------|---------|
| **uv** (recommended) | `uv sync` |
| **pip** | `python -m venv .venv`, activate it (`source .venv/bin/activate`, Windows: `.venv\Scripts\activate`), then `pip install -r requirements.txt` |

## Step 3: Run (two terminals)

| | Terminal 1: backend | Terminal 2: frontend |
|---|---|---|
| **uv** | `uv run fastapi dev api.py` | `uv run streamlit run app.py` |
| **pip** (with `.venv` active) | `fastapi dev api.py` | `streamlit run app.py` |
| Opens at | http://127.0.0.1:8000/docs | http://localhost:8501 |

Always start the **backend first** and leave it running. Stop either one with **Ctrl + C**.

**Quick backend test:** open http://127.0.0.1:8000/docs, expand **POST /analyze**, click **Try it out**, enter `{"text": "The food was cold"}` and click **Execute**.

## Using the dashboard

### Analyze reviews tab

| I want to… | Do this |
|------------|---------|
| Try it quickly | **📄 Load sample reviews** → **🔍 Analyze** |
| Paste my own reviews | Choose **Paste text**, one review per line |
| Use a file | Choose **Upload a file** → a `.txt` (one review per line) or `.csv` |
| Pick the CSV column | Use **Which column has the reviews?** (it guesses columns named review, text, comment, feedback or message) |
| Empty the text box | **🧹 Clear** |
| Label this batch | Type a **Batch name** before analyzing (e.g. "March reviews") |
| See only complaints | **Results** → **Sentiment** → `negative` |
| Find specific reviews | **Theme** filter or **Search reviews** |
| See what to improve | **🛠️ What to fix first** |
| Save results to my computer | **⬇️ Download results (CSV)** |
| Keep results in the database | **💾 Save to database** (once per batch) |

### Saved history tab

| I want to… | Do this |
|------------|---------|
| See all saved reviews | Open **📚 Saved history** |
| See if things are improving | **Average score over time** (appears once you've saved on two or more days) |
| Look at one batch | **Batch** filter |
| Export everything | **⬇️ Download history (CSV)** |
| Start fresh | **🗑️ Delete all saved reviews** → tick the box → **Delete everything** |

### Sidebar
Shows whether the backend is connected and which model it uses. Click **🔄 Check again** after starting the backend.

## What the results mean

| Column | Meaning |
|--------|---------|
| `label` | 🟢 positive, 🟡 neutral, 🔴 negative, or ⚠️ error |
| `score` | 1 (very bad) to 5 (very good) |
| `theme` | One word for the main topic, e.g. `delivery`, `taste`, `price` |
| `suggestion` | A short improvement tip (only for negative and neutral reviews) |
| `error` | Why a review couldn't be analyzed |

Averages and percentages only count reviews that were analyzed successfully. Error rows are never saved to the database.

## Limits
- Up to **100 reviews** per batch (extra ones are skipped, with a note)
- Up to **2,000 characters** per review (longer ones are shortened, with a note)

## Settings in `.env`

| Setting | Purpose | Default |
|---------|---------|---------|
| `GOOGLE_API_KEY` | Your Gemini API key (required) | `your_google_api_key_here` (placeholder) |
| `GEMINI_MODEL` | Model the backend uses | `gemini-3.6-flash` |
| `FEEDBACK_API_URL` | Where the dashboard finds the backend | `http://127.0.0.1:8000` |

Restart the backend after changing `.env`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Sidebar: "Backend isn't running" | Start it in another terminal: `uv run fastapi dev api.py`, then **🔄 Check again** |
| Sidebar: key "missing or still the placeholder" | Copy `sample.env` to `.env`, add your real key, restart the backend |
| Error rows: "rejected the API key" | Re-copy the full key from AI Studio into `.env`; restart the backend |
| Error rows: "model … isn't available" | Google retired the model. Set a current one in `GEMINI_MODEL`; restart the backend |
| Error rows: "rate limit or quota" | Wait a minute, then analyze a smaller batch |
| Error rows: "backend stopped responding" | The backend closed mid-batch. Restart it and analyze again |
| **Analyze** is greyed out | Add at least one review first |
| **Save to database** is greyed out | This batch is already saved, or every review failed |
| Port 8000 already in use | Stop the other program, or run `uv run fastapi dev api.py --port 8001` and set `FEEDBACK_API_URL=http://127.0.0.1:8001` in `.env` |
| CSV shows strange characters | Save the CSV as "CSV UTF-8" in Excel and upload again |
| `uv: command not found` | `pip install uv`, or use the pip instructions |
| Windows shows `sample` instead of `sample.env` | Explorer may hide extensions; it's the same file |

## Customize

| Change | Where |
|--------|-------|
| What Gemini is asked | `PROMPT` in `api.py` |
| Fields returned per review | `GeminiAnalysis` and `Analysis` in `api.py` (and the result dict in `app.py`) |
| Batch and length limits | `MAX_REVIEWS`, `MAX_REVIEW_LENGTH` in `feedback_utils.py` (and `api.py`) |
| CSV column guesses | `REVIEW_COLUMN_HINTS` in `feedback_utils.py` |
| Database location | `FEEDBACK_DB` environment variable, or `DB_FILE` in `database.py` |
| Dashboard colors | `.streamlit/config.toml` |
