# Customer Feedback Analyzer: Summary

📚 **Learning source:** [CodeBasics.io](https://codebasics.io)

## The problem
A restaurant owner has dozens of customer reviews and no time to read them all. They want a simple tool: paste the reviews, click a button, and instantly see how customers feel and what they keep complaining about.

## The solution
A two-part AI application:
- A **FastAPI backend** that uses Google Gemini to analyze one review and return structured results
- A **Streamlit dashboard** that sends every review to the backend, summarizes the results, and saves them to a **SQLite** database

This is the shape of most real AI products: a backend service that wraps the AI, and an interface that calls it.

## What it does
- Takes reviews pasted in, loaded from the sample file, or uploaded as `.txt` or `.csv`
- Gives each review a sentiment label, a 1 to 5 score, a one-word theme and, for complaints, a short improvement tip
- Summarizes the batch: average score, % positive and negative, top theme and top complaint
- Charts reviews per theme and the sentiment breakdown
- Groups improvement tips by theme under **What to fix first**
- Filters and searches the results, and exports them to CSV
- Saves batches to a database with a name and timestamp, and shows the full history with a score trend over time
- Shows backend status, explains every error, and never lets one bad review stop the batch

## Tech stack

| Tool | Used for |
|------|----------|
| Python 3.12 | Everything |
| FastAPI | Backend web service (`/analyze`, `/health`) |
| Google Gemini (`google-genai`) | Analyzing reviews with structured JSON output |
| Pydantic | Validating requests and responses |
| Streamlit | Dashboard |
| requests | Dashboard calling the backend |
| pandas | Tables and charts |
| SQLite | Saving reviews |
| python-dotenv | Loading the API key from `.env` |
| uv | Managing the environment and packages |

## Project structure

```
feedback_analyzer/
├── api.py                 # Backend
├── app.py                 # Dashboard
├── database.py            # SQLite
├── feedback_utils.py      # Helpers
├── sample_reviews.txt     # Example reviews
├── sample.env             # API key placeholder (copy to .env)
├── pyproject.toml
├── uv.lock
├── .python-version
├── requirements.txt
├── .gitignore
├── .streamlit/config.toml
└── docs/
    ├── HOW_IT_WORKS.md
    ├── QUICK_REFERENCE.md
    ├── SUMMARY.md
    └── KEY_TAKEAWAYS.md
```

## Quick start
```bash
cp sample.env .env              # then replace your_google_api_key_here with your real key
uv sync
uv run fastapi dev api.py       # terminal 1
uv run streamlit run app.py     # terminal 2
```

## Improvements over the original project

| Original | Now |
|----------|-----|
| Server crashed at start-up without a key | Starts anyway; `/health` and clear errors explain the problem |
| Hard-coded `gemini-2.5-flash` (since retired by Google) | Model set in `.env` (`GEMINI_MODEL`) |
| `label` could be any text; score unchecked | Label limited to 3 values; score kept within 1 to 5; theme cleaned to one word |
| Could return `None` if Gemini's answer didn't fit | Validated, with a clear 502 error otherwise |
| Failed reviews showed only "error" | Each failure shows its reason |
| % positive divided by all reviews, including errors | Percentages use successfully analyzed reviews only |
| Error rows saved to the database with score 0 | Error rows are never saved |
| Same batch could be saved repeatedly | Save is disabled once a batch is saved |
| No timeouts on requests | Timeouts, plus an early stop if the backend goes down |
| Paste only | Paste, load the sample file, or upload `.txt` / `.csv` |
| Summary and table only | Charts, top complaint, What to fix first, filters, search, CSV export |
| History list only | Batch names, timestamps, score trend, filters, export, delete |

The "Make it your own" ideas from the original course project are all built in: the theme chart, filtering to negative reviews, loading `sample_reviews.txt`, and the `suggestion` field.

## Possible next steps
- Analyze several reviews in one Gemini request to save time and tokens
- Detect the language of each review and translate before analyzing
- Draft a polite reply to each negative review
- Add login so several businesses can keep separate histories
- Deploy the backend and dashboard online (e.g. Render and Streamlit Community Cloud)
