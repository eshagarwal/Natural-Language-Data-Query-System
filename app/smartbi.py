import streamlit as st
import pandas as pd
import numpy as np
import time
import random

from styles import load_css

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartBI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# LOAD CSS
# ─────────────────────────────────────────────
load_css()


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# ─────────────────────────────────────────────
# DUMMY BACKEND  (replace with real agent call)
# ─────────────────────────────────────────────
SAMPLE_RESPONSES = [
    {
        "text": "Here are the top 5 sellers by total revenue for the last quarter.",
        "table": pd.DataFrame(
            {
                "Seller ID": ["S-0041", "S-0183", "S-0092", "S-0307", "S-0256"],
                "Orders": [1_243, 987, 1_102, 834, 761],
                "Revenue (R$)": [84_320.50, 72_415.00, 68_900.75, 61_250.00, 57_880.25],
                "Avg Rating": [4.6, 4.3, 4.8, 4.1, 4.5],
            }
        ),
        "insight": "Seller S-0041 leads in revenue despite having fewer orders than S-0092, "
        "indicating a higher average order value. Consider studying their product mix.",
    },
    {
        "text": "The monthly order trend shows consistent growth through Q3 with a notable dip in September.",
        "table": pd.DataFrame(
            {
                "Month": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                "Orders": [4_210, 4_590, 3_980, 5_120, 6_340, 7_890],
                "Revenue (R$)": [312_000, 341_500, 295_000, 388_000, 481_000, 602_000],
            }
        ),
        "insight": "The September dip is consistent with Brazil's low season. "
        "November–December spike aligns with Black Friday and holiday shopping.",
    },
    {
        "text": "Product category breakdown by order volume.",
        "table": pd.DataFrame(
            {
                "Category": [
                    "Health & Beauty",
                    "Electronics",
                    "Toys & Games",
                    "Home & Kitchen",
                    "Fashion",
                ],
                "Orders": [8_421, 6_302, 5_190, 4_870, 3_650],
                "Avg Price (R$)": [89.90, 312.50, 65.00, 128.40, 145.20],
                "Return Rate (%)": [2.1, 4.7, 1.8, 3.2, 5.6],
            }
        ),
        "insight": "Electronics has the highest return rate at 4.7%. "
        "Health & Beauty dominates volume with a low return rate, making it the most efficient category.",
    },
    {
        "text": "Average delivery time by region.",
        "table": pd.DataFrame(
            {
                "State": ["SP", "RJ", "MG", "BA", "RS"],
                "Avg Delivery (days)": [6.2, 8.1, 9.4, 14.3, 11.7],
                "On-Time Rate (%)": [92, 87, 84, 71, 78],
            }
        ),
        "insight": "São Paulo benefits from proximity to most fulfilment centres. "
        "Bahia shows the lowest on-time rate — consider regional warehouse partnerships.",
    },
]


def get_response(query: str) -> dict:
    """Simulated backend. Replace with real MCP / BI-agent call."""
    time.sleep(random.uniform(0.8, 1.6))  # simulate latency
    return random.choice(SAMPLE_RESPONSES)


# ─────────────────────────────────────────────
# UI RENDERING HELPERS
# ─────────────────────────────────────────────
def render_header():
    st.markdown(
        """
    <div class="smartbi-header">
      <h1><span class="dot"></span> SmartBI</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    # Top static HTML
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">✦</div>
      <h2>Ask your data anything</h2>
      <p>SmartBI translates your plain-English questions into SQL and returns answers with insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Chips container start
    st.markdown('<div class="suggestion-chips">', unsafe_allow_html=True)

    chips = [
        "Top sellers last quarter",
        "Monthly order trend",
        "Category breakdown",
        "Avg delivery time by state",
    ]

    cols = st.columns(len(chips))

    for i, chip in enumerate(chips):
        with cols[i]:
            if st.button(chip, key=f"chip_{i}"):
                st.session_state.chat_input = chip
                st.rerun()

    # Chips container end
    st.markdown('</div>', unsafe_allow_html=True)

def render_message(role: str, content: dict):
    """Render a single chat message."""
    if role == "user":
        st.markdown(
            f"""
        <div class="message-row user">
          <div class="bubble user">{content['text']}</div>
          <div class="avatar user">👤</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    else:  # assistant
        st.markdown(
            f"""
        <div class="message-row assistant">
          <div class="avatar assistant">BI</div>
          <div class="bubble assistant">{content['text']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if content.get("table") is not None:
            st.dataframe(
                content["table"],
                use_container_width=True,
                hide_index=True,
            )

        if content.get("insight"):
            st.markdown(
                f"""
            <div class="insight-box">
              <strong>✦ Insight</strong>
              {content['insight']}
            </div>
            """,
                unsafe_allow_html=True,
            )


def render_messages():
    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"])


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
render_header()

# ── Conversation area ──────────────────────────
if not st.session_state.messages:
    render_empty_state()
else:
    render_messages()

# ── Process pending query (keeps spinner inside chat area) ──
if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None

    with st.spinner("Thinking…"):
        response = get_response(query)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
    st.rerun()

# ── Hint above input ───────────────────────────
st.markdown(
    '<div class="divider-hint">SmartBI may make mistakes — always verify critical figures</div>',
    unsafe_allow_html=True,
)

# ── Input row ──────────────────────────────────
col_input, col_btn = st.columns([9, 1])

with col_input:
    user_input = st.text_input(
        label="query",
        placeholder="Ask your data a question…",
        label_visibility="collapsed",
        key="chat_input",
    )

with col_btn:
    send_clicked = st.button(
        "↑",
        disabled=(not st.session_state.get("chat_input", "").strip()),  # FIX
        use_container_width=True,
        key="send_btn",
    )

# ── Handle send ────────────────────────────────
if send_clicked:
    query_text = st.session_state.get("chat_input", "").strip()
    if query_text:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": {"text": query_text},
            }
        )
        st.session_state.pending_query = query_text

        # clear input
        st.session_state.chat_input = ""

        st.rerun()
