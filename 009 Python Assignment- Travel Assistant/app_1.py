"""AI Travel Assistant: starter file for the assignment.

Learning source: CodeBasics.io (Python for AI course)
Build your own version here. The finished solution is in app_solution.py.
Run with:  streamlit run app_1.py
"""
import streamlit as st

st.title("AI Travel Assistant")
st.write("Build your interactive UI here!")

# Hint: Use st.session_state to store your chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Write your Streamlit code here...
