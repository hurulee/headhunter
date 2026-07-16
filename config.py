import os

from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "lmstudio")
LLM_MODEL = os.environ.get("LLM_MODEL", "google/gemma-4-12b-qat")
LM_STUDIO_HOST = os.environ.get("LM_STUDIO_HOST", "127.0.0.1")
LM_STUDIO_BASE = f"http://{LM_STUDIO_HOST}:1234/v1"
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")

# Context management. The conversation history grows every turn, and once the
# prompt approaches the model's context window the reply gets truncated
# mid-sentence (finish_reason="length"). SummarizationMiddleware condenses the
# older turns once the history crosses SUMMARY_TRIGGER_TOKENS, keeping the most
# recent SUMMARY_KEEP_MESSAGES intact. Set CONTEXT_WINDOW to the context length
# loaded in LM Studio; the trigger defaults to half of it, leaving room for the
# system prompt + the model's reply (a reasoning model can spend 600-1000 tokens
# thinking on top of the visible answer).
CONTEXT_WINDOW = int(os.environ.get("CONTEXT_WINDOW", "8192"))
SUMMARY_TRIGGER_TOKENS = int(os.environ.get("SUMMARY_TRIGGER_TOKENS", str(CONTEXT_WINDOW // 2)))
SUMMARY_KEEP_MESSAGES = int(os.environ.get("SUMMARY_KEEP_MESSAGES", "6"))


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
