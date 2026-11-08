"""Helper functions for the chatbot. No Streamlit code here, so everything can be tested on its own."""
import json
from datetime import datetime

PLACEHOLDER_KEY = "your-api-key-here"

# Used when the live model list can't be loaded. The "-latest" aliases are kept
# up to date by Google, so they keep working when older models are retired.
DEFAULT_MODEL = "gemini-flash-latest"
FALLBACK_MODELS = ["gemini-flash-latest", "gemini-flash-lite-latest"]

# Model names containing these words aren't text-chat models (speech, images, embeddings...).
NON_CHAT_WORDS = ("tts", "image", "embedding", "live", "audio", "computer-use", "veo", "imagen", "aqa")

PERSONALITIES = {
    "Helpful assistant": "You are a helpful, friendly assistant. Give clear, accurate answers and keep them reasonably concise.",
    "Patient tutor": "You are a patient tutor. Explain ideas step by step with simple examples, and check whether the user understood before moving on.",
    "Witty movie buff": "You are a witty movie buff who loves making puns. Recommend films based on what the user has told you about their taste.",
    "Concise expert": "You are an expert who answers in as few words as possible. Use short sentences or brief bullet points.",
    "Coding helper": "You are an experienced Python developer. Explain code clearly, point out bugs, and show short, working examples.",
    "No personality": "",
}
CUSTOM_PERSONALITY = "Custom…"


# ---------------- API key ----------------
def clean_key(value: str | None) -> str | None:
    """Return the key, or None if it's empty or still the placeholder."""
    if not value:
        return None
    value = value.strip().strip('"').strip("'")
    if not value or value == PLACEHOLDER_KEY:
        return None
    return value


def is_placeholder(value: str | None) -> bool:
    return bool(value) and value.strip().strip('"').strip("'") == PLACEHOLDER_KEY


# ---------------- Messages ----------------
def make_message(role: str, text: str) -> dict:
    """Gemini's message format. role is "user" or "model"."""
    return {"role": role, "parts": [{"text": text}]}


def message_text(message: dict) -> str:
    return message["parts"][0]["text"]


def messages_to_send(conversation: list[dict], max_exchanges: int | None) -> list[dict]:
    """The part of the memory sent to the model.

    max_exchanges=None sends everything. Otherwise only the last N user+model
    pairs (plus the newest user message) are sent. The result always starts
    with a user message, which is what Gemini expects.
    """
    if max_exchanges is None:
        window = list(conversation)
    else:
        window = conversation[-(max_exchanges * 2 + 1):]
    while window and window[0]["role"] != "user":
        window = window[1:]
    return window


def undo_last_exchange(conversation: list[dict]) -> list[dict]:
    """Remove the newest model reply and the user message before it."""
    convo = list(conversation)
    if convo and convo[-1]["role"] == "model":
        convo.pop()
    if convo and convo[-1]["role"] == "user":
        convo.pop()
    return convo


# ---------------- Saving and loading ----------------
def to_json(conversation: list[dict]) -> str:
    return json.dumps(conversation, ensure_ascii=False, indent=2)


def to_markdown(conversation: list[dict], model: str, personality: str) -> str:
    lines = [
        "# Chat transcript",
        "",
        f"- Saved: {datetime.now():%Y-%m-%d %H:%M}",
        f"- Model: {model}",
        f"- Personality: {personality}",
        "",
    ]
    for m in conversation:
        speaker = "🧑 You" if m["role"] == "user" else "🤖 Assistant"
        lines += [f"### {speaker}", "", message_text(m), ""]
    return "\n".join(lines)


def parse_saved_chat(raw: bytes | str) -> list[dict]:
    """Read a chat saved with to_json(). Raises ValueError with a friendly message if it isn't valid."""
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("This file isn't valid JSON. Upload a chat saved from this app (the .json download).")
    if not isinstance(data, list):
        raise ValueError("This file doesn't contain a chat. Upload a chat saved from this app.")

    conversation = []
    for i, m in enumerate(data, start=1):
        try:
            role, text = m["role"], m["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            raise ValueError(f"Message {i} isn't in the expected format.")
        if role not in ("user", "model") or not isinstance(text, str):
            raise ValueError(f"Message {i} has an unknown role or no text.")
        conversation.append(make_message(role, text))
    return conversation


# ---------------- Models ----------------
def chat_model_names(models) -> list[str]:
    """Pick text-chat Gemini models from client.models.list() results, newest-looking first."""
    names = set()
    for m in models:
        name = (getattr(m, "name", "") or "").removeprefix("models/")
        actions = getattr(m, "supported_actions", None) or []
        if (
            name.startswith("gemini")
            and "generateContent" in actions
            and not any(word in name for word in NON_CHAT_WORDS)
        ):
            names.add(name)
    aliases = sorted(n for n in names if n.endswith("-latest"))
    others = sorted((n for n in names if not n.endswith("-latest")), reverse=True)
    return aliases + others


# ---------------- Errors ----------------
def friendly_error(error: Exception) -> str:
    """Turn an API error into advice the user can act on."""
    if any(word in type(error).__name__ for word in ("Connect", "Timeout", "Network")):
        return "Couldn't reach Google's servers. Check your internet connection and try again."

    code = getattr(error, "code", None)
    message = str(getattr(error, "message", "") or error)
    lower = message.lower()

    if "api key" in lower and ("not valid" in lower or "invalid" in lower or "expired" in lower):
        return "Your API key wasn't accepted. Check that you copied the whole key, then restart the app."
    if code in (401, 403):
        return "Your API key doesn't have permission for this. Check the key in Google AI Studio."
    if code == 404:
        return "That model isn't available (it may have been retired). Pick another model in the sidebar."
    if code == 429:
        return "You've hit the rate limit or free-tier quota. Wait a minute and try again, or choose a lighter model."
    if code is not None and code >= 500:
        return "Google's servers had a problem. Please try again in a moment."
    if code == 400:
        return f"The request was rejected: {message}"
    return f"Something went wrong: {message}"
