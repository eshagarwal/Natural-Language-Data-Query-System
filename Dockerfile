FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /my_app
COPY pyproject.toml ./
COPY uv.lock ./
COPY .python-version ./
COPY ./data ./data
COPY ./server ./server
COPY ./business_analyst_agent ./business_analyst_agent
COPY ./app ./app

RUN uv sync --locked --no-dev

ENV PYTHONUNBUFFERED=1

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app/smartbi.py", "--server.address=0.0.0.0", "--server.port=8501"]