# ✈️ AI Travel Assistant

A Streamlit web app that plans trips through conversation. It teaches **LLM API calling**, **conversational memory**, **structured Pydantic outputs**, and **Streamlit UI development**.

> 📚 **Learning source:** [CodeBasics.io](https://codebasics.io), *Python for AI* course
> 👤 **Solution by:** Peter Pandey

**The problem:** a booking platform wants a travel assistant. Users share their preferences over several messages, so the assistant must remember the conversation, call an LLM, handle errors gracefully, and finally export a strict, structured itinerary.

## What's inside

| File | Purpose |
|------|---------|
| `app_solution.py` | The finished Streamlit app |
| `app_1.py` | Starter file for building your own version |
| `travel_utils.py` | Itinerary schema, prompts and helper functions |
| `.env.example` | API key template with a **placeholder** (copy to `.env`) |
| `requirements.txt` | Packages for `pip` |
| `pyproject.toml` / `uv.lock` | Packages for `uv` (exact, tested versions) |
| `.streamlit/config.toml` | App color theme |
| `docs/` | How it works, quick reference, summary, key takeaways |

## Quick start

### 1. Get the files
Clone the repository, or click **Code → Download ZIP** on GitHub, right-click the zip, choose **Extract All**, and open the folder in your terminal.

### 2. Add your API key ⚠️
The project contains a **placeholder** instead of a real key. The app won't work until you replace it.

1. Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).
2. Copy `.env.example` and name the copy **`.env`** (same folder).
3. In `.env`, replace `your_actual_api_key_here` with your real key:
   ```text
   GEMINI_API_KEY=AIza...your-real-key...
   ```
4. Save. **Never upload `.env` to GitHub.** It's already in `.gitignore`.

### 3. Install the packages

Using `uv` (recommended):
```bash
uv sync
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

Or using `pip`:
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app_solution.py
```
It opens at http://localhost:8501.

Try telling the assistant: *"I want to visit Kyoto for 4 days"*, then *"Medium budget, I love temples and local food"*, then click **Generate final itinerary**.

## Features
- **Conversational memory:** every message is stored and re-sent, so the assistant remembers earlier preferences
- **Helpful follow-up questions** about anything missing: destination, days, budget, interests
- **Streaming replies** that appear as they're written
- **Structured output:** the final itinerary is forced into the `TravelItinerary` Pydantic schema and validated
- **Clear itinerary view:** destination, duration, budget, highlights and a section for each day
- **Sanity check:** a warning if the plan doesn't cover every day of the trip
- **Downloads:** save the itinerary as JSON or Markdown
- **Graceful errors:** plain-language messages, and failed requests never pollute the memory
- **Safe setup:** API key placeholder, detection of an unreplaced placeholder, and `.env` kept out of Git

## Changes from the original course files
- Switched from `google-generativeai` (no longer supported by Google) to the current **`google-genai`** library
- The model is configurable with `GEMINI_MODEL` in `.env` (default `gemini-3.6-flash`)
- The itinerary is validated with Pydantic and displayed neatly, not shown as raw text
- Failed messages are no longer left in the chat memory
- The itinerary stays on screen after the next message, and the button only works once you've chatted
- `README` paths fixed, and `uv.lock` regenerated to match the dependencies

## Documentation
- [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md): setup, usage and troubleshooting
- [docs/HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md): step-by-step code walkthrough
- [docs/SUMMARY.md](docs/SUMMARY.md): project overview
- [docs/KEY_TAKEAWAYS.md](docs/KEY_TAKEAWAYS.md): what this project teaches

## Credits
Assignment, problem statement and original materials: [CodeBasics.io](https://codebasics.io) (*Codebasics Python Course: Python for AI*). Solution and extensions: Peter Pandey.
