from agents.base_agent import BaseAgent

class CuratorAgent(BaseAgent):

    def run(self, topic, products):

        system = "You are a retail product curator."
        user = f"""
        Topic: {topic}

        Select top 5 products.

        Products:
        {products}
        """

        return self.call_llm(system, user)
