# Quick Reference Guide: AI Travel Assistant

📚 Learning source: [CodeBasics.io](https://codebasics.io) · Solution by Peter Pandey

## Requirements
- Python 3.10 or newer
- A Google Gemini API key (free tier available)
- An internet connection

## Step 1: Get the project
- **Git:** `git clone <your-repo-url>` and `cd` into the folder
- **ZIP:** download it, right-click → **Extract All**, and open the folder in your terminal

## Step 2: Replace the API key placeholder ⚠️

| Step | macOS / Linux | Windows |
|------|---------------|---------|
| Copy the template | `cp .env.example .env` | `copy .env.example .env` |
| Edit it | Any text editor | Notepad or any editor |

In **`.env`**, change:
```text
GEMINI_API_KEY=your_actual_api_key_here
```
to your real key (from [Google AI Studio](https://aistudio.google.com/apikey)):
```text
GEMINI_API_KEY=AIza...your-real-key...
```
No quotes or spaces needed.

> 🔒 `.env` is in `.gitignore`, so it won't be uploaded. Never put your real key in `.env.example` or any `.py` file.

**Alternative:** skip `.env` and paste your key into **Gemini API key** in the app's sidebar. It's kept only for that browser session.

## Step 3: Install

| Option | Commands |
|--------|----------|
| **uv** (recommended) | `uv sync`, then `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`) |
| **pip** | `python -m venv .venv`, activate it, then `pip install -r requirements.txt` |

## Step 4: Run

| Task | Command |
|------|---------|
| Run the finished app | `streamlit run app_solution.py` (opens at http://localhost:8501) |
| Run your own version | `streamlit run app_1.py` |
| Stop the app | **Ctrl + C** in the terminal |

## Using the app

| I want to… | Do this |
|------------|---------|
| Plan a trip | Type in the chat box at the bottom; answer the assistant's questions |
| Get the final plan | Click **🗺️ Generate final itinerary** (enabled after your first message) |
| See each day | Open the **Day 1**, **Day 2**… sections |
| See the raw structured output | Open **Structured output (Pydantic JSON)** |
| Save the itinerary | **⬇️ Download JSON** or **⬇️ Download Markdown** |
| Update the plan | Keep chatting (e.g. "make it 5 days"), then click **Generate** again |
| Start over | Sidebar → **🔄 Start a new trip** |
| Use a different model | Sidebar → **Model** |
| Use a key without `.env` | Sidebar → **Gemini API key** |

**Good to know**
- The sidebar shows how many messages are in memory.
- Refreshing the browser tab starts a new conversation. Download your itinerary first if you want to keep it.

## Settings in `.env`

| Setting | Purpose | Default |
|---------|---------|---------|
| `GEMINI_API_KEY` | Your API key (required) | `your_actual_api_key_here` (placeholder) |
| `GEMINI_MODEL` | Model to use | `gemini-3.6-flash` |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No API key found" | Create `.env` from `.env.example` and add your key, then restart the app |
| "still contains the placeholder" | Replace `your_actual_api_key_here` in `.env` with your real key |
| "Your API key wasn't accepted" | Re-copy the full key from Google AI Studio |
| "That model isn't available" | Google retired the model. Set a current one in `GEMINI_MODEL` or the sidebar |
| "rate limit or free-tier quota" | Wait a minute and try again |
| "didn't match the expected format" | Click **Generate** again; add more trip details if it repeats |
| "plan covers X days" warning | The model planned the wrong number of days. Click **Generate** again |
| Changes to `.env` ignored | Restart the app; `.env` is read when it starts |
| Generate button greyed out | Send at least one message about your trip first |
| `ModuleNotFoundError: google.genai` | Activate the environment, then `uv sync` or `pip install -r requirements.txt` |
| `streamlit: command not found` | Activate the environment, or use `python -m streamlit run app_solution.py` |
| Windows shows `env.example` | Explorer may hide the leading dot; it's the same file |

## Customize

| Change | Where |
|--------|-------|
| Assistant's tone and questions | `SYSTEM_INSTRUCTION` in `travel_utils.py` |
| What the final itinerary must include | `FINAL_REQUEST` and the Pydantic models in `travel_utils.py` |
| Default model | `GEMINI_MODEL` in `.env`, or `DEFAULT_MODEL` in `travel_utils.py` |
| App colors | `.streamlit/config.toml` |
