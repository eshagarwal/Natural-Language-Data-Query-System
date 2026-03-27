import streamlit as st
import asyncio

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types as genai_types

from business_analyst_agent.agent import root_agent

APP_NAME = "smartbi_app"
USER_ID = "esha_user"
SESSION_KEY = "adk_session_id"


@st.cache_resource
def initialize_adk():
    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    return runner, session_service


async def run_adk_async(runner, session_id, query):
    session = runner.session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    content = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=query)],
    )

    final_text = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_text = event.content.parts[0].text
                break

    return final_text


def run_adk_sync(runner, session_id, query):
    return asyncio.run(run_adk_async(runner, session_id, query))