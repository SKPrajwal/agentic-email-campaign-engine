from agents.base_agent import BaseAgent

class StrategyAgent(BaseAgent):

    def run(self, topic):

        system = "You are a marketing strategist."

        user = f"""
        Topic: {topic}

        Define tone and email structure.
        """

        return self.call_llm(system, user)
