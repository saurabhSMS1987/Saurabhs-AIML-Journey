# Key Takeaways

What this project teaches about building chat apps with language models. The core lesson comes from [CodeBasics.io](https://codebasics.io).

## 1. Language models have no memory
Each API call is a blank slate. Every chatbot "remembers" the same way: it stores the conversation itself and sends it back with each new message. Here that's a plain Python list of dictionaries.

## 2. In Streamlit, memory needs `st.session_state`
Streamlit re-runs the whole script on every interaction, so ordinary variables are reset each time. `st.session_state` keeps the conversation alive between reruns for as long as the browser tab is open.

## 3. Memory has a cost, so it can be managed
The whole history is re-sent with every message, so longer chats are slower, cost more, and can exceed the model's limit. The memory slider shows the trade-off: send less, and the bot forgets older details. Sending less doesn't have to mean storing less.

## 4. Keep errors out of the conversation
If an error message is saved as the AI's reply, it's sent back to the model with every later message and can confuse it. Show errors on screen, and remove the unanswered question so the memory stays a clean back-and-forth.

## 5. Never put a real API key in code you share
Use a placeholder in a template (`.env.example`), keep the real key in `.env`, and list `.env` in `.gitignore`. Anyone who finds your key can use your quota. If a key is ever uploaded by mistake, delete it in Google AI Studio and create a new one.

## 6. Check for the placeholder, not just a missing key
A common mistake is forgetting to replace `your-api-key-here`. Detecting the placeholder lets the app say exactly what's wrong, instead of sending a fake key and showing a confusing error from Google.

## 7. Don't hard-code model names that can expire
AI providers retire models regularly, and a fixed name like `gemini-2.5-flash` eventually breaks. Using a `-latest` alias, reading the default from settings, and loading the model list from the API keeps the app working as models change.

## 8. Streaming makes apps feel faster
A reply that appears word by word feels quicker than one that appears all at once after a pause, even if the total time is the same. A Python generator that `yield`s each piece, passed to `st.write_stream()`, is all it takes.

## 9. A system instruction shapes the whole chat
Personalities are set with a system instruction, which the model follows throughout but which isn't part of the conversation list. That's why switching personality mid-chat changes the tone of later replies without rewriting history.

## 10. Turn technical errors into actions
"404 NOT_FOUND" doesn't help most people. "That model isn't available; pick another one in the sidebar" does. Mapping error codes to plain-language next steps is one of the cheapest ways to make an app feel reliable.

## 11. Cache what doesn't need repeating, but not failures
The client and model list are cached so they aren't recreated on every click. Streamlit doesn't cache a function that raised an error, so a failed model-list request is simply retried later instead of being stuck for an hour.

## 12. Keep logic separate from the interface
`chat_utils.py` has no Streamlit code, so the memory window, file loading and error messages can be tested directly. The app itself was tested with Streamlit's `AppTest` and a fake Gemini client, covering normal chats, memory limits, undo, missing keys, the placeholder, and API errors, without spending any API quota.
