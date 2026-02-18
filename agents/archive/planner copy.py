from agents.base_agent import BaseAgent
import json

class PlannerAgent(BaseAgent):

    def run(self, topic: str):

        system = "You are a planning agent. Output JSON only."
        user = f"""
        Topic: {topic}

        Return:
        {{
          "steps": ["retrieve","curate","strategize","write","critic"]
        }}
        """
        # print("Planner prompt:", system, user)

        response = self.call_llm(system, user)
        # print("Planner response:", response)

        return json.loads(response)
