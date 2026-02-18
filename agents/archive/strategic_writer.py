from agents.base_agent import BaseAgent

class StrategicWriterAgent(BaseAgent):

    def run(self, topic, curated_products):

        system = "You are a marketing strategist who write high-converting retail marketing emails."

        user = f"""
        Topic: {topic}
        Products: {curated_products}

        Generate marketing email.
        """

        return self.call_llm(system, user)
