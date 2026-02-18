from agents.base_agent import BaseAgent

class CuratorAgent(BaseAgent):

    def run(self, topic, products):

        system = """
You are a RETAIL PRODUCT CURATOR.

IMPORTANT:
- Select products that maximize retail sales.
- Focus on product relevance and campaign alignment.

Return STRICT JSON list of selected products.
"""

        user = f"""
Campaign Topic: {topic}

Available Products:
{products}

Select 4-6 products best suited for retail campaign sales.
"""

        return self.call_llm(
            system_prompt=system,
            user_prompt=user,
            expect_json=True,
            max_tokens=800
        )
