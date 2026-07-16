from langchain_openai import ChatOpenAI

from prompts.orchestrator import ORCHESTRATOR_PROMPT


class Orchestrator:
    def __init__(self, llm: ChatOpenAI, agents: dict):
        self.llm = llm
        self.agents = agents

    def route(self, user_message: str) -> str:
        """Use the LLM to classify which agent should handle this message."""
        response = self.llm.invoke([
            {"role": "system", "content": ORCHESTRATOR_PROMPT},
            {"role": "user", "content": user_message},
        ])
        decision = response.content.strip().upper()
        if decision not in self.agents:
            return "DISCOVERY"
        return decision

    def invoke(self, user_message: str, config: dict):
        """Route the message to the appropriate agent and return its response."""
        route_to = self.route(user_message)
        agent = self.agents[route_to]
        print(f"[Routed to: {route_to}]")
        return agent.invoke({"messages": [{"role": "user", "content": user_message}]}, config)
