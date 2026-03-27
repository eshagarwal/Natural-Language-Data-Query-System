import streamlit as st
import pandas as pd
import time
import random

from styles import load_css
from components import render_header, render_empty_state, render_messages

# Page config
st.set_page_config(
    page_title="SmartBI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Load styles
load_css()

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# Dummy backend
def get_response(query: str):
    time.sleep(random.uniform(0.8, 1.6))
    return {
        "text": "Sample response",
        "table": None,
        "insight": None,
    }


# UI
render_header()

if not st.session_state.messages:
    render_empty_state()
else:
    render_messages()


# Handle query
if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None

    with st.spinner("Thinking…"):
        response = get_response(query)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })

    st.rerun()


# Input
st.markdown(
    '<div class="divider-hint">SmartBI may make mistakes — always verify critical figures</div>',
    unsafe_allow_html=True,
)

col_input, col_btn = st.columns([9, 1])

with col_input:
    st.text_input(
        label="query",
        placeholder="Ask your data a question…",
        label_visibility="collapsed",
        key="chat_input",
    )

with col_btn:
    send_clicked = st.button(
        "↑",
        disabled=(not st.session_state.get("chat_input", "").strip()),
        use_container_width=True,
    )


if send_clicked:
    query_text = st.session_state.get("chat_input", "").strip()

    if query_text:
        st.session_state.messages.append({
            "role": "user",
            "content": {"text": query_text},
        })

        st.session_state.pending_query = query_text
        st.session_state.chat_input = ""

        st.rerun()