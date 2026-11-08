# How the Code Works: A Step-by-Step Guide

📚 Learning source: [CodeBasics.io](https://codebasics.io)

The app has two programs that talk to each other over HTTP, plus two helper files:

| File | Job |
|------|-----|
| `api.py` | **Backend.** A FastAPI service with one main job: analyze one review with Gemini. |
| `app.py` | **Frontend.** The Streamlit dashboard. It never talks to Gemini directly; it calls the backend. |
| `database.py` | All SQLite work: create the table, save, load, delete. |
| `feedback_utils.py` | Plain Python helpers: reading files, summaries, filters, CSV export. No Streamlit code, so it's easy to test. |

```
 Browser ──► app.py (Streamlit) ──HTTP──► api.py (FastAPI) ──► Google Gemini
                  │
                  └──► database.py ──► feedback.db (SQLite)
```

Why split it? The backend keeps the API key and the AI logic in one place. Any other program (a mobile app, a script, another website) could use the same `/analyze` endpoint.

---

## Part 1: The backend (`api.py`)

### Step 1: Load settings without crashing

```python
load_dotenv()

def get_api_key():
    key = (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or "").strip()...
    return None if not key or key.lower() in PLACEHOLDER_KEYS else key
```

`load_dotenv()` reads `.env`. `get_api_key()` treats a missing key **or the placeholder** (`your_google_api_key_here`, or the original `<your google api key>`) as "no key".

The Gemini client is created **on first use** in `get_client()`, not at start-up. In the original version, `genai.Client()` ran at import, so a missing key crashed the server before it even started. Now the server always starts, and explains the problem instead.

The model comes from `GEMINI_MODEL` (default `gemini-3.6-flash`). The original hard-coded `gemini-2.5-flash`, which Google has since retired; now a retired model is a one-line change in `.env`.

### Step 2: Define the data shapes with Pydantic

```python
class Review(BaseModel):                 # what the caller SENDS
    text: str = Field(min_length=1, max_length=2000)

class GeminiAnalysis(BaseModel):         # what we ASK Gemini for
    label: Literal["positive", "negative", "neutral"]
    score: int
    theme: str
    suggestion: str

class Analysis(BaseModel):               # what we SEND BACK (checked)
    label: Literal["positive", "negative", "neutral"]
    score: int = Field(ge=1, le=5)
    theme: str
    suggestion: str
```

- `Review` rejects empty or very long text automatically. FastAPI returns a **422** error without running any code.
- `Literal[...]` restricts `label` to exactly three values. In the original, `label: str` allowed anything.
- There are two output models on purpose: `GeminiAnalysis` is kept simple so Gemini's schema support handles it reliably, and `Analysis` adds strict rules (`score` between 1 and 5) for what we return.
- `suggestion` is new: a short improvement tip for negative or neutral reviews. Keeping it to one short sentence keeps token use low.

### Step 3: The `/analyze` endpoint

```python
@app.post("/analyze", response_model=Analysis)
def analyze(review: Review):
    response = client.models.generate_content(
        model=get_model(),
        contents=PROMPT.format(text=text),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GeminiAnalysis,
        ),
    )
```

1. FastAPI turns the incoming JSON into a `Review` object (and rejects bad input).
2. The prompt explains each field; the schema forces Gemini to reply with matching JSON.
3. The answer is read from `response.parsed`, or validated from the raw text if needed. If it still doesn't fit, the endpoint returns **502** with a clear message instead of crashing. The original returned `response.parsed` directly, which could be `None`.
4. `clean_analysis()` makes the answer safe: it keeps the score within 1 to 5, turns the theme into one lowercase word (so "Delivery Time" becomes `delivery`, and themes group correctly), and clears the suggestion for positive reviews.

### Step 4: Turn Gemini errors into useful HTTP errors

`error_status()` maps problems to HTTP status codes and messages the dashboard can show:

| Problem | Status | Message |
|---------|--------|---------|
| Key missing or placeholder | 500 | "GOOGLE_API_KEY is missing or still the placeholder…" |
| Key rejected by Google | 401 | "Gemini rejected the API key…" |
| Model retired or wrong | 502 | "The model … isn't available…" |
| Rate limit or quota | 429 | "Gemini rate limit or quota reached…" |
| No internet | 503 | "The backend couldn't reach Gemini…" |
| Answer in the wrong format | 502 | "Gemini's answer wasn't in the expected format…" |

### Step 5: The `/health` endpoint

```python
@app.get("/health")
def health():
    return {"status": "ok", "model": get_model(), "api_key_configured": get_api_key() is not None}
```

A quick, free check (no Gemini call) that the dashboard uses to show whether the backend is running and set up.

---

## Part 2: The frontend (`app.py`)

### Step 6: Remember things across clicks

Streamlit re-runs the whole script on every click. Values that must survive go in `st.session_state`: the latest `results`, whether they've been `saved`, and the text box contents.

### Step 7: Check the backend

`check_backend()` calls `/health` (3-second timeout) on every run and shows the result in the sidebar: connected, not running, or running without a usable key. The **Analyze** button refuses to start if the backend isn't usable, so you get one clear message instead of a table full of errors.

### Step 8: Collect the reviews

| Source | How |
|--------|-----|
| Paste text | `parse_reviews_text()` splits by line and skips blank lines |
| Load sample reviews | A button callback reads `sample_reviews.txt` into the text box |
| `.txt` upload | Same as pasted text |
| `.csv` upload | `csv_columns()` reads the header, `guess_review_column()` picks a likely column (you can change it), and `reviews_from_csv()` reads that column |

`decode_upload()` handles files saved by Excel (UTF-8 with a hidden BOM) and older Windows encodings. `prepare_batch()` shortens reviews over 2,000 characters and caps a batch at 100 reviews, explaining both.

### Step 9: Analyze each review

```python
for i, review in enumerate(reviews, start=1):
    progress.progress(i / len(reviews), text=f"Analyzing review {i} of {len(reviews)}…")
    results.append(analyze_one(review))
```

`analyze_one()` posts one review to `/analyze` with a 60-second timeout, and **never raises**:
- On success it returns the label, score, theme and suggestion.
- On failure it returns an **error row** with the backend's own reason (e.g. "Gemini rate limit…"), so the owner knows what went wrong. The original recorded only "error".

If the backend stops responding mid-batch, the loop stops and marks the remaining reviews instead of waiting on each one.

### Step 10: Summarize and chart

`summarize()` in `feedback_utils.py` returns everything for the summary cards:
- Reviews analyzed vs. total
- Average score, % positive and % negative, calculated **only from successfully analyzed reviews**. The original divided by all reviews including errors, which understated the percentages.
- Counts per label and per theme (using `collections.Counter`), the top theme, and the top complaint (most common theme among negative reviews)

Two bar charts show reviews per theme and the sentiment breakdown.

### Step 11: What to fix first

`action_items()` collects the suggestions from negative and neutral reviews, groups them by theme, removes duplicates, and sorts the groups so the most common problem comes first.

### Step 12: Filter, download and save

- `filter_results()` applies the sentiment, theme and search filters to the table.
- **Download results (CSV)** uses `to_csv()`, which handles commas and quotes inside reviews.
- **Save to database** calls `save_results()` with the batch name. It's disabled after saving, so a batch can't be saved twice by accident; analyzing a new batch enables it again.

---

## Part 3: The database (`database.py`)

### Step 13: Create and upgrade the table

`init_db()` creates the `feedback` table if needed, then checks its columns with `PRAGMA table_info` and adds any that are missing (`suggestion`, `saved_at`, `batch`) with `ALTER TABLE`. A `feedback.db` made by the original app is upgraded automatically with all its rows kept.

The file is stored next to the code (not wherever the terminal happens to be), or wherever `FEEDBACK_DB` points.

### Step 14: Save, load and delete

- `save_results()` writes all rows in one `executemany()` call with a shared timestamp and batch name, and **skips error rows**. The original saved them with a score of 0, which dragged down every later average.
- `load_history()` returns rows as dictionaries, newest first.
- `delete_all()` empties the table (the dashboard asks for confirmation first).

Every function opens the connection with `closing(...)` and a transaction block, so connections are always closed and changes committed, even if something fails.

### Step 15: The history tab

The history tab reuses `summarize()` and `filter_results()` for its cards and filters, adds a **batch** filter, and draws **average score over time** (grouped by the day each batch was saved) once there are two or more days of data.

---

## A full request, start to finish

```
 1. Owner clicks Analyze
 2. app.py ── GET /health ──► api.py                 (is the backend ready?)
 3. for each review:
      app.py ── POST /analyze {"text": "..."} ──► api.py
      api.py ── prompt + GeminiAnalysis schema ──► Gemini
      Gemini ── JSON ──► api.py ── clean_analysis() ──► Analysis JSON ──► app.py
      (on any failure: an error row with the reason)
 4. summarize() → cards, charts, "What to fix first", table
 5. Save to database → save_results() → feedback.db
 6. Saved history → load_history() → cards, trend chart, filters
```
