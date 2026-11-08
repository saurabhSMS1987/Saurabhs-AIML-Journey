"""
The frontend: a Streamlit dashboard for a business owner.

Learning source: CodeBasics.io

Paste or upload customer reviews, click Analyze, and see the results.
This app does NOT call Gemini directly. It calls OUR OWN backend (api.py).

Run it (terminal 2, while api.py is running in terminal 1):
    uv run streamlit run app.py
"""
import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

import feedback_utils as fu
from database import DB_FILE, delete_all, init_db, load_history, save_results

load_dotenv()
API_BASE = (os.getenv("FEEDBACK_API_URL") or "http://127.0.0.1:8000").rstrip("/")
SAMPLE_FILE = Path(__file__).parent / "sample_reviews.txt"

st.set_page_config(page_title="Customer Feedback Analyzer", page_icon="📝", layout="wide")
init_db()

for key, default in {"results": None, "saved": False, "reviews_text": ""}.items():
    st.session_state.setdefault(key, default)


# ---------------- Talking to our backend ----------------
def check_backend() -> tuple[bool, str, dict]:
    """(is it usable?, message, health info)."""
    try:
        info = requests.get(f"{API_BASE}/health", timeout=3).json()
    except Exception:
        return False, "Backend isn't running. Start it in another terminal: `uv run fastapi dev api.py`", {}
    if not info.get("api_key_configured"):
        return False, ("The backend is running, but `GOOGLE_API_KEY` in `.env` is missing or still the "
                       "placeholder. Add your real key and restart the backend."), info
    return True, f"Backend connected · model `{info.get('model')}`", info


def analyze_one(review: str) -> dict:
    """Ask our backend to analyze one review. Never raises: failures become 'error' rows."""
    try:
        response = requests.post(f"{API_BASE}/analyze", json={"text": review}, timeout=60)
    except requests.exceptions.RequestException:
        return fu.error_result(review, "Couldn't reach the backend.")
    if response.status_code != 200:
        try:
            detail = response.json().get("detail")
            reason = detail if isinstance(detail, str) else "The backend rejected this review."
        except ValueError:
            reason = f"Backend error (HTTP {response.status_code})."
        return fu.error_result(review, reason)
    data = response.json()
    return {"review": review, "label": data["label"], "score": data["score"], "theme": data["theme"],
            "suggestion": data.get("suggestion", ""), "error": ""}


def load_sample():
    st.session_state.reviews_text = SAMPLE_FILE.read_text(encoding="utf-8")


def clear_input():
    st.session_state.reviews_text = ""


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("🔌 Backend")
    backend_ok, backend_msg, _ = check_backend()
    (st.success if backend_ok else st.error)(backend_msg)
    st.caption(f"Address: `{API_BASE}`")
    if st.button("🔄 Check again", width="stretch"):
        st.rerun()
    st.divider()
    st.caption(f"Database: `{Path(DB_FILE).name}`")
    st.caption("📚 Learning source: [CodeBasics.io](https://codebasics.io)")

st.title("📝 Customer Feedback Analyzer")
st.caption("See how customers feel, what they talk about, and what to fix first.")

tab_analyze, tab_history = st.tabs(["🔍 Analyze reviews", "📚 Saved history"])

