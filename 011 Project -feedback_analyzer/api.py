"""
The backend: a small FastAPI service that analyzes customer reviews with Gemini.

Learning source: CodeBasics.io

Run it (terminal 1, leave it running):
    uv run fastapi dev api.py

Interactive docs: http://127.0.0.1:8000/docs
"""
import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

DEFAULT_MODEL = "gemini-3.6-flash"
PLACEHOLDER_KEYS = {"your_google_api_key_here", "<your google api key>", "your_key_here", "your-api-key-here"}
MAX_REVIEW_LENGTH = 2000

app = FastAPI(
    title="Customer Feedback Analyzer API",
    description="Analyzes one customer review at a time with Google Gemini. Learning source: CodeBasics.io",
    version="1.0.0",
)


# ---------------- Settings ----------------
def get_api_key() -> str | None:
    """The key from .env, or None if it's missing or still the placeholder."""
    key = (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or "").strip().strip('"').strip("'")
    return None if not key or key.lower() in PLACEHOLDER_KEYS else key


def get_model() -> str:
    return os.getenv("GEMINI_MODEL", "").strip() or DEFAULT_MODEL


_client: genai.Client | None = None


def get_client() -> genai.Client:
    """Create the Gemini client on first use, so the server can start (and report problems) without a key."""
    global _client
    key = get_api_key()
    if key is None:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY is missing or still the placeholder. Put your real key in the .env file and restart the backend.",
        )
    if _client is None:
        _client = genai.Client(api_key=key)
    return _client


# ---------------- Data shapes ----------------
# What the caller must SEND us
class Review(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_REVIEW_LENGTH, description="One customer review")


# What we ask Gemini for. Kept small on purpose -> fewer tokens used.
class GeminiAnalysis(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    score: int
    theme: str
    suggestion: str


# What we SEND back to the caller (checked and cleaned)
class Analysis(BaseModel):
    label: Literal["positive", "negative", "neutral"] = Field(description="Overall feeling of the review")
    score: int = Field(ge=1, le=5, description="1 (very bad) to 5 (very good)")
    theme: str = Field(description="One lowercase word for the main topic, e.g. 'delivery'")
    suggestion: str = Field(description="One short tip for the business; empty for positive reviews")


PROMPT = (
    "Analyze this customer review for a restaurant business.\n"
    "label must be 'positive', 'negative', or 'neutral'.\n"
    "score must be a whole number from 1 (very bad) to 5 (very good).\n"
    "theme must be ONE lowercase word for the main topic "
    "(for example: delivery, taste, price, service, quality, app, portion).\n"
    "suggestion: if the review is negative or neutral, ONE short sentence (max 15 words) on how "
    "the business could improve. If it is positive, return an empty string.\n"
    "Review: {text}"
)


def clean_analysis(raw: GeminiAnalysis) -> Analysis:
    """Make the model's answer safe to use: score within 1-5, theme a single lowercase word."""
    theme = (raw.theme or "").strip().lower().split()
    theme = "".join(ch for ch in (theme[0] if theme else "other") if ch.isalnum() or ch == "-") or "other"
    suggestion = "" if raw.label == "positive" else (raw.suggestion or "").strip()
    return Analysis(label=raw.label, score=min(5, max(1, int(raw.score))), theme=theme, suggestion=suggestion)


def error_status(error: Exception) -> tuple[int, str]:
    """Turn a Gemini error into an HTTP status and a message the frontend can show."""
    code = getattr(error, "code", None)
    message = str(getattr(error, "message", "") or error)
    if "api key" in message.lower() and any(w in message.lower() for w in ("not valid", "invalid", "expired")):
        return 401, "Gemini rejected the API key. Check GOOGLE_API_KEY in .env and restart the backend."
    if code == 404:
        return 502, f"The model '{get_model()}' isn't available. Set a current model in GEMINI_MODEL in .env."
    if code == 429:
        return 429, "Gemini rate limit or quota reached. Wait a minute and try again."
    if any(w in type(error).__name__ for w in ("Connect", "Timeout", "Network")):
        return 503, "The backend couldn't reach Gemini. Check the internet connection."
    return 502, f"Gemini error: {message[:300]}"


# ---------------- Endpoints ----------------
@app.get("/health")
def health():
    """Lets the dashboard check that the backend is running and set up."""
    return {"status": "ok", "model": get_model(), "api_key_configured": get_api_key() is not None}


@app.post("/analyze", response_model=Analysis)
def analyze(review: Review):
    text = review.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="The review is empty.")
    client = get_client()
    try:
        response = client.models.generate_content(
            model=get_model(),
            contents=PROMPT.format(text=text),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeminiAnalysis,
            ),
        )
    except Exception as e:
        status, detail = error_status(e)
        raise HTTPException(status_code=status, detail=detail)

    try:
        raw = response.parsed if isinstance(response.parsed, GeminiAnalysis) else GeminiAnalysis.model_validate_json(response.text or "")
    except Exception:
        raise HTTPException(status_code=502, detail="Gemini's answer wasn't in the expected format. Try again.")
    return clean_analysis(raw)
