# Quick Reference Guide: Running the Chatbot

## Requirements
- Python 3.10 or newer
- A Google Gemini API key (free tier available)
- An internet connection

## Step 1: Get an API key
1. Go to [Google AI Studio](https://aistudio.google.com/apikey) and sign in with a Google account.
2. Click **Create API key** and copy it.

## Step 2: Replace the placeholder with your key ⚠️

The project contains **`your-api-key-here`** as a placeholder. You must replace it with your real key.

| Step | macOS / Linux | Windows |
|------|---------------|---------|
| Copy the template | `cp .env.example .env` | `copy .env.example .env` |
| Open it | Any text editor | Any text editor (e.g. Notepad) |

Change this line in **`.env`**:
```
GEMINI_API_KEY=your-api-key-here
```
to:
```
GEMINI_API_KEY=AIza...your-real-key...
```
No quotes or spaces are needed. Save the file.

> 🔒 **Keep your key private.** `.env` is listed in `.gitignore`, so Git won't upload it. Never paste your key into `app.py`, `.env.example`, or anything else you push to GitHub.

**Alternative:** skip the `.env` file and paste your key into **Gemini API key** in the app's sidebar. It's kept only for that browser session.

## Step 3: Install and run

| Step | macOS / Linux | Windows |
|------|---------------|---------|
| 1. Go to the project folder | `cd gemini_chatbot` | `cd gemini_chatbot` |
| 2. Create a virtual environment | `python3 -m venv venv` | `python -m venv venv` |
| 3. Activate it | `source venv/bin/activate` | `venv\Scripts\activate` |
| 4. Install packages | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| 5. Start the app | `streamlit run app.py` | `streamlit run app.py` |

The app opens at **http://localhost:8501**. Stop it with **Ctrl + C**.

**Every time after that:**
```bash
cd gemini_chatbot
source venv/bin/activate        # Windows: venv\Scripts\activate
streamlit run app.py
```

## Running the notebook (optional)
```bash
pip install notebook
jupyter notebook chatbot.ipynb
```
The notebook reads the same `.env` file, so do Step 2 first.

## Folder layout
```
gemini_chatbot/
├── app.py
├── chat_utils.py
├── chatbot.ipynb
├── requirements.txt
├── .env.example          ← template (uploaded to GitHub)
├── .env                  ← your real key (created by you, NOT uploaded)
├── .gitignore
└── .streamlit/
    ├── config.toml
    └── secrets.toml.example
```

## Using the app

| I want to… | Do this |
|------------|---------|
| Chat | Type in the box at the bottom and press **Enter** |
| Change the model | Sidebar → **Model**, or type a name in **…or type a model name** |
| Change the bot's personality | Sidebar → **Personality** (choose **Custom…** to write your own) |
| Make answers more or less creative | Sidebar → tick **Set creativity** → move the slider |
| Limit what the bot remembers | Sidebar → **Remember the last…** |
| See what's sent to the model | Main page → **🔍 Peek inside the memory** |
| Remove the last question and answer | Sidebar → **↩️ Undo last** |
| Start a new chat | Sidebar → **🗑️ Clear chat** |
| Save a chat to read later | Sidebar → **Download as Markdown** |
| Save a chat to continue later | Sidebar → **Download as JSON** |
| Continue a saved chat | Sidebar → upload the `.json` file → **Load this chat** |

**Good to know**
- Changing the personality or model mid-chat affects the **next** replies only.
- "Remember the last…" changes what is **sent** to the model, not what's stored. Switching back to **Everything** restores full memory.
- Refreshing the browser tab starts a new chat. Download the chat first if you want to keep it.

## Settings in `.env`

| Setting | Purpose | Example |
|---------|---------|---------|
| `GEMINI_API_KEY` | Your API key (required) | `AIza...` |
| `GEMINI_MODEL` | Model selected by default (optional) | `gemini-flash-latest` |

## Deploy to Streamlit Community Cloud (optional)
1. Push the project to GitHub (your `.env` stays on your computer).
2. On [share.streamlit.io](https://share.streamlit.io), create an app from your repository with `app.py` as the main file.
3. In the app's **Settings → Secrets**, paste the contents of `.streamlit/secrets.toml.example` and replace `your-api-key-here` with your real key.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No API key found" | Create `.env` from `.env.example`, add your key, and restart the app |
| "still contains the placeholder" | Replace `your-api-key-here` in `.env` with your real key, then restart |
| "Your API key wasn't accepted" | Re-copy the full key from AI Studio; check for missing characters |
| "That model isn't available" | The model was retired or the name is wrong. Pick another model in the sidebar |
| "Couldn't load the model list" | The app shows default models instead. Usually a key or connection problem |
| "rate limit or free-tier quota" | Wait a minute, or switch to a lighter model (e.g. a Flash-Lite model) |
| "Couldn't reach Google's servers" | Check your internet connection or firewall |
| "empty reply" | The reply was blocked by safety filters. Rephrase your message |
| Key changes in `.env` not picked up | Restart the app; `.env` is read when the app starts |
| `streamlit: command not found` | Activate the virtual environment, or run `python -m streamlit run app.py` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` with the environment active |
| Error about `width` argument | Upgrade Streamlit: `pip install -U streamlit` |

## Learning source
This project is based on a lesson from [CodeBasics.io](https://codebasics.io).

## Customize

| Change | Where |
|--------|-------|
| Add or edit personalities | `PERSONALITIES` in `chat_utils.py` |
| Change the default model | `GEMINI_MODEL` in `.env`, or `DEFAULT_MODEL` in `chat_utils.py` |
| Change the memory slider options | `memory_choice` in `app.py` |
| Change the theme | `.streamlit/config.toml` |