# =============== Analyze tab ===============
with tab_analyze:
    source = st.radio("Where are your reviews?", ["Paste text", "Upload a file"], horizontal=True)
    reviews: list[str] = []

    if source == "Paste text":
        b1, b2, _ = st.columns([1, 1, 3])
        b1.button("📄 Load sample reviews", on_click=load_sample, width="stretch")
        b2.button("🧹 Clear", on_click=clear_input, width="stretch")
        st.text_area("Reviews (one per line)", key="reviews_text", height=220,
                     placeholder="The food was great but delivery was slow.\nAmazing taste, will order again!")
        reviews = fu.parse_reviews_text(st.session_state.reviews_text)
    else:
        upload = st.file_uploader("Upload a .txt file (one review per line) or a .csv file", type=["txt", "csv"])
        if upload is not None:
            text = fu.decode_upload(upload.getvalue())
            if upload.name.lower().endswith(".csv"):
                columns = fu.csv_columns(text)
                if columns:
                    column = st.selectbox("Which column has the reviews?", columns,
                                          index=fu.guess_review_column(columns))
                    reviews = fu.reviews_from_csv(text, column)
                else:
                    st.warning("This CSV file looks empty.")
            else:
                reviews = fu.parse_reviews_text(text)

    reviews, notes = fu.prepare_batch(reviews)
    for note in notes:
        st.info(note)
    st.caption(f"{len(reviews)} review(s) ready.")
    batch_name = st.text_input("Batch name (optional, saved with the results)", placeholder="e.g. March reviews")

    if st.button("🔍 Analyze", type="primary", disabled=not reviews):
        if not backend_ok:
            st.error(backend_msg)
        else:
            results = []
            progress = st.progress(0.0, text="Starting…")
            for i, review in enumerate(reviews, start=1):
                progress.progress(i / len(reviews), text=f"Analyzing review {i} of {len(reviews)}…")
                results.append(analyze_one(review))
                # Stop early if the backend disappears mid-batch, instead of failing every review.
                if results[-1]["error"] == "Couldn't reach the backend.":
                    results += [fu.error_result(r, "Not analyzed: the backend stopped responding.") for r in reviews[i:]]
                    break
            progress.empty()
            st.session_state.results = results
            st.session_state.batch_name = batch_name
            st.session_state.saved = False

    results = st.session_state.results
    if results:
        summary = fu.summarize(results)
        st.divider()
        st.subheader("Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Reviews analyzed", f"{summary['analyzed']} / {summary['total']}")
        if summary["analyzed"]:
            c2.metric("Average score", f"{summary['average_score']} / 5")
            c3.metric("% Positive", f"{summary['pct_positive']}%")
            c4.metric("% Negative", f"{summary['pct_negative']}%")
            msg = f"Customers talk most about **{summary['top_theme']}**."
            if summary["top_complaint"]:
                msg += f" The most common complaint is about **{summary['top_complaint']}**."
            st.info(msg)
        if summary["errors"]:
            st.warning(f"{summary['errors']} review(s) couldn't be analyzed. See the **error** rows below for the reason.")

        if summary["analyzed"]:
            ch1, ch2 = st.columns(2)
            with ch1:
                st.markdown("**Reviews per theme**")
                st.bar_chart(pd.DataFrame({"reviews": summary["theme_counts"]}), horizontal=True)
            with ch2:
                st.markdown("**Sentiment**")
                st.bar_chart(pd.DataFrame({"reviews": summary["label_counts"]}))

            items = fu.action_items(results)
            if items:
                st.subheader("🛠️ What to fix first")
                for item in items:
                    with st.expander(f"**{item['theme']}** · {item['count']} review(s)", expanded=item is items[0]):
                        for s in item["suggestions"]:
                            st.markdown(f"- {s}")

        st.subheader("Results")
        f1, f2, f3 = st.columns(3)
        labels = f1.multiselect("Sentiment", fu.LABELS + (["error"] if summary["errors"] else []), key="filter_labels")
        themes = f2.multiselect("Theme", list(summary["theme_counts"]), key="filter_themes")
        search = f3.text_input("Search reviews", key="filter_search")
        shown = fu.filter_results(results, labels, themes, search)
        table = pd.DataFrame(shown, columns=["review", "label", "score", "theme", "suggestion", "error"])
        table["label"] = table["label"].map(fu.LABEL_ICONS)
        st.dataframe(
            table, hide_index=True, width="stretch",
            column_config={
                "review": st.column_config.TextColumn("Review", width="large"),
                "score": st.column_config.NumberColumn("Score", format="%d ⭐"),
                "suggestion": st.column_config.TextColumn("Suggestion", width="medium"),
                "error": st.column_config.TextColumn("Error", width="small"),
            },
        )
        st.caption(f"Showing {len(shown)} of {len(results)} reviews.")

        d1, d2 = st.columns(2)
        d1.download_button("⬇️ Download results (CSV)",
                           fu.to_csv(results, ["review", "label", "score", "theme", "suggestion", "error"]),
                           "feedback_results.csv", "text/csv", width="stretch")
        if d2.button("💾 Save to database", width="stretch", disabled=st.session_state.saved or not summary["analyzed"],
                     help="Already saved" if st.session_state.saved else "Error rows are not saved"):
            count = save_results(results, st.session_state.get("batch_name", ""))
            st.session_state.saved = True
            st.session_state.saved_count = count
            st.rerun()
        if st.session_state.saved:
            st.success(f"✅ Saved {st.session_state.get('saved_count', 0)} review(s) to "
                       f"{Path(DB_FILE).name}. Open **Saved history** to see everything.")

# =============== History tab ===============
with tab_history:
    history = load_history()
    if not history:
        st.write("Nothing saved yet. Analyze some reviews and click **Save to database**.")
    else:
        h = fu.summarize(history)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Saved reviews", h["total"])
        c2.metric("Average score", f"{h['average_score']} / 5")
        c3.metric("% Positive", f"{h['pct_positive']}%")
        c4.metric("Top complaint", h["top_complaint"] or "–")

        df = pd.DataFrame(history)
        dated = df.dropna(subset=["saved_at"]).copy()
        if not dated.empty:
            dated["date"] = pd.to_datetime(dated["saved_at"]).dt.date
            trend = dated.groupby("date")["score"].mean().round(2)
            if len(trend) > 1:
                st.markdown("**Average score over time**")
                st.line_chart(trend)

        batches = sorted(b for b in df["batch"].dropna().unique() if b)
        f1, f2, f3 = st.columns(3)
        pick_batches = f1.multiselect("Batch", batches, key="hist_batches") if batches else []
        pick_labels = f2.multiselect("Sentiment", fu.LABELS, key="hist_labels")
        search = f3.text_input("Search saved reviews", key="hist_search")
        rows = [r for r in fu.filter_results(history, pick_labels, None, search)
                if not pick_batches or r["batch"] in pick_batches]
        st.dataframe(
            pd.DataFrame(rows, columns=["saved_at", "batch", "review", "label", "score", "theme", "suggestion"]),
            hide_index=True, width="stretch",
            column_config={"review": st.column_config.TextColumn("Review", width="large"),
                           "score": st.column_config.NumberColumn("Score", format="%d ⭐")},
        )
        st.caption(f"Showing {len(rows)} of {len(history)} saved reviews.")
        st.download_button("⬇️ Download history (CSV)",
                           fu.to_csv(history, ["saved_at", "batch", "review", "label", "score", "theme", "suggestion"]),
                           "feedback_history.csv", "text/csv")

        with st.expander("🗑️ Delete all saved reviews"):
            st.warning("This permanently removes every saved review from the database.")
            if st.checkbox("I understand this can't be undone") and st.button("Delete everything", type="primary"):
                deleted = delete_all()
                st.success(f"Deleted {deleted} review(s).")
                st.rerun()
