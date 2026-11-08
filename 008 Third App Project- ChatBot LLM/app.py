"""Chatbot with Memory: a Streamlit chat app powered by Google Gemini."""
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

import chat_utils as cu

load_dotenv()
st.set_page_config(page_title="Chatbot with Memory", page_icon="💬", layout="centered")

# The conversation list IS the memory. st.session_state keeps it alive across
# Streamlit's reruns (otherwise it would reset on every message).
if "conversation" not in st.session_state:
    st.session_state.conversation = []


def key_from_secrets() -> str | None:
    """Streamlit Cloud stores keys in st.secrets. Locally this file usually doesn't exist."""
    try:
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


@st.cache_data(ttl=3600, show_spinner=False)
def load_model_names(api_key: str) -> list[str]:
    # Errors are not cached by Streamlit, so a failed attempt is retried next time.
    return cu.chat_model_names(get_client(api_key).models.list())


def stream_reply(client: genai.Client, model: str, contents: list[dict], config: types.GenerateContentConfig):
    """Yield the reply piece by piece as Gemini writes it."""
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=config):
        if chunk.text:
            yield chunk.text


# ================= Sidebar =================
with st.sidebar:
    st.header("⚙️ Settings")

    # ---- API key ----
    env_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    sidebar_key = st.text_input(
        "Gemini API key (optional)",
        type="password",
        help="Only needed if you haven't put your key in the .env file. It's kept for this browser session only.",
    )
    api_key = cu.clean_key(sidebar_key) or cu.clean_key(key_from_secrets()) or cu.clean_key(env_key)

    # ---- Model ----
    default_model = os.getenv("GEMINI_MODEL", "").strip() or cu.DEFAULT_MODEL
    model_names, list_error = list(cu.FALLBACK_MODELS), None
    if api_key:
        try:
            model_names = load_model_names(api_key) or model_names
        except Exception as e:
            list_error = cu.friendly_error(e)
    if default_model not in model_names:
        model_names.insert(0, default_model)
    model = st.selectbox("Model", model_names, index=model_names.index(default_model))
    custom_model = st.text_input("…or type a model name", placeholder="e.g. gemini-flash-latest").strip()
    model = custom_model or model
    if list_error:
        st.caption(f"⚠️ Couldn't load the model list, so showing defaults. {list_error}")

    # ---- Personality ----
    personality = st.selectbox("Personality", list(cu.PERSONALITIES) + [cu.CUSTOM_PERSONALITY])
    if personality == cu.CUSTOM_PERSONALITY:
        system_instruction = st.text_area(
            "Describe the personality",
            placeholder="e.g. You are a cheerful chef who answers every question with a cooking tip.",
        ).strip()
    else:
        system_instruction = cu.PERSONALITIES[personality]

    # ---- Creativity ----
    set_temperature = st.checkbox(
        "Set creativity (temperature)",
        help="Leave this off to use the model's recommended default. Newer models work best at their default.",
    )
    temperature = st.slider("Creativity", 0.0, 2.0, 1.0, 0.1, help="Lower = focused, higher = more creative.") if set_temperature else None

    # ---- Memory ----
    st.subheader("🧠 Memory")
    memory_choice = st.select_slider(
        "Remember the last…",
        options=["1 exchange", "3 exchanges", "5 exchanges", "10 exchanges", "20 exchanges", "Everything"],
        value="Everything",
        help="How much of the conversation is re-sent to the model with each new message.",
    )
    max_exchanges = None if memory_choice == "Everything" else int(memory_choice.split()[0])

    convo = st.session_state.conversation
    sent = cu.messages_to_send(convo, max_exchanges)
    st.caption(f"{len(convo)} messages stored · the model sees the last {len(sent)}")

    col1, col2 = st.columns(2)
    if col1.button("🗑️ Clear chat", width="stretch", disabled=not convo):
        st.session_state.conversation = []
        st.rerun()
    if col2.button("↩️ Undo last", width="stretch", disabled=not convo):
        st.session_state.conversation = cu.undo_last_exchange(convo)
        st.rerun()

    # ---- Save and load ----
    st.subheader("💾 Save or load a chat")
    st.download_button(
        "Download as Markdown", cu.to_markdown(convo, model, personality),
        file_name="chat.md", mime="text/markdown", width="stretch", disabled=not convo,
    )
    st.download_button(
        "Download as JSON (can be reloaded)", cu.to_json(convo),
        file_name="chat.json", mime="application/json", width="stretch", disabled=not convo,
    )
    uploaded = st.file_uploader("Load a saved chat (.json)", type=["json"])
    if uploaded is not None and st.button("Load this chat", width="stretch"):
        try:
            st.session_state.conversation = cu.parse_saved_chat(uploaded.getvalue())
            st.rerun()
        except ValueError as e:
            st.error(str(e))

    st.divider()
    st.caption("📚 Learning source: [CodeBasics.io](https://codebasics.io)")

# ================= Main area =================
st.title("💬 Chatbot with Memory")
st.caption(f"Model: `{model}` · Personality: {personality}")

if not api_key:
    st.warning("**No API key found.** The chatbot needs a Gemini API key to work.")
    if cu.is_placeholder(env_key):
        st.info("Your `.env` file still contains the placeholder `your-api-key-here`. Replace it with your real key and restart the app.")
    st.markdown(
        "1. Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).\n"
        "2. Copy `.env.example` to a new file named `.env`.\n"
        "3. In `.env`, replace `your-api-key-here` with your key.\n"
        "4. Restart the app (`Ctrl + C`, then `streamlit run app.py`).\n\n"
        "Or paste the key into **Gemini API key** in the sidebar for this session."
    )
    st.stop()

# Show the whole conversation so far
for message in st.session_state.conversation:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(cu.message_text(message))

with st.expander("🔍 Peek inside the memory"):
    st.caption("This is the exact list sent to Gemini with your next message.")
    st.json(cu.messages_to_send(st.session_state.conversation, max_exchanges), expanded=False)

# Take new input from the user
user_input = st.chat_input("Say something...")

if user_input:
    # 1. add the user's message to memory and show it
    st.session_state.conversation.append(cu.make_message("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. send the remembered conversation so the model has context
    contents = cu.messages_to_send(st.session_state.conversation, max_exchanges)
    config = types.GenerateContentConfig(
        system_instruction=system_instruction or None,
        temperature=temperature,
    )
    reply, error = "", None
    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(stream_reply(get_client(api_key), model, contents, config))
            if not isinstance(reply, str):  # write_stream returns a list if nothing was written
                reply = "".join(str(r) for r in reply)
            if not reply.strip():
                error = "The model returned an empty reply, possibly because of its safety filters. Try rephrasing."
        except Exception as e:
            error = cu.friendly_error(e)
        if error:
            st.error(error)

    # 3. add the reply to memory. If it failed, take the user's message back out,
    #    so the error never becomes part of the memory sent next time.
    if error:
        st.session_state.conversation.pop()
        st.caption("Your message wasn't saved. Fix the problem above and send it again.")
    else:
        st.session_state.conversation.append(cu.make_message("model", reply))
        st.rerun()  # refresh the sidebar counts and download buttons
