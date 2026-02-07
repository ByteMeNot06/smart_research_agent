import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

from smart_research_agent.app.config import MAX_FETCH_CHARS


@tool
def fetch_page(url: str) -> str:
    """
    Fetch and extract main text content from a web page.

    This tool MUST NOT raise exceptions.
    On failure, it returns a short diagnostic string.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)

        if resp.status_code != 200:
            return f"[FETCH_FAILED] HTTP {resp.status_code} for {url}"

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)

        if not text.strip():
            return f"[FETCH_EMPTY] No readable text extracted from {url}"

        return text[:MAX_FETCH_CHARS]

    except requests.RequestException as e:
        return f"[FETCH_ERROR] {type(e).__name__}: {e}"
