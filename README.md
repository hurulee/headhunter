# Headhunter - AI Chat Agent

A conversational AI agent built with LangChain and LangGraph, powered by a local LLM via LM Studio. The agent can chat, perform calculations, and answer questions from your own documents (RAG).

## Prerequisites

- **Python 3.10+**
- **LM Studio** running locally on port 1234 with the following models loaded:
  - `gemma-4-E4B-it` (chat model)
  - `text-embedding-nomic-embed-text-v1.5` (embedding model)
- **Docker Desktop** (optional, for running in a container)

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add documents

Place `.pdf` or `.txt` files in the `knowledge/` folder. The agent will load and index them on startup.

## Running locally

Make sure LM Studio is running, then:

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
docker run -it -e LM_STUDIO_HOST=host.docker.internal headhunter
```

- `-it` enables interactive mode so you can chat
- `-e LM_STUDIO_HOST=host.docker.internal` allows the container to reach LM Studio on your Mac

### Verify the container is running

```bash
docker ps
```

### Stop the container

Type `quit`, `exit`, or `q` at the `You:` prompt, or press `Ctrl+C`.

## Features

- **General chat** - talk about any topic
- **Calculator** - add, subtract, multiply, divide (e.g. "What is 6 times 7, plus 10?")
- **Document search (RAG)** - ask questions about documents in the `knowledge/` folder
- **Chat history** - remembers conversation context within a session
