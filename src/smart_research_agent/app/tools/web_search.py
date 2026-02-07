from langchain.tools import tool
from tavily import TavilyClient

from smart_research_agent.app.config import TAVILY_API_KEY, MAX_SEARCH_RESULTS

client = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def web_search(query: str) -> str:
    """
    Search the web for factual information.
    """
    results = client.search(
        query=query,
        max_results=MAX_SEARCH_RESULTS,
        include_raw_content=False
    )

    formatted = []
    for r in results.get("results", []):
        formatted.append(
            f"Title: {r.get('title')}\n"
            f"Snippet: {r.get('content')}\n"
            f"URL: {r.get('url')}\n"
        )

    return "\n---\n".join(formatted)
