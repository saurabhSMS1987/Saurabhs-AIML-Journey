# How the Code Works: A Step-by-Step Guide

📚 Learning source: [CodeBasics.io](https://codebasics.io) · Solution by Peter Pandey

The project is split into two files with separate jobs:

| File | Job |
|------|-----|
| `app_solution.py` | The web interface: chat, itinerary display, downloads |
| `travel_utils.py` | The schema, prompts and helper functions. No Streamlit code, so it's easy to test on its own |

`app_1.py` is a starter file for building your own version.

---

## Step 1: Describe the output with Pydantic (`travel_utils.py`)

```python
class DailyPlan(BaseModel):
    day: int = Field(description="The day number, e.g., 1")
    plan: str = Field(description="A detailed paragraph of the itinerary for this day")

class TravelItinerary(BaseModel):
    destination: str = Field(...)
    duration_days: int = Field(...)
    budget_category: str = Field(...)
    activities: List[str] = Field(...)
    daily_itinerary: List[DailyPlan] = Field(...)
```

A Pydantic model is a blueprint that checks data. `TravelItinerary` says exactly which fields the final plan must have and what type each one is. Because each day has two parts (`day` and `plan`), it gets its own model, `DailyPlan`, which `TravelItinerary` uses as a list.

The `Field(description=...)` text is sent to Gemini along with the schema, so the descriptions double as instructions, for example that `duration_days` must be a whole number.

## Step 2: Understand how Streamlit runs the app

Every time you interact with the page (send a message, click a button), Streamlit **re-runs `app_solution.py` from top to bottom**. Normal variables are recreated each time, which would wipe the conversation. So anything that must last goes in **`st.session_state`**:

```python
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None
```

**`chat_history` is the memory.** LLMs forget everything between calls, so the app keeps the conversation itself and sends the whole list each time. `itinerary` keeps the generated plan on screen across reruns.

## Step 3: Load the API key and model

```python
load_dotenv()
env_key = os.getenv("GEMINI_API_KEY")
api_key = tu.clean_key(sidebar_key) or tu.clean_key(env_key)
```

- `load_dotenv()` reads your key from `.env`, so it never appears in the code.
- The app checks the sidebar's **Gemini API key** box first, then `.env`.
- `clean_key()` strips spaces and quotes, and treats the placeholder `your_actual_api_key_here` as "no key".
- With no usable key, the app shows setup steps (with a specific note if the placeholder is still in `.env`), and `st.stop()` ends the run. The sidebar is already drawn, so you can still paste a key there.
- The model comes from `GEMINI_MODEL` in `.env` (default `gemini-3.6-flash`) and can be changed in the sidebar. When Google retires a model, you change one line, not the code.

The client is created once per key with `@st.cache_resource`, so it isn't rebuilt on every click:

```python
@st.cache_resource(show_spinner=False)
def get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)
```

`genai.Client` comes from **`google-genai`**, Google's current library. The original files used `google-generativeai`, which Google no longer supports.

## Step 4: Show the conversation

```python
for message in st.session_state.chat_history:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(tu.message_text(message))
```

Each message is stored in Gemini's format: `{"role": "user" or "model", "parts": [{"text": ...}]}`. Streamlit's chat bubbles call the AI `"assistant"`, so the role is translated for display.

## Step 5: Chat with streaming replies

When you send a message:

1. **Save it to memory and show it.**
   ```python
   st.session_state.chat_history.append(tu.make_message("user", prompt))
   ```
2. **Send the whole history and stream the reply.**
   ```python
   reply = st.write_stream(stream_reply(client, model, st.session_state.chat_history))
   ```
   `stream_reply()` is a **generator**: it calls `generate_content_stream()` and `yield`s each piece of text as Gemini writes it. `st.write_stream()` shows the pieces as they arrive and returns the full reply.

   A **system instruction** (`SYSTEM_INSTRUCTION` in `travel_utils.py`) tells the model to act as a travel assistant and ask about destination, days, budget and interests. It applies to every reply but isn't part of `chat_history`.
3. **Save the reply to memory**, then `st.rerun()` so the sidebar's message count updates.

If the request fails or the reply is empty, the error is shown and **the unanswered message is removed** with `chat_history.pop()`. That keeps the memory a clean back-and-forth instead of collecting messages that never got a reply.

## Step 6: Generate the structured itinerary

The **🗺️ Generate final itinerary** button is disabled until you've sent at least one message. When clicked, it calls:

```python
response = client.models.generate_content(
    model=model,
    contents=tu.itinerary_request(chat_history),
    config=types.GenerateContentConfig(
        system_instruction=tu.SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        response_schema=tu.TravelItinerary,
    ),
)
```

- **`itinerary_request()`** sends the whole conversation plus one final instruction (`FINAL_REQUEST`) asking for every field and one plan per day. The instruction is added only for this call, not saved to memory.
- **`response_mime_type="application/json"`** makes the model reply with JSON instead of prose.
- **`response_schema=TravelItinerary`** forces that JSON to follow the Pydantic schema.

## Step 7: Validate the result

```python
def parse_itinerary(response) -> TravelItinerary:
    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, TravelItinerary):
        return parsed
    ...
    return TravelItinerary.model_validate_json(text)
```

`google-genai` normally fills `response.parsed` with a ready `TravelItinerary` object. If it can't, `model_validate_json()` checks the raw text and raises an error if anything is missing or the wrong type. Either way, the app only continues with a valid itinerary.

The original solution showed `result.text` without validating it, so a broken response would have been displayed as if it were fine.

## Step 8: Display and download the itinerary

Because the itinerary is a real object, not just text, the app can display it properly:

- The destination, plus metric cards for duration and budget
- The highlights from `activities`
- An expandable section for each day, sorted by day number
- **Warnings** from `itinerary_warnings()` if the number of daily plans doesn't match `duration_days`, or the budget isn't Low, Medium or High
- The raw Pydantic JSON in an expander
- **Downloads** as JSON (`model_dump_json()`) or Markdown (`itinerary_to_markdown()`)

## Step 9: Friendly errors and starting over

`friendly_error()` turns technical errors into next steps:

| Problem | What you see |
|---------|--------------|
| Itinerary fails validation | "didn't match the expected format. Please try again." |
| Rejected key | "Your API key wasn't accepted…" |
| 401 / 403 | "doesn't have permission…" |
| 404 | "That model isn't available (it may have been retired)…" |
| 429 | "You've hit the rate limit or free-tier quota…" |
| 500+ | "Google's servers had a problem…" |
| No connection | "Couldn't reach Google's servers…" |

**🔄 Start a new trip** in the sidebar empties `chat_history` and removes the itinerary.

---

## How data flows

```
 .env / sidebar ──► API key + model ──► genai.Client (cached)
                                              │
 your message ──► chat_history.append(user)   │
                                              ▼
                  generate_content_stream(chat_history, system instruction)
                                              │
                  st.write_stream() shows it live
                                              │
                  chat_history.append(model reply)   (user message removed if it failed)
                                              │
 Generate button                              ▼
                  chat_history + FINAL_REQUEST
                                              │
                  generate_content(response_schema=TravelItinerary, JSON)
                                              │
                  response.parsed  or  TravelItinerary.model_validate_json()
                                              │
                  ✅ validated TravelItinerary ──► st.session_state.itinerary
                                              │
                  formatted view · warnings · JSON / Markdown downloads
```
