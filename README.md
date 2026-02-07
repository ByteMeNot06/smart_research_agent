# Smart Research Agent

Single-agent web research assistant built with **LangChain**, **OpenRouter**, **Tavily**, and **Streamlit**.

This project implements a constrained, single-shot research agent that:

* Searches the web (once)
* Fetches selected pages (up to twice)
* Produces a structured research report
* Lists sources used

The agent follows a strict output format and tool-usage policy defined in `system.txt`.

---

## ✨ Features

* 🔎 Web search via Tavily API
* 📄 Page content extraction using BeautifulSoup
* 🤖 LLM-powered reasoning via OpenRouter
* 🧠 Strict single-shot research flow
* 📊 Structured output format:

  * Title
  * Executive Summary
  * Key Facts
  * Uncertainties / Conflicts
  * Sources
* 🖥 Streamlit UI
* 🧩 Clean modular architecture

---

## 🏗 Project Structure

```
smart_research_agent/
├── pyproject.toml
├── .env_example
├── src/
│   └── smart_research_agent/
│       └── app/
│           ├── agent.py
│           ├── config.py
│           ├── ui.py
│           ├── prompts/
│           │   └── system.txt
│           └── tools/
│               ├── web_search.py
│               └── fetch_page.py
```

---

## ⚙️ Requirements

* Python **3.10+**
* OpenRouter API key
* Tavily API key

---

## 🔑 Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd smart_research_agent
```

### 2. Create environment variables

Copy the example:

```bash
cp .env_example .env
```

Add your keys:

```
OPENROUTER_API_KEY=sk-...
TAVILY_API_KEY=...
```

Or export manually:

```bash
export OPENROUTER_API_KEY=your_key
export TAVILY_API_KEY=your_key
```

(Use `setx` on Windows.)

---

### 3. Create virtual environment and install dependencies

If using `uv`:

```bash
uv venv
uv pip install -e .
```

Or using pip:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
```

---

## 🚀 Running the App

From the project root:

```bash
streamlit run src/smart_research_agent/app/ui.py
```

Then open the local Streamlit URL in your browser.

---

## 🧠 How It Works

### 1. Agent Construction

`agent.py`:

* Loads system prompt from `prompts/system.txt`
* Initializes `ChatOpenAI` with OpenRouter base URL
* Registers tools:

  * `web_search`
  * `fetch_page`
* Creates a LangChain agent

---

### 2. Tooling

#### 🔎 `web_search`

* Uses Tavily API
* Returns formatted:

  * Title
  * Snippet
  * URL
* Limited to `MAX_SEARCH_RESULTS = 5`

#### 📄 `fetch_page`

* Fetches webpage content
* Removes scripts/styles
* Extracts visible text
* Truncates to `MAX_FETCH_CHARS = 4000`
* Never raises exceptions (returns diagnostic strings instead)

---

### 3. Research Constraints

Defined in `system.txt`:

* Web search: **max 1**
* Page fetch: **max 2**
* No follow-up questions
* No retries
* Must produce structured output
* Must list URLs in "Sources"

This ensures:

* Deterministic behavior
* Low cost
* Controlled execution

---

## 📌 Configuration

`config.py`:

```python
MODEL_NAME = "google/gemini-2.5-flash-lite"
MAX_SEARCH_RESULTS = 5
MAX_FETCH_CHARS = 4000
```

You can modify:

* Model
* Search depth
* Fetch size

---

## 📤 Output Format

The agent always produces:

```
Title

Executive Summary
(under 120 words)

Key Facts
- Bullet points only

Uncertainties / Conflicts
- Bullet points only

Sources
- URLs only
```

If information is insufficient, it explicitly states so.

---

## 🛠 Tech Stack

* LangChain
* LangChain OpenAI
* Tavily
* Streamlit
* BeautifulSoup
* Requests
* OpenRouter
* Gemini Flash Lite

---

## 🔒 Error Handling

* `fetch_page` never throws exceptions
* Failed fetches return tagged diagnostics:

  * `[FETCH_FAILED]`
  * `[FETCH_EMPTY]`
  * `[FETCH_ERROR]`
* Missing API keys raise startup errors

---

## 📈 Possible Improvements

* Add caching layer
* Add structured citation tracking
* Add rate limiting
* Add retry policies (currently disallowed by prompt)
* Add multi-step research mode
* Add streaming responses
* Add Docker support
* Add unit tests

---

## 🧪 Example Research Topics

* “Solid-state batteries in EVs”
* “Recent advances in fusion energy”
* “Impact of AI regulation in the EU”
* “Latest developments in carbon capture”

---

## 📄 License

Add your preferred license here.

---
