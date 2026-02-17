from agents.base_agent import BaseAgent

class CriticAgent(BaseAgent):

    def run(self, email):

        system = "Improve marketing email clarity and persuasion."

        user = f"""
        Improve this email:

        {email}
        """

        return self.call_llm(system, user)
