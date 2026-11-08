"""Shared pieces for the AI Travel Assistant app: schema, prompts and helpers.

Learning source: CodeBasics.io (Python for AI course).
No Streamlit code here, so everything can be tested on its own.
"""
from typing import List

from pydantic import BaseModel, Field

PLACEHOLDER_KEYS = {"your_actual_api_key_here", "your-api-key-here"}
DEFAULT_MODEL = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = (
    "You are a friendly travel assistant for a booking platform. Help the user plan a trip. "
    "Find out their destination, how many days they have, their budget (Low, Medium or High) "
    "and what they enjoy. Ask about anything that's missing, one or two questions at a time. "
    "Keep replies short and practical. When you have enough details, tell the user they can "
    "generate their final itinerary."
)

FINAL_REQUEST = (
    "Based strictly on the preferences I shared in this conversation, create my complete travel "
    "itinerary. Fill in every field: destination (city and country), duration_days as a whole "
    "number, budget_category (Low, Medium or High), 3 to 5 activities, and a daily_itinerary with "
    "one entry for every day of the trip. If I didn't mention something, choose a sensible default."
)


# ---------------- Pydantic schema ----------------
class DailyPlan(BaseModel):
    day: int = Field(description="The day number, e.g., 1")
    plan: str = Field(description="A detailed paragraph of the itinerary for this day")


class TravelItinerary(BaseModel):
    destination: str = Field(description="The destination city and country, e.g., 'Kyoto, Japan'")
    duration_days: int = Field(description="Strictly the integer number of days, e.g., 4")
    budget_category: str = Field(description="The budget level: Low, Medium, or High")
    activities: List[str] = Field(description="A list of 3 to 5 core activities or themes")
    daily_itinerary: List[DailyPlan] = Field(description="A list containing the detailed plan for each day")


# ---------------- API key ----------------
def clean_key(value: str | None) -> str | None:
    """Return the key, or None if it's empty or still a placeholder."""
    if not value:
        return None
    value = value.strip().strip('"').strip("'")
    return None if not value or value in PLACEHOLDER_KEYS else value


def is_placeholder(value: str | None) -> bool:
    return bool(value) and value.strip().strip('"').strip("'") in PLACEHOLDER_KEYS


# ---------------- Messages (Gemini format) ----------------
def make_message(role: str, text: str) -> dict:
    """role is "user" or "model"."""
    return {"role": role, "parts": [{"text": text}]}


def message_text(message: dict) -> str:
    return message["parts"][0]["text"]


def itinerary_request(chat_history: list[dict]) -> list[dict]:
    """The whole conversation plus one final instruction asking for the structured itinerary."""
    return list(chat_history) + [make_message("user", FINAL_REQUEST)]


def parse_itinerary(response) -> TravelItinerary:
    """Turn the API response into a validated TravelItinerary (raises ValueError if it doesn't fit)."""
    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, TravelItinerary):
        return parsed
    text = getattr(response, "text", None)
    if not text:
        raise ValueError("The model returned an empty itinerary. Please try again.")
    return TravelItinerary.model_validate_json(text)


def itinerary_warnings(itinerary: TravelItinerary) -> list[str]:
    """Spot common mistakes the schema alone can't catch."""
    warnings = []
    if len(itinerary.daily_itinerary) != itinerary.duration_days:
        warnings.append(
            f"The trip is {itinerary.duration_days} days, but the plan covers "
            f"{len(itinerary.daily_itinerary)} days."
        )
    if itinerary.budget_category.strip().lower() not in {"low", "medium", "high"}:
        warnings.append(f"Unexpected budget category: {itinerary.budget_category}.")
    return warnings


def itinerary_to_markdown(itinerary: TravelItinerary) -> str:
    lines = [
        f"# Trip to {itinerary.destination}",
        "",
        f"- **Duration:** {itinerary.duration_days} days",
        f"- **Budget:** {itinerary.budget_category}",
        "",
        "## Highlights",
        *[f"- {a}" for a in itinerary.activities],
        "",
        "## Day by day",
    ]
    for d in sorted(itinerary.daily_itinerary, key=lambda d: d.day):
        lines += ["", f"### Day {d.day}", "", d.plan]
    lines += ["", "---", "Planned with the AI Travel Assistant · Learning source: CodeBasics.io"]
    return "\n".join(lines)


# ---------------- Errors ----------------
def friendly_error(error: Exception) -> str:
    """Turn an API error into advice the user can act on."""
    if isinstance(error, ValueError) and not hasattr(error, "code"):
        return f"The itinerary didn't match the expected format. Please try again. ({str(error)[:200]})"
    if any(w in type(error).__name__ for w in ("Connect", "Timeout", "Network")):
        return "Couldn't reach Google's servers. Check your internet connection and try again."
    code = getattr(error, "code", None)
    message = str(getattr(error, "message", "") or error)
    lower = message.lower()
    if "api key" in lower and any(w in lower for w in ("not valid", "invalid", "expired")):
        return "Your API key wasn't accepted. Check that you copied the whole key into .env, then restart."
    if code in (401, 403):
        return "Your API key doesn't have permission for this. Check the key in Google AI Studio."
    if code == 404:
        return "That model isn't available (it may have been retired). Change the model in the sidebar or in .env."
    if code == 429:
        return "You've hit the rate limit or free-tier quota. Wait a minute and try again."
    if code is not None and code >= 500:
        return "Google's servers had a problem. Please try again in a moment."
    return f"Something went wrong: {message}"
