from agents.base_agent import BaseAgent

class StrategyAgent(BaseAgent):

    def run(self, topic):

        system = """
You are a RETAIL CAMPAIGN STRATEGIST.

IMPORTANT:
- You DO NOT create event plans.
- You DO NOT describe locations or activities.
- You ONLY define strategy to SELL PRODUCTS through email.

The topic is ONLY a marketing angle to frame retail sales.

Return STRICT JSON:

{
  "campaign_angle": "",
  "product_focus": "",
  "tone": "",
  "curation_rules": "",
  "writing_guidelines": ""
  "Tone": ""
  "Email Structure": ""
}
"""

        user = f"""
Campaign Topic: {topic}

Create a retail sales strategy that helps:
- Curator agent select products
- Writer agent generate sales-focused email content
"""

        return self.call_llm(
            system_prompt=system,
            user_prompt=user,
            expect_json=True,
            max_tokens=300
        )
