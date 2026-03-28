import streamlit as st
import time
import sys
import os
import asyncio
import sqlite3
from datetime import datetime


async def setup_session(session_service, session_id):
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    if not session:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state={},
        )


def get_user_sessions():
    """Fetch all sessions for the current user and app from the database."""
    try:
        conn = sqlite3.connect("data/session_data.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, create_time, update_time 
            FROM sessions 
            WHERE app_name=? AND user_id=? 
            ORDER BY create_time DESC
        """,
            (APP_NAME, USER_ID),
        )
        sessions = cursor.fetchall()
        conn.close()
        return sessions
    except Exception as e:
        st.error(f"Error fetching sessions: {e}")
        return []


def load_chat_history(session_id):
    """Load chat history for a specific session from the events table."""
    try:
        conn = sqlite3.connect("data/session_data.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, timestamp, event_data
            FROM events
            WHERE app_name=? AND user_id=? AND session_id=?
            ORDER BY timestamp ASC
        """,
            (APP_NAME, USER_ID, session_id),
        )
        events = cursor.fetchall()
        conn.close()

        messages = []
        for event_id, timestamp_str, event_data_str in events:
            try:
                import json

                event_data = json.loads(event_data_str)

                # Extract user messages
                if event_data.get("content", {}).get("role") == "user":
                    parts = event_data.get("content", {}).get("parts", [])
                    for part in parts:
                        if "text" in part:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": part["text"],
                                    "thought": None,
                                }
                            )

                # Extract assistant messages (model responses)
                elif event_data.get("content", {}).get("role") == "model":
                    parts = event_data.get("content", {}).get("parts", [])
                    text_content = ""
                    thought_content = ""

                    for part in parts:
                        if "text" in part:
                            # Check if this is a thought (look for thought indicator)
                            if part.get("thought", False) or "thought" in str(part):
                                thought_content += part["text"]
                            else:
                                text_content += part["text"]

                    if text_content:
                        messages.append(
                            {
                                "role": "assistant",
                                "content": text_content,
                                "thought": thought_content if thought_content else None,
                            }
                        )

            except (json.JSONDecodeError, KeyError) as e:
                # Skip malformed events
                continue

        return messages
    except Exception as e:
        st.error(f"Error loading chat history: {e}")
        return []


# Load styles
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from styles import load_css
from components import render_header, render_empty_state, render_messages
from adk_service import initialize_adk, run_adk_sync

load_css()

runner, session_service = initialize_adk()

SESSION_KEY = "adk_session_id"
APP_NAME = "smartbi_app"
USER_ID = "esha_user"

# Session state initialization
if SESSION_KEY not in st.session_state:
    session_id = f"session_{int(time.time())}"
    st.session_state[SESSION_KEY] = session_id
else:
    session_id = st.session_state[SESSION_KEY]

# Load chat history for current session if not already loaded
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = load_chat_history(session_id)

# ✅ Run async session setup
try:
    asyncio.run(setup_session(session_service, session_id))
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(setup_session(session_service, session_id))
    loop.close()


# Sidebar
with st.sidebar:
    if st.button("➕  New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.session_state.clear_input = False
        new_session_id = f"session_{int(time.time())}"
        st.session_state[SESSION_KEY] = new_session_id
        st.rerun(scope="app")

    # Display session history
    st.divider()
    st.caption("Chat History")

    sessions = get_user_sessions()
    if sessions:
        for session_id, create_time_str, update_time_str in sessions:
            # Parse the create time to format it nicely
            try:
                create_time = datetime.strptime(
                    create_time_str.split(".")[0], "%Y-%m-%d %H:%M:%S"
                )
                formatted_time = create_time.strftime("%b %d, %H:%M")
                button_label = f"Chat from {formatted_time}"
            except:
                button_label = f"Chat {session_id.split('_')[-1]}"

            # Highlight current session
            if session_id == st.session_state[SESSION_KEY]:
                if st.button(
                    button_label,
                    key=f"session_{session_id}",
                    type="primary",
                    use_container_width=True,
                ):
                    st.rerun(scope="app")
            else:
                if st.button(
                    button_label, key=f"session_{session_id}", use_container_width=True
                ):
                    # Load chat history for this session
                    st.session_state.messages = load_chat_history(session_id)
                    st.session_state.pending_query = None
                    st.session_state.clear_input = False
                    st.session_state[SESSION_KEY] = session_id
                    st.rerun(scope="app")
    else:
        st.caption("No previous chats")


# Page config
st.set_page_config(
    page_title="SmartBI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded",
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
            "thought": response["thought"],
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
