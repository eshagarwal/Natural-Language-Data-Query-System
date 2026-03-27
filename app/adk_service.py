import streamlit as st
import asyncio
import os

from google.adk.sessions.database_session_service import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types as genai_types

from business_analyst_agent.agent import root_agent

APP_NAME = "smartbi_app"
USER_ID = "esha_user"
SESSION_KEY = "adk_session_id"


@st.cache_resource
def initialize_adk():
    session_service = DatabaseSessionService("sqlite+aiosqlite:///./data/session_data.db")

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    return runner, session_service


async def run_adk_async(runner: Runner, session_id, query):
    def filter_thought(content_part: genai_types.Part) -> tuple[bool, str]:
        """
        Takes content part as input and filters for thought.

        Returns:
            tuple: bool, str
        """
        if content_part.thought is not None and content_part.thought == True:
            return True, content_part.text if content_part.text else ""
        if content_part.thought is None or (content_part.thought is not None and content_part.thought == False):
            return False, content_part.text if content_part.text else ""
        

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
    thought_text = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content is None:
                continue
            if event.content.parts is None:
                continue
            for part in event.content.parts:
                thought, text = filter_thought(part)
                if thought:
                    thought_text += f"\n{text}"
                else:
                    final_text += f"\n{text}"
        else:
            if event.content is None:
                continue
            if event.content.parts is None:
                continue
            for part in event.content.parts:
                thought, text = filter_thought(part)
                if thought:
                    thought_text += f"\n{text}"

    return final_text, thought_text


def run_adk_sync(runner, session_id, query):
    return asyncio.run(run_adk_async(runner, session_id, query))