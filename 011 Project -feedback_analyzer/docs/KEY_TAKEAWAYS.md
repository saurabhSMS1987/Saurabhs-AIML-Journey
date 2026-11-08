# Key Takeaways

📚 Learning source: [CodeBasics.io](https://codebasics.io)

## 1. Real AI apps have a backend and a frontend
The backend (`api.py`) owns the API key and the AI logic. The frontend (`app.py`) only calls `/analyze`. Swap "analyze a review" for "summarize a document" or "tag a support ticket" and the structure stays the same.

## 2. Pydantic guards both doors
`Review` checks what comes **in** (non-empty, not too long). `Analysis` checks what goes **out** (a known label, a score from 1 to 5). FastAPI applies both automatically and documents them at `/docs`.

## 3. Structured output turns text into data
Passing a schema with `response_mime_type="application/json"` makes Gemini reply with fields your code can count, average and chart, instead of free text you'd have to read.

## 4. Don't fully trust the model; clean its answer
Even with a schema, a model might return a score of 9 or a theme like "Delivery Time". `clean_analysis()` clamps the score and reduces the theme to one lowercase word, so themes group correctly in charts.

## 5. Use `Literal` for fixed choices
`label: Literal["positive", "negative", "neutral"]` is stricter and clearer than `label: str`. The allowed values are also sent to Gemini as part of the schema.

## 6. Start up safely and report problems
Creating the Gemini client on first use, rather than at import, lets the server start without a key and explain what's missing through `/health` and clear error messages.

## 7. Errors should carry reasons
Returning the right HTTP status (401, 429, 502…) with a plain-language `detail` lets the dashboard show *why* a review failed, not just that it did.

## 8. One failure must not stop the batch
Each review is handled independently, and `analyze_one()` never raises. If the backend disappears entirely, the loop stops early instead of waiting on every remaining review.

## 9. Bad data spreads; keep it out
The original saved failed reviews with a score of 0, which quietly lowered every future average. Skipping error rows when saving, and excluding them from percentages, keeps the numbers honest.

## 10. Databases change; upgrade them in place
Checking existing columns with `PRAGMA table_info` and adding new ones with `ALTER TABLE` means users of the old version keep their data when they update.

## 11. Always close connections and set timeouts
`closing(...)` with a transaction block guarantees every SQLite connection is closed and committed. `timeout=` on every `requests` call means a stuck backend can't freeze the dashboard.

## 12. Split code by job
`api.py` is about the AI, `app.py` about the screen, `database.py` about storage, and `feedback_utils.py` about data handling. Each file is shorter, easier to read and easier to test.

## 13. Keep secrets and personal data out of Git
`sample.env` holds a placeholder; the real key lives in `.env`. Both `.env` and `feedback.db` (customer reviews) are in `.gitignore`.

## 14. Settings belong in configuration, not code
The model name and backend address come from `.env`. When Google retires a model, or the backend moves, nothing in the code has to change.

## 15. Test the whole chain without spending quota
The backend was tested with the real Gemini library and a fake network layer, which also checks that the request and schema are built correctly. The dashboard was tested with Streamlit's `AppTest`, calling the real backend code with a stand-in for Gemini. Together they covered the full path from click to database, plus the error cases.
