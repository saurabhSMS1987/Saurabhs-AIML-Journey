# Key Takeaways

📚 Learning source: [CodeBasics.io](https://codebasics.io) · Solution by Peter Pandey

## 1. LLMs have no memory; your code provides it
Each API call starts fresh. The assistant only "remembers" because the app keeps every message in `chat_history` and sends the whole list each time.

## 2. In Streamlit, anything that must survive a click goes in `st.session_state`
Streamlit re-runs the script on every interaction. Both the chat memory and the generated itinerary live in session state, or they'd disappear.

## 3. Messages follow a format
Gemini expects each message as `{"role": "user" | "model", "parts": [{"text": ...}]}`. Getting this right is what lets the model tell your messages from its own earlier replies.

## 4. A system instruction shapes the whole conversation
Telling the model it's a travel assistant that should ask about destination, days, budget and interests produces focused, useful replies, without adding anything to the memory list.

## 5. Pydantic turns "please reply in this format" into a guarantee
A schema describes the exact fields and types you need. Passing it as `response_schema` with `response_mime_type="application/json"` makes the model follow it, and `Field(description=...)` doubles as instructions for each field.

## 6. Always validate structured output
Asking for JSON isn't the same as getting valid JSON. Using `response.parsed` or `TravelItinerary.model_validate_json()` means the app only continues with data that really fits the schema.

## 7. Some rules need checks beyond the schema
A schema can require `duration_days` to be an integer, but not that there's one daily plan per day. Small extra checks (like `itinerary_warnings()`) catch these logical mistakes.

## 8. Handle errors without corrupting state
Wrapping API calls in `try...except` prevents crashes, but it's equally important to undo partial changes. Removing a message that never got a reply keeps the memory consistent for later calls.

## 9. Guide users away from mistakes
Disabling **Generate** until there's a conversation, and explaining errors in plain language, prevents confusing results before they happen.

## 10. Keep secrets out of code and out of Git
Put a placeholder in `.env.example`, keep the real key in `.env`, and list `.env` in `.gitignore`. Checking for the placeholder lets the app explain exactly what's wrong.

## 11. Libraries and models change; design for it
`google-generativeai` reached end of support, and Gemini models are retired regularly. Using the current SDK and reading the model name from `.env` means updates are a one-line change.

## 12. Structured data makes better interfaces
Because the itinerary is an object rather than text, the app can show metric cards, one section per day, warnings and downloads. Structured output pays off well beyond the API call.

## 13. Streaming makes apps feel faster
A reply that appears word by word feels quicker than one that appears after a pause. A Python generator that `yield`s each piece, passed to `st.write_stream()`, is all it takes.

## 14. Test without spending API quota
The app was tested with Streamlit's `AppTest` and a stand-in for the Gemini client. That covered normal chats, itinerary generation, schema failures, API errors and the key placeholder without making real API calls.
