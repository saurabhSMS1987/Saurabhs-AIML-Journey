# Chatbot with Memory: Summary

A chat app built with **Python**, **Streamlit** and **Google Gemini** that shows how chatbot memory works. Language models don't remember anything between calls, so the app keeps the whole conversation in a Python list and re-sends it with every message. That list is the memory.

It started from a teaching notebook and a 25-line app from the [CodeBasics.io](https://codebasics.io) course, and was extended into a fuller, more robust chatbot.

## What it does

- **Remembers the conversation** using a list kept in `st.session_state`
- **Streams replies** word by word as the model writes them
- **Lists available models live** from your Gemini account, with a box for any model name
- **Offers personalities** (helpful assistant, patient tutor, witty movie buff, concise expert, coding helper) or a custom one
- **Lets you control memory size**, from the last exchange to everything
- **Shows the memory** exactly as it's sent to the model
- **Undoes** the last exchange or **clears** the chat
- **Saves chats** as Markdown (to read) or JSON (to reload and continue)
- **Explains errors** in plain language and keeps errors out of the memory
- **Protects your API key** with a placeholder template and `.gitignore`

## Tech stack

| Tool | Used for |
|------|----------|
| Python | App logic |
| Streamlit | Web interface and session memory |
| google-genai | Talking to Gemini models |
| python-dotenv | Loading the API key from `.env` |

## Project structure

```
gemini_chatbot/
├── app.py                        # The chat app
├── chat_utils.py                 # Helpers (no Streamlit code)
├── chatbot.ipynb                 # Lesson notebook
├── requirements.txt              # Python packages
├── .env.example                  # API key template (placeholder)
├── .gitignore                    # Keeps .env and secrets off GitHub
├── .streamlit/
│   ├── config.toml               # Theme
│   └── secrets.toml.example      # Key template for Streamlit Cloud
└── docs/
    ├── HOW_IT_WORKS.md
    ├── QUICK_REFERENCE.md
    ├── SUMMARY.md
    └── KEY_TAKEAWAYS.md
```

## Quick start

```bash
cp .env.example .env          # then replace your-api-key-here with your real key
pip install -r requirements.txt
streamlit run app.py
```

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for full steps and troubleshooting.

## Improvements over the original app

| Original | Now |
|----------|-----|
| Fixed model `gemini-2.5-flash`, which Google has scheduled for retirement | Live model list, `gemini-flash-latest` default, any model by name |
| Errors saved into memory as if the AI said them | Errors shown on screen only; memory stays clean |
| Crash if the key was missing | Setup instructions, including a check for the unreplaced placeholder |
| Reply appears all at once | Reply streams in as it's written |
| Always sends the full history | Adjustable memory window |
| Clear chat only | Undo, save, reload, personalities, creativity |

## Learning source
The core lesson (an LLM has no memory, so the app keeps the conversation in a list) comes from [CodeBasics.io](https://codebasics.io).

## Possible next steps

- Summarize old messages instead of dropping them, so long chats keep the gist
- Upload images or PDFs and ask questions about them
- Save chats to a database so they survive closing the browser
- Show token usage and estimated cost per message
- Let the bot search the web for current information
