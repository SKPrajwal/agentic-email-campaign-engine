from agents.base_agent import BaseAgent
import json

class PlannerAgent(BaseAgent):

    def run(self, topic: str):

        system = """
You are a senior orchestration planner for a multi-agent system.

Your job:
- Break the goal into logical execution steps
- Decide dependencies between steps
- Only include steps that are necessary
- Output STRICT JSON
"""

        user = f"""
Goal: Create a marketing email campaign.

Topic: {topic}

Available Agents:
- retrieve → fetch products
- curate → filter relevant products
- strategize → build marketing angle
- write → generate email content
- critic → improve final email

Return JSON:

{{
  "reasoning": "...why this plan works...",
  "execution_plan":[
      {{"step":"retrieve"}},
      {{"step":"curate","depends_on":["retrieve"]}},
      {{"step":"strategize"}},
      {{"step":"write","depends_on":["curate","strategize"]}},
      {{"step":"critic","depends_on":["write"]}}
  ]
}}
"""

        response = self.call_llm(system, user)
        return json.loads(response)
