import streamlit as st
import time
import sys
import os
import asyncio


async def setup_session(session_service, session_id):
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    if not session:
        await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id, state={}
        )


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from styles import load_css
from components import render_header, render_empty_state, render_messages
from adk_service import initialize_adk, run_adk_sync

# Load styles
load_css()

runner, session_service = initialize_adk()

SESSION_KEY = "adk_session_id"
APP_NAME = "smartbi_app"
USER_ID = "esha_user"

import time

if SESSION_KEY not in st.session_state:
    session_id = f"session_{int(time.time())}"
    st.session_state[SESSION_KEY] = session_id
else:
    session_id = st.session_state[SESSION_KEY]

# ✅ Run async session setup
try:
    asyncio.run(setup_session(session_service, session_id))
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(setup_session(session_service, session_id))
    loop.close()

# Page config
st.set_page_config(
    page_title="SmartBI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False


# backend
def get_response(query: str):
    try:
        text, thought_text = run_adk_sync(runner, session_id, query)

        return {
            "text": text,
            "thought": thought_text,
        }

    except Exception as e:
        return {
            "text": "⚠️ Error processing query",
            "thought": "",
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

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response["text"],
            "thought": response["thought"]
        }
    )

    st.rerun()


# Input
st.markdown(
    '<div class="divider-hint">SmartBI may make mistakes — always verify critical figures</div>',
    unsafe_allow_html=True,
)

col_input, col_btn = st.columns([9, 1])

if st.session_state.clear_input:
    st.session_state.chat_input = ""
    st.session_state.clear_input = False

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
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query_text,
                "thought": None,
            }
        )

        st.session_state.pending_query = query_text
        st.session_state.clear_input = True

        st.rerun()
