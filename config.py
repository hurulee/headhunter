import os

from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "lmstudio")
LLM_MODEL = os.environ.get("LLM_MODEL", "gemma-4-e4b-it")
LM_STUDIO_HOST = os.environ.get("LM_STUDIO_HOST", "127.0.0.1")
LM_STUDIO_BASE = f"http://{LM_STUDIO_HOST}:1234/v1"
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")


def create_llm():
    """Create and return the LLM based on the configured provider."""
    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=LLM_MODEL)
    elif LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=LLM_MODEL)
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            base_url=LM_STUDIO_BASE,
            api_key="lm-studio",
            model=LLM_MODEL,
        )
