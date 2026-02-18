from agents.base_agent import BaseAgent


class WriterAgent(BaseAgent):

    def run(self, topic, curated_products, strategy):

        system = """
            You are a retail email writer agent.

            IMPORTANT RULES:
            - Output STRICT JSON only.
            - Do NOT add markdown.
            - Do NOT include explanations.
            - Follow the schema exactly.
            - Keep the closing generic instead of place holder. 

            Schema:

            {
            "subject": "",
            "preheader": "",
            "greeting": "",
            "headline": "",
            "intro": "",
            "products": [
            {
                "name": "",
                "price": "",
                "description": "",
                "highlight": "",
                "image_url": ""
            }
            ],
            "cta_text": "",
            "closing": ""
            }
        """

        user = f"""
            Topic: {topic}

            Strategy:
            {strategy}

            Curated Products:
            {curated_products}
        """

        return self.call_llm(
            system_prompt=system,
            user_prompt=user,
            expect_json=True,
            max_tokens=900
        )
