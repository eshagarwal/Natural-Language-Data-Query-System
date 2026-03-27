import streamlit as st
import pandas as pd
import numpy as np
import time
import random

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
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F7F8FA !important;
    font-family: 'DM Sans', sans-serif;
    color: #1A1A2E;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── App container ── */
[data-testid="stAppViewContainer"] > .main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    padding: 0 !important;
}

.block-container {
    max-width: 760px !important;
    padding: 0 1rem 180px 1rem !important;
    margin: 0 auto !important;
}

/* ── Header bar ── */
.smartbi-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(247, 248, 250, 0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0,0,0,0.06);
    padding: 14px 0;
    text-align: center;
    margin-bottom: 8px;
}
.smartbi-header h1 {
    font-family: 'DM Sans', sans-serif;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: #1A1A2E;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}
.smartbi-header .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #3B82F6;
    display: inline-block;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── Empty state ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 20px 40px;
    text-align: center;
    opacity: 0;
    animation: fadeIn 0.6s ease 0.2s forwards;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.empty-icon {
    font-size: 48px;
    margin-bottom: 20px;
    filter: grayscale(20%);
}
.empty-state h2 {
    font-size: 22px;
    font-weight: 600;
    color: #1A1A2E;
    margin-bottom: 8px;
}
.empty-state p {
    font-size: 14px;
    color: #6B7280;
    max-width: 360px;
    line-height: 1.6;
}
.suggestion-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 24px;
}
.chip {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 13px;
    color: #374151;
    cursor: pointer;
    transition: all 0.15s ease;
    font-family: 'DM Sans', sans-serif;
}
.chip:hover {
    background: #EFF6FF;
    border-color: #BFDBFE;
    color: #1D4ED8;
}

/* ── Message bubbles ── */
.message-row {
    display: flex;
    margin-bottom: 16px;
    margin-top: 16px;
    animation: slideUp 0.25s ease;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.message-row.user  { justify-content: flex-end; }
.message-row.assistant { justify-content: flex-start; }

.bubble {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 14.5px;
    line-height: 1.65;
    word-break: break-word;
}
.bubble.user {
    background: #2563EB;
    color: white;
    border-bottom-right-radius: 6px;
}
.bubble.assistant {
    background: white;
    color: #1A1A2E;
    border: 1px solid #E5E7EB;
    border-bottom-left-radius: 6px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.avatar.assistant {
    background: #1A1A2E;
    color: white;
    margin-right: 10px;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.5px;
}
.avatar.user {
    background: #DBEAFE;
    color: #1D4ED8;
    margin-left: 10px;
    font-size: 16px;
}

/* ── Insight box ── */
.insight-box {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 12px;
    padding: 12px 16px;
    margin-top: 12px;
    font-size: 13.5px;
    color: #166534;
    line-height: 1.6;
}
.insight-box strong {
    font-weight: 600;
    display: block;
    margin-bottom: 4px;
    color: #15803D;
}

/* ── Table wrapper ── */
.table-wrapper {
    margin-top: 12px;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #E5E7EB;
}

/* ── Input dock ── */
.input-dock {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 200;
    background: linear-gradient(to top, #F7F8FA 70%, transparent);
    padding: 20px 16px 24px;
    pointer-events: none;
}
.input-inner {
    max-width: 760px;
    margin: 0 auto;
    pointer-events: all;
    display: flex;
    align-items: center;
    background: white;
    border: 1.5px solid #E5E7EB;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    padding: 4px 4px 4px 16px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.input-inner:focus-within {
    border-color: #3B82F6;
    box-shadow: 0 4px 20px rgba(59,130,246,0.15);
}
.input-inner input {
    flex: 1;
    border: none;
    outline: none;
    font-family: 'DM Sans', sans-serif;
    font-size: 14.5px;
    color: #1A1A2E;
    background: transparent;
    padding: 10px 0;
}
.input-inner input::placeholder { color: #9CA3AF; }
.send-btn {
    width: 38px; height: 38px;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    transition: all 0.15s ease;
    flex-shrink: 0;
}
.send-btn.active {
    background: #2563EB;
    color: white;
}
.send-btn.active:hover {
    background: #1D4ED8;
    transform: scale(1.05);
}
.send-btn.inactive {
    background: #F3F4F6;
    color: #D1D5DB;
    cursor: not-allowed;
}

/* ── Divider between messages & input ── */
.divider-hint {
    text-align: center;
    font-size: 11px;
    color: #D1D5DB;
    padding: 8px 0 4px;
}

/* ── Streamlit widget overrides ── */
[data-testid="stTextInput"] > div > div > input {
    border-radius: 14px !important;
    border: none !important;
    padding: 12px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14.5px !important;
    background: transparent !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: none !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    border: none !important;
    transition: all 0.15s ease !important;
}

/* stDataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Spinner */
[data-testid="stSpinner"] > div {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #6B7280 !important;
}

/* Chip buttons */
[data-testid="stButton"] button[kind="secondary"] {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 13px;
    color: #374151;
}

[data-testid="stButton"] button[kind="secondary"]:hover {
    background: #EFF6FF;
    border-color: #BFDBFE;
    color: #1D4ED8;
}

</style>
""",
    unsafe_allow_html=True,
)


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
