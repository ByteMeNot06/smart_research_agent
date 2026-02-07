from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from smart_research_agent.app.config import MODEL_NAME, OPENROUTER_API_KEY
from smart_research_agent.app.tools.web_search import web_search
from smart_research_agent.app.tools.fetch_page import fetch_page

SYSTEM_PROMPT_PATH = Path(__file__).parent / "prompts" / "system.txt"


def build_agent():
    system_prompt = SYSTEM_PROMPT_PATH.read_text()

    llm = ChatOpenAI(
        model=MODEL_NAME,
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2,
    ).with_config(
        {"system_message": system_prompt}
    )

    tools = [web_search, fetch_page]

    agent = create_agent(
        model=llm,
        tools=tools,
    )

    return agent
