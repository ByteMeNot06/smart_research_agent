import streamlit as st
from typing import Any

from smart_research_agent.app.agent import build_agent

st.set_page_config(page_title="Smart Research Agent", layout="wide")

st.title("Smart Web Research Assistant")

topic = st.text_input(
    "Research topic",
    placeholder="e.g. Solid-state batteries in EVs"
)


def extract_final_answer(result: Any) -> str:
    """
    Extract the final human-readable answer from LangGraph output.
    """
    if not isinstance(result, dict):
        return str(result)

    messages = result.get("messages", [])
    if not messages:
        return "No response generated."

    # Walk backwards to find the last AI message with content
    for msg in reversed(messages):
        content = getattr(msg, "content", None)
        if isinstance(content, str) and content.strip():
            return content

    return "No readable output produced."


def extract_sources(result: Any) -> list[str]:
    """
    Extract URLs from ToolMessage content (best-effort).
    """
    sources = []

    if not isinstance(result, dict):
        return sources

    for msg in result.get("messages", []):
        if msg.__class__.__name__ == "ToolMessage":
            text = getattr(msg, "content", "")
            for line in text.splitlines():
                if line.startswith("URL:"):
                    sources.append(line.replace("URL:", "").strip())

    return sorted(set(sources))


if st.button("Run research") and topic:
    with st.spinner("Researching..."):
        agent = build_agent()
        result = agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": topic}
                ]
            }
        )

    # ---- Main Answer ----
    st.subheader("Answer")
    final_answer = extract_final_answer(result)
    st.markdown(final_answer)

    # ---- Sources ----
    sources = extract_sources(result)
    if sources:
        st.subheader("Sources")
        for url in sources:
            st.markdown(f"- {url}")

    # ---- Debug (collapsed) ----
    with st.expander("Debug: raw agent trace"):
        st.write(result)
