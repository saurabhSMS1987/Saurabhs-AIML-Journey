# AI Travel Assistant: Summary

📚 **Learning source:** [CodeBasics.io](https://codebasics.io), *Codebasics Python Course: Python for AI*
👤 **Solution by:** Peter Pandey

## The problem
A travel booking platform wants a smart assistant. Users describe their trip over several messages, so the assistant must:

1. Define a strict **Pydantic schema** for the final itinerary
2. Connect to an **LLM API** and keep **conversational memory**
3. **Handle errors** gracefully
4. Produce a **structured, schema-enforced itinerary** from the conversation
5. Present it all in a **Streamlit** web app

## What the app does
- Chats naturally about your trip and remembers every detail you share
- Asks follow-up questions about anything missing (destination, days, budget, interests)
- Streams replies as they're written
- Produces a validated `TravelItinerary`: destination, duration, budget, highlights and a day-by-day plan
- Displays the itinerary neatly and warns about mismatched day counts
- Exports the itinerary as JSON or Markdown
- Handles errors without crashing or corrupting the memory

## Tech stack

| Tool | Used for |
|------|----------|
| Python | Program logic |
| Streamlit | Web interface and session memory |
| google-genai | Calling Google Gemini models |
| Pydantic | Defining and validating the itinerary structure |
| python-dotenv | Loading the API key from `.env` |
| uv / pip | Installing packages |

## Project structure

```
travel_assistant_assignment/
├── README.md
├── app_solution.py               # Finished app
├── app_1.py                      # Starter app
├── travel_utils.py               # Schema, prompts, helpers
├── .env.example                  # API key placeholder
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .streamlit/config.toml
└── docs/
    ├── HOW_IT_WORKS.md
    ├── QUICK_REFERENCE.md
    ├── SUMMARY.md
    └── KEY_TAKEAWAYS.md
```

## Quick start
```bash
cp .env.example .env            # then replace your_actual_api_key_here with your real key
uv sync                         # or: pip install -r requirements.txt
streamlit run app_solution.py
```

## Improvements over the original solution

| Original | Now |
|----------|-----|
| `google-generativeai`, which Google no longer supports | Current `google-genai` library |
| Model name fixed in code | Set with `GEMINI_MODEL` in `.env` or the sidebar |
| Itinerary shown as raw text, never validated | Validated into a `TravelItinerary` object |
| Failed chat messages left in memory | Removed, so memory stays clean |
| Generate button worked with no conversation | Disabled until you've shared preferences |
| Itinerary vanished after the next message | Kept in `st.session_state` |
| Raw JSON only | Formatted day-by-day view, warnings, JSON and Markdown downloads |
| Reply appeared all at once | Streams as it's written |
| Missing key caused confusing errors | Clear setup steps, including placeholder detection |

## Possible next steps
- Use `Literal["Low", "Medium", "High"]` for a stricter budget field
- Add estimated costs per day and a total budget to the schema
- Let users regenerate a single day without redoing the whole trip
- Add Google Search grounding for current opening hours and events
- Save trips to a database so they're available later
