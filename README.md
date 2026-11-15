# Headhunter - Career Guidance Agent

A multi-agent AI system built with LangChain and LangGraph that helps you explore your career history and research new directions. Powered by a local LLM via LM Studio (or optionally Anthropic/OpenAI).

## How it works

An **Orchestrator** classifies each message and routes it to one of two agents:

- **Discovery Agent** — reflects on your background, work history, skills, and experiences using your personal documents
- **Research Agent** — searches both your documents and the web (via Tavily) for job market data, salary ranges, career paths, and industry trends

## Prerequisites

- **Python 3.10+**
- **LM Studio** running locally on port 1234 with the following models loaded:
  - `google/gemma-4-12b-qat` (chat model)
  - `text-embedding-nomic-embed-text-v1.5` (embedding model)
- **Tavily API key** — free tier available at tavily.com — required for web search

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```
TAVILY_API_KEY=your_tavily_api_key_here
```

Optional overrides:

```
LLM_PROVIDER=lmstudio        # or: anthropic, openai
LLM_MODEL=google/gemma-4-12b-qat     # model name for the chosen provider
LM_STUDIO_HOST=127.0.0.1     # hostname where LM Studio is running
ANTHROPIC_API_KEY=...         # required if LLM_PROVIDER=anthropic
OPENAI_API_KEY=...            # required if LLM_PROVIDER=openai
```

### 4. Add your documents

The `knowledge/` folder is **not included in this repository** — it's gitignored so that personal documents are never committed or pushed. You need to create it yourself and add your own files:

```bash
mkdir knowledge
```

Then place your `.pdf`, `.txt`, or `.md` files directly in the `knowledge/` folder (subfolders are supported too). The agent will load and index everything in it on startup. Typical documents include your resume, performance reviews, and notes about past projects.

> **Note:** Anything you put in `knowledge/` stays local — it's excluded from version control, so it won't be pushed to the remote.

## Starting LM Studio

1. Open **LM Studio** and go to the **Developer** tab (`<->` icon in the left sidebar)
2. Click **Start Server** — it should show `Server running on port 1234`
3. Under **Loaded Models**, load both:
   - `google/gemma-4-12b-qat`
   - `text-embedding-nomic-embed-text-v1.5`

## Running locally

With LM Studio running and both models loaded:

```bash
python main.py
```

## Running with Docker

### Build the image

```bash
docker build -t headhunter .
```

### Run the container

```bash
docker run -it \
  -e LM_STUDIO_HOST=host.docker.internal \
  -e TAVILY_API_KEY=your_key_here \
  headhunter
```

- `-it` enables interactive mode
- `LM_STUDIO_HOST=host.docker.internal` allows the container to reach LM Studio on your host machine

### Stop the container

Type `quit`, `exit`, or `q` at the `You:` prompt, or press `Ctrl+C`.

## Features

- **Career discovery** — reflects on your work history, skills, and experiences from your personal documents
- **Job market research** — searches the web for roles, salaries, and industry trends
- **Document knowledge base (RAG)** — indexes resumes, performance reviews, and other `.pdf`/`.txt`/`.md` files you add to a local, gitignored `knowledge/` folder
- **Conversational memory** — remembers context within a session
- **Multiple LLM providers** — LM Studio (default), Anthropic, or OpenAI via environment variables
