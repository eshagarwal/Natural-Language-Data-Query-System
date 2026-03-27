import streamlit as st

def load_css():
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
