import os
import sys
from datetime import datetime

from config import create_llm, LM_STUDIO_BASE, KNOWLEDGE_DIR, LLM_PROVIDER, LLM_MODEL, CONTEXT_WINDOW
from agents.discovery import create_discovery_agent
from agents.research import create_research_agent
from agents.orchestrator import Orchestrator

# Set DEBUG_MESSAGES=1 to print the full message history after every turn. Handy
# for watching SummarizationMiddleware fire: the list grows, then suddenly
# collapses into a summary message plus the most recent few messages.
DEBUG_MESSAGES = os.environ.get("DEBUG_MESSAGES", "0") == "1"

# Set DEBUG_LOG_FILE=some.txt to mirror everything printed to the terminal into
# that file too (appended), so you can review a whole session without scrolling.
DEBUG_LOG_FILE = os.environ.get("DEBUG_LOG_FILE")


class _Tee:
    """Write everything sent to stdout to several streams (console + file)."""

    def __init__(self, *streams):
        self._streams = streams

    def write(self, data):
        for stream in self._streams:
            stream.write(data)
            stream.flush()
        return len(data)

    def flush(self):
        for stream in self._streams:
            stream.flush()


def _is_summary(message):
    # SummarizationMiddleware injects its summary as a HumanMessage tagged with
    # this marker (see langchain .../middleware/summarization.py).
    return getattr(message, "additional_kwargs", {}).get("lc_source") == "summarization"


def _summary_text(messages):
    for m in messages:
        if _is_summary(m):
            return m.content
    return None


def _last_prompt_tokens(messages):
    # The model reports how many prompt tokens it actually processed for the most
    # recent call. After SummarizationMiddleware fires, the history sent to the
    # model shrinks, so this number drops -- the clearest metric of it working.
    for m in reversed(messages):
        usage = getattr(m, "usage_metadata", None)
        if usage and usage.get("input_tokens"):
            return usage["input_tokens"]
    return None


def dump_messages(messages):
    print(f"\n[messages: {len(messages)} in thread]")
    for i, m in enumerate(messages):
        content = m.content if isinstance(m.content, str) else str(m.content)
        preview = content.replace("\n", " ")[:90]
        tags = []
        if _is_summary(m):
            tags.append("SUMMARY")
        tool_calls = getattr(m, "tool_calls", None)
        if tool_calls:
            tags.append(f"tool_calls={len(tool_calls)}")
        suffix = f"  <{', '.join(tags)}>" if tags else ""
        print(f"  {i:>2}. {type(m).__name__:16} {preview!r}{suffix}")
    print()

llm = create_llm()
print(f"Using {LLM_PROVIDER} / {LLM_MODEL}")

print("Initializing agents...")
discovery_agent = create_discovery_agent(llm, LM_STUDIO_BASE, KNOWLEDGE_DIR)
research_agent = create_research_agent(llm, LM_STUDIO_BASE, KNOWLEDGE_DIR)

orchestrator = Orchestrator(llm, {
    "DISCOVERY": discovery_agent,
    "RESEARCH": research_agent,
})

if __name__ == "__main__":
    log_fh = None
    if DEBUG_LOG_FILE:
        log_fh = open(DEBUG_LOG_FILE, "a", encoding="utf-8")
        sys.stdout = _Tee(sys.__stdout__, log_fh)
        print(f"\n===== session started {datetime.now():%Y-%m-%d %H:%M:%S} =====")

    print("Career Guidance Agent (type 'quit' to exit)")
    print("-" * 40)

    prev_summary = None
    while True:
        user_input = input("\nYou: ")
        # The terminal echoes typed input, but that echo doesn't pass through
        # stdout, so record it in the log file explicitly.
        if log_fh:
            log_fh.write(user_input + "\n")
            log_fh.flush()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        config = {"configurable": {"thread_id": "main"}}
        response = orchestrator.invoke(user_input, config)

        if DEBUG_MESSAGES:
            # SummarizationMiddleware fires when a summary message appears, or
            # when an existing summary is rewritten (it re-summarizes as the
            # conversation keeps growing). The message count does NOT reliably
            # drop, because `keep` retains recent messages and new ones are added
            # the same turn -- so detect the summary message itself instead.
            summary = _summary_text(response["messages"])
            if summary and summary != prev_summary:
                print("\n*** SummarizationMiddleware fired: older turns condensed "
                      "into a summary message (marked <SUMMARY> below) ***")
            prev_summary = summary

            prompt_tokens = _last_prompt_tokens(response["messages"])
            if prompt_tokens is not None:
                pct = 100 * prompt_tokens / CONTEXT_WINDOW
                print(f"[context: {prompt_tokens} / {CONTEXT_WINDOW} prompt tokens "
                      f"({pct:.1f}% of window)]")

            dump_messages(response["messages"])

        final_message = ""
        for msg in reversed(response["messages"]):
            if msg.content:
                final_message = msg.content
                break

        if not final_message:
            print("\n[DEBUG] Empty response. Dumping last message for diagnosis:")
            last = response["messages"][-1]
            meta = getattr(last, "response_metadata", {}) or {}
            extra = getattr(last, "additional_kwargs", {}) or {}
            print(f"[DEBUG]   type            = {type(last).__name__}")
            print(f"[DEBUG]   content         = {last.content!r}")
            print(f"[DEBUG]   tool_calls      = {getattr(last, 'tool_calls', None)}")
            print(f"[DEBUG]   finish_reason   = {meta.get('finish_reason')}")
            print(f"[DEBUG]   token_usage     = {meta.get('token_usage')}")
            reasoning = extra.get("reasoning_content")
            if reasoning:
                print(f"[DEBUG]   reasoning_content (first 500 chars):\n{reasoning[:500]}")
            print(f"[DEBUG]   total messages in thread = {len(response['messages'])}")

        print(f"Agent: {final_message}")

    if log_fh:
        print(f"===== session ended {datetime.now():%Y-%m-%d %H:%M:%S} =====")
        sys.stdout = sys.__stdout__
        log_fh.close()
