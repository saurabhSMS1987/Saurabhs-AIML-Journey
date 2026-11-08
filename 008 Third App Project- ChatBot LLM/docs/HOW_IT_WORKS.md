# How the Code Works: A Step-by-Step Guide

This guide follows the chatbot from the moment it starts to the moment a reply appears. It builds on the idea from `chatbot.ipynb`, a lesson from [CodeBasics.io](https://codebasics.io):

> **An LLM has no memory.** Each call is a blank slate. The app "remembers" by keeping every message in a list and re-sending that list every time.

The project is split into files with separate jobs:

| File | Job |
|------|-----|
| `app.py` | The interface: sidebar settings, chat display, sending messages. |
| `chat_utils.py` | Plain Python helpers: message format, memory window, saving and loading, error messages. No Streamlit code, so it can be tested on its own. |
| `chatbot.ipynb` | The lesson: proves the model forgets, then fixes it with a list. |

---

## Step 1: Understand how Streamlit runs your script

Every time you interact with the page (send a message, click a button, move a slider), Streamlit **re-runs `app.py` from top to bottom**. Normal variables are recreated from scratch on each run, which would wipe the chat.

That's why the conversation lives in **`st.session_state`**, which survives reruns for as long as the browser tab is open:

```python
if "conversation" not in st.session_state:
    st.session_state.conversation = []
```

This list *is* the chatbot's memory.

## Step 2: Load settings and find the API key

```python
load_dotenv()
```

`load_dotenv()` reads the `.env` file and puts `GEMINI_API_KEY` (and optionally `GEMINI_MODEL`) into the environment.

The app looks for a key in three places, in this order:

1. The **Gemini API key** box in the sidebar
2. **Streamlit secrets** (used when deployed to Streamlit Community Cloud)
3. The **`.env` file** (`GEMINI_API_KEY`, or `GOOGLE_API_KEY`)

Each value passes through `clean_key()`, which strips spaces and quotes and treats the placeholder `your-api-key-here` as "no key". So if you forget to replace the placeholder, the app doesn't send a fake key to Google; it shows setup instructions instead.

`key_from_secrets()` wraps `st.secrets` in `try/except`, because reading secrets raises an error when no secrets file exists, which is normal when running locally.

## Step 3: Create the Gemini client once

```python
@st.cache_resource(show_spinner=False)
def get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)
```

Because the script re-runs constantly, `@st.cache_resource` keeps one client per key instead of creating a new one on every click.

## Step 4: Build the model list

```python
@st.cache_data(ttl=3600, show_spinner=False)
def load_model_names(api_key: str) -> list[str]:
    return cu.chat_model_names(get_client(api_key).models.list())
```

Google regularly retires older models, so a hard-coded model name eventually stops working. Instead, the app asks the API which models your key can use.

`chat_model_names()` keeps only models that:
- start with `gemini`
- support `generateContent` (text replies)
- aren't specialist models (speech, images, embeddings, live audio)

Names ending in `-latest` (like `gemini-flash-latest`) are listed first. These are aliases Google keeps pointed at its current model, so they're the safest default.

The list is cached for an hour (`ttl=3600`). If loading fails, the exception isn't cached, so the app tries again on the next run; meanwhile it shows `FALLBACK_MODELS` and a note explaining why. You can also type any model name in the box underneath.

## Step 5: Read the other sidebar settings

- **Personality** picks a *system instruction* from `PERSONALITIES` in `chat_utils.py`. A system instruction is guidance the model follows for the whole chat but which isn't part of the conversation list. "Custom…" lets you write your own; "No personality" sends none.
- **Creativity** is off by default, which lets each model use its recommended temperature. When ticked, the slider value (0 to 2) is sent.
- **Remember the last…** sets `max_exchanges`: how many recent question-and-answer pairs are sent. "Everything" means `None`, which sends the full list.

## Step 6: Decide what part of memory to send

```python
def messages_to_send(conversation, max_exchanges):
    if max_exchanges is None:
        window = list(conversation)
    else:
        window = conversation[-(max_exchanges * 2 + 1):]
    while window and window[0]["role"] != "user":
        window = window[1:]
    return window
```

Each exchange is 2 messages (user + model), plus 1 for the new question, hence `max_exchanges * 2 + 1`. The `while` loop makes sure the list starts with a user message, which is the order Gemini expects.

Real chat products do something similar: memory costs money and time (every message is re-sent), and models have a limit on how much text they can read. Trimming is the simplest way to manage that. Note that **only what's sent is trimmed**; the full chat stays stored, so switching back to "Everything" restores full memory.

The sidebar shows both numbers, such as "12 messages stored · the model sees the last 3".

## Step 7: Undo, clear, save and load

- **Clear chat** replaces the list with `[]`, and the model instantly "forgets".
- **Undo last** calls `undo_last_exchange()`, which removes the newest reply and the question before it.
- **Download as Markdown** builds a readable transcript with `to_markdown()`.
- **Download as JSON** saves the raw list with `to_json()`. This is exactly the memory format, so it can be loaded back later.
- **Load this chat** reads an uploaded file with `parse_saved_chat()`. It checks that the file is a list of messages, each with a `user` or `model` role and some text. Anything else gets a clear error message instead of crashing. Loading only happens when you press the button, so it doesn't repeat on every rerun.

After each of these, `st.rerun()` redraws the page with the new memory.

## Step 8: Stop early if there's no key

If no usable key was found, the main area shows step-by-step setup instructions (with an extra note if the placeholder is still in `.env`), and `st.stop()` ends the run. The sidebar has already been drawn, so you can still paste a key there.

## Step 9: Show the conversation and the memory

```python
for message in st.session_state.conversation:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(cu.message_text(message))
```

Gemini calls the AI's role `"model"`, while Streamlit's chat bubbles use `"assistant"`, so the role is translated for display.

**🔍 Peek inside the memory** shows the exact list that will be sent next, the same idea as printing `conversation` in the notebook.

## Step 10: Send a message and stream the reply

When you type a message, three things happen, just like `chat()` in the notebook:

**1. Add the question to memory and show it.**

```python
st.session_state.conversation.append(cu.make_message("user", user_input))
```

`make_message()` builds Gemini's format: `{"role": "user", "parts": [{"text": ...}]}`.

**2. Send the remembered conversation and stream the reply.**

```python
config = types.GenerateContentConfig(
    system_instruction=system_instruction or None,
    temperature=temperature,
)
reply = st.write_stream(stream_reply(get_client(api_key), model, contents, config))
```

`stream_reply()` is a **generator**: it calls `generate_content_stream()` and `yield`s each piece of text as Gemini writes it. `st.write_stream()` displays the pieces as they arrive and returns the full reply at the end. Pieces with no text are skipped.

**3. Save the reply to memory**, then `st.rerun()` so the sidebar counts and download buttons include the new messages.

## Step 11: Handle errors without corrupting memory

The original version saved error messages into the conversation as if the AI had said them. Those errors were then sent back to the model with every later message. This version fixes that:

```python
if error:
    st.session_state.conversation.pop()   # remove the unanswered question
    ...
else:
    st.session_state.conversation.append(cu.make_message("model", reply))
```

On failure, the error is shown on screen only, and the unanswered question is removed, so the memory stays a clean back-and-forth of real messages.

`friendly_error()` turns technical errors into advice:

| Problem | What you see |
|---------|--------------|
| Bad API key | "Your API key wasn't accepted…" |
| 401 / 403 | "doesn't have permission…" |
| 404 | "That model isn't available (it may have been retired)…" |
| 429 | "You've hit the rate limit or free-tier quota…" |
| 500+ | "Google's servers had a problem…" |
| No connection | "Couldn't reach Google's servers…" |
| Empty reply | "possibly because of its safety filters…" |

---

## How data flows through the app

```
 .env / secrets / sidebar ──► clean_key() ──► get_client()  (cached)
                                                  │
                         models.list() ──► chat_model_names() ──► Model dropdown
                                                  │
 You type a message                               │
        │                                         │
        ▼                                         ▼
 conversation.append(user msg)        messages_to_send(memory slider)
        │                                         │
        └──────────────► generate_content_stream(model, contents, config)
                                                  │
                                    st.write_stream() shows it live
                                                  │
                             ┌────────────────────┴─────────────────┐
                          success                                 error
                             │                                      │
               conversation.append(model msg)       remove user msg, show friendly_error()
```
