"""
Helper functions for the dashboard: reading reviews, summaries and exports.

Learning source: CodeBasics.io
No Streamlit code here, so everything can be tested on its own.
"""
import csv
import io
from collections import Counter

MAX_REVIEWS = 100          # per batch, to protect your Gemini quota
MAX_REVIEW_LENGTH = 2000   # must match the backend's limit
LABELS = ["positive", "neutral", "negative"]
LABEL_ICONS = {"positive": "🟢 positive", "neutral": "🟡 neutral", "negative": "🔴 negative", "error": "⚠️ error"}
REVIEW_COLUMN_HINTS = ("review", "text", "comment", "feedback", "message")


def parse_reviews_text(text: str) -> list[str]:
    """One review per line; blank lines and extra spaces are ignored."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def decode_upload(data: bytes) -> str:
    """Read an uploaded file's text (handles Excel's UTF-8 BOM and older Windows encodings)."""
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def csv_columns(text: str) -> list[str]:
    reader = csv.reader(io.StringIO(text))
    header = next(reader, [])
    return [h.strip() for h in header]


def guess_review_column(columns: list[str]) -> int:
    """Index of the column most likely to hold the reviews (0 if nothing obvious)."""
    for i, name in enumerate(columns):
        if any(hint in name.lower() for hint in REVIEW_COLUMN_HINTS):
            return i
    return 0


def reviews_from_csv(text: str, column: str) -> list[str]:
    reader = csv.DictReader(io.StringIO(text))
    reader.fieldnames = [f.strip() for f in (reader.fieldnames or [])]
    return [(row.get(column) or "").strip() for row in reader if (row.get(column) or "").strip()]


def prepare_batch(reviews: list[str]) -> tuple[list[str], list[str]]:
    """Trim long reviews and cap the batch size. Returns (reviews, notes for the user)."""
    notes = []
    too_long = sum(len(r) > MAX_REVIEW_LENGTH for r in reviews)
    if too_long:
        notes.append(f"{too_long} review(s) were longer than {MAX_REVIEW_LENGTH} characters and were shortened.")
    reviews = [r[:MAX_REVIEW_LENGTH] for r in reviews]
    if len(reviews) > MAX_REVIEWS:
        notes.append(f"Only the first {MAX_REVIEWS} of {len(reviews)} reviews will be analyzed in one batch.")
        reviews = reviews[:MAX_REVIEWS]
    return reviews, notes


def error_result(review: str, reason: str) -> dict:
    return {"review": review, "label": "error", "score": None, "theme": "", "suggestion": "", "error": reason}


def summarize(results: list[dict]) -> dict:
    """Numbers for the summary cards. Percentages and averages ignore failed rows."""
    ok = [r for r in results if r["label"] != "error"]
    labels = Counter(r["label"] for r in ok)
    themes = Counter(r["theme"] for r in ok if r.get("theme"))
    n = len(ok)
    return {
        "total": len(results),
        "analyzed": n,
        "errors": len(results) - n,
        "average_score": round(sum(r["score"] for r in ok) / n, 1) if n else None,
        "pct_positive": round(labels["positive"] / n * 100) if n else None,
        "pct_negative": round(labels["negative"] / n * 100) if n else None,
        "label_counts": {label: labels[label] for label in LABELS},
        "theme_counts": dict(themes.most_common()),
        "top_theme": themes.most_common(1)[0][0] if themes else None,
        "top_complaint": Counter(r["theme"] for r in ok if r["label"] == "negative").most_common(1)[0][0]
        if labels["negative"] else None,
    }


def action_items(results: list[dict]) -> list[dict]:
    """Suggestions from negative/neutral reviews, grouped by theme, most frequent problem first."""
    groups: dict[str, list[str]] = {}
    for r in results:
        if r["label"] in ("negative", "neutral") and r.get("suggestion"):
            groups.setdefault(r["theme"] or "other", []).append(r["suggestion"])
    items = [{"theme": t, "count": len(s), "suggestions": list(dict.fromkeys(s))} for t, s in groups.items()]
    return sorted(items, key=lambda i: -i["count"])


def filter_results(results, labels=None, themes=None, search=""):
    search = search.strip().lower()
    return [
        r for r in results
        if (not labels or r["label"] in labels)
        and (not themes or r["theme"] in themes)
        and (not search or search in r["review"].lower())
    ]


def to_csv(rows: list[dict], columns: list[str]) -> str:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()
