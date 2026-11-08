"""AI Travel Assistant: Streamlit solution.

Solution by Peter Pandey · Learning source: CodeBasics.io (Python for AI course)
Run with:  streamlit run app_solution.py
"""
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

import travel_utils as tu

load_dotenv()
st.set_page_config(page_title="AI Travel Assistant", page_icon="✈️", layout="centered")

# Memory: kept in session_state so it survives Streamlit's reruns.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None


@st.cache_resource(show_spinner=False)
def get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def stream_reply(client, model, contents):
    """Yield the chat reply piece by piece as Gemini writes it."""
    config = types.GenerateContentConfig(system_instruction=tu.SYSTEM_INSTRUCTION)
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=config):
        if chunk.text:
            yield chunk.text


def generate_itinerary(client, model, chat_history) -> tu.TravelItinerary:
    """Ask for the final itinerary, forcing the TravelItinerary schema."""
    response = client.models.generate_content(
        model=model,
        contents=tu.itinerary_request(chat_history),
        config=types.GenerateContentConfig(
            system_instruction=tu.SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=tu.TravelItinerary,
        ),
    )
    return tu.parse_itinerary(response)


# ================= Sidebar =================
with st.sidebar:
    st.header("⚙️ Settings")
    env_key = os.getenv("GEMINI_API_KEY")
    sidebar_key = st.text_input(
        "Gemini API key (optional)", type="password",
        help="Only needed if you haven't put your key in the .env file. Kept for this browser session only.",
    )
    api_key = tu.clean_key(sidebar_key) or tu.clean_key(env_key)
    st.caption("✅ API key found" if api_key else "⚠️ No API key yet")

    model = st.text_input("Model", value=os.getenv("GEMINI_MODEL", "").strip() or tu.DEFAULT_MODEL).strip() or tu.DEFAULT_MODEL

    user_turns = sum(1 for m in st.session_state.chat_history if m["role"] == "user")
    st.caption(f"🧠 Memory: {len(st.session_state.chat_history)} messages ({user_turns} from you)")

    if st.button("🔄 Start a new trip", width="stretch", disabled=not st.session_state.chat_history):
        st.session_state.chat_history = []
        st.session_state.itinerary = None
        st.rerun()

    st.divider()
    st.caption("Solution by **Peter Pandey**\n\n📚 Learning source: [CodeBasics.io](https://codebasics.io)")

# ================= Main =================
st.title("✈️ AI Travel Assistant")
st.caption("Tell me where you'd like to go, for how long, your budget and what you enjoy. "
           "When you're ready, generate your final itinerary.")

if not api_key:
    st.warning("**No API key found.** The assistant needs a Gemini API key to work.")
    if tu.is_placeholder(env_key):
        st.info("Your `.env` file still contains the placeholder `your_actual_api_key_here`. "
                "Replace it with your real key and restart the app.")
    st.markdown(
        "1. Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).\n"
        "2. Copy `.env.example` to a new file named `.env`.\n"
        "3. In `.env`, replace `your_actual_api_key_here` with your key.\n"
        "4. Restart the app (`Ctrl + C`, then `streamlit run app_solution.py`).\n\n"
        "Or paste the key into the sidebar for this session."
    )
    st.stop()

client = get_client(api_key)

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(tu.message_text(message))

# ---------- Final itinerary ----------
has_preferences = any(m["role"] == "user" for m in st.session_state.chat_history)
if st.button("🗺️ Generate final itinerary", type="primary", disabled=not has_preferences,
             help="Share your trip preferences in the chat first."):
    with st.spinner("Compiling your structured itinerary..."):
        try:
            st.session_state.itinerary = generate_itinerary(client, model, st.session_state.chat_history)
        except Exception as e:
            st.error(tu.friendly_error(e))

itinerary = st.session_state.itinerary
if itinerary:
    st.success("Itinerary generated!")
    with st.container(border=True):
        st.subheader(f"📍 {itinerary.destination}")
        c1, c2 = st.columns(2)
        c1.metric("Duration", f"{itinerary.duration_days} days")
        c2.metric("Budget", itinerary.budget_category)
        st.markdown("**Highlights:** " + " · ".join(itinerary.activities))
        for warning in tu.itinerary_warnings(itinerary):
            st.warning(warning)
        for day in sorted(itinerary.daily_itinerary, key=lambda d: d.day):
            with st.expander(f"Day {day.day}", expanded=day.day == 1):
                st.write(day.plan)
        with st.expander("Structured output (Pydantic JSON)"):
            st.json(itinerary.model_dump())
        d1, d2 = st.columns(2)
        d1.download_button("⬇️ Download JSON", itinerary.model_dump_json(indent=2),
                           "itinerary.json", "application/json", width="stretch")
        d2.download_button("⬇️ Download Markdown", tu.itinerary_to_markdown(itinerary),
                           "itinerary.md", "text/markdown", width="stretch")

# ---------- Chat ----------
if prompt := st.chat_input("Where do you want to go?"):
    st.session_state.chat_history.append(tu.make_message("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    error = None
    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(stream_reply(client, model, st.session_state.chat_history))
            if not isinstance(reply, str):
                reply = "".join(str(r) for r in reply)
            if not reply.strip():
                error = "The model returned an empty reply, possibly because of its safety filters. Try rephrasing."
        except Exception as e:
            error = tu.friendly_error(e)
        if error:
            st.error(error)

    if error:
        # Keep the memory clean: remove the question that didn't get an answer.
        st.session_state.chat_history.pop()
    else:
        st.session_state.chat_history.append(tu.make_message("model", reply))
        st.rerun()
