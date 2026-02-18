from agents.base_agent import BaseAgent

class WriterAgent(BaseAgent):

    def run(self, topic, curated_products, strategy):

        system = "You write high-converting retail marketing emails."

        user = f"""
        Topic: {topic}
        Strategy: {strategy}
        Products: {curated_products}

        Generate marketing email.
        """

        return self.call_llm(system, user)
