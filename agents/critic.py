from agents.base_agent import BaseAgent


class CriticAgent(BaseAgent):

    def run(self, email_json: dict):

        system = """
        You are a senior retail email critic agent.

        Your job:
        - Improve persuasion
        - Fix tone consistency
        - Make content concise
        - Keep structure EXACTLY the same

        IMPORTANT RULES:
        - Return STRICT JSON
        - Do NOT add markdown
        - Do NOT remove fields
        - Only improve text content
        """

        user = f"""
        Improve this campaign email JSON:
        with replacing any refernce names with Customer
        EX [Name] -> replace with Customer
        
        EMAIL_JSON : 
        {email_json}
        """

        improved_email = self.call_llm(
            system_prompt=system,
            user_prompt=user,
            expect_json=True,
            max_tokens=900
        )

        return improved_email
