import streamlit as st
import json
import typing


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
    st.markdown(
        """
    <div class="empty-state">
      <div class="empty-icon">✦</div>
      <h2>Ask your data anything</h2>
      <p>SmartBI translates your plain-English questions into SQL and returns answers with insights.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

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

    st.markdown("</div>", unsafe_allow_html=True)


def render_message(role: str, content: str, thought: typing.Union[str, None]):
    if role == "user":
        st.markdown(
            f"""
        <div class="message-row user">
            <div class="bubble user">{content}<button class="copy-btn" onclick="navigator.clipboard.writeText({json.dumps(content)})" style="margin-left:8px; cursor:pointer;">📋</button></div>
          <div class="avatar user">👤</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        if thought:
            with st.expander("Show thinking"):
                st.markdown(
                    f"""
                {thought}
                """,
                    unsafe_allow_html=True,
                )
        st.markdown(
            f"""
        <div class="message-row assistant">
          <div class="avatar assistant">BI</div>
            <div class="bubble assistant">{content}<button class="copy-btn" onclick="navigator.clipboard.writeText({json.dumps(content)})" style="margin-left:8px; cursor:pointer;">📋</button></div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_messages():
    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"], msg["thought"])
