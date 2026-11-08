# 💬 Chatbot with Memory (Streamlit + Google Gemini)

A chat app that remembers your conversation, built to show how chatbot "memory" really works: the app keeps every message in a Python list and re-sends it to the model each time.

> 📚 **Learning source:** based on a lesson from [CodeBasics.io](https://codebasics.io).

## ⚠️ Before you start: add your API key
This project ships with a **placeholder** instead of a real key. The app won't work until you replace it.

1. Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey).
2. Copy `.env.example` to a new file named **`.env`** in the same folder.
3. Open `.env` and replace `your-api-key-here` with your real key:
   ```
   GEMINI_API_KEY=AIza...your-real-key...
   ```
4. Save the file. **Never upload `.env` to GitHub.** It's already listed in `.gitignore`.

## Run it
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501.

## Files
| File | Purpose |
|------|---------|
| `app.py` | The Streamlit chat app |
| `chat_utils.py` | Helper functions: memory window, saving/loading, error messages |
| `chatbot.ipynb` | Lesson notebook explaining how chatbot memory works |
| `requirements.txt` | Python packages |
| `.env.example` | Template for your API key (copy to `.env`) |
| `.streamlit/config.toml` | Color theme |
| `.streamlit/secrets.toml.example` | Template for deploying to Streamlit Community Cloud |
| `docs/` | How it works, quick reference, summary, key takeaways |

## Features
- **Memory:** the bot remembers everything said earlier in the chat
- **Streaming replies** that appear word by word
- **Model picker** loaded live from your Gemini account, plus a box for any model name
- **Personalities:** helpful assistant, tutor, movie buff, concise expert, coding helper, or your own
- **Memory slider:** choose how much of the conversation the model sees
- **Peek inside the memory:** see the exact list sent to Gemini
- **Undo** the last exchange, or **clear** the whole chat
- **Save** chats as Markdown or JSON, and **reload** a saved JSON chat later
- **Friendly errors** for bad keys, retired models, rate limits and connection problems

## Credits
The chatbot-memory lesson and the original notebook and app come from [CodeBasics.io](https://codebasics.io). This project extends them with extra features and documentation.

## Learn more
- [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) – setup, usage, troubleshooting
- [docs/HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md) – step-by-step code walkthrough
- [docs/SUMMARY.md](docs/SUMMARY.md) – project overview
- [docs/KEY_TAKEAWAYS.md](docs/KEY_TAKEAWAYS.md) – what this project teaches
