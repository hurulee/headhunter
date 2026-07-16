from config import create_llm, LM_STUDIO_BASE, KNOWLEDGE_DIR, LLM_PROVIDER, LLM_MODEL
from agents.discovery import create_discovery_agent
from agents.research import create_research_agent
from agents.orchestrator import Orchestrator

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
    print("Career Guidance Agent (type 'quit' to exit)")
    print("-" * 40)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ("quit", "exit", "q"):
            break

        config = {"configurable": {"thread_id": "main"}}
        response = orchestrator.invoke(user_input, config)
        final_message = ""
        for msg in reversed(response["messages"]):
            if msg.content:
                final_message = msg.content
                break
        print(f"Agent: {final_message}")
