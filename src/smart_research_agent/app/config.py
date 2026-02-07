import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY is not set")

MODEL_NAME = "google/gemini-2.5-flash-lite"

MAX_SEARCH_RESULTS = 5
MAX_FETCH_CHARS = 4000