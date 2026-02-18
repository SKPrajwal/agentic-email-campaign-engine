from agents.base_agent import BaseAgent

class CuratorAgent(BaseAgent):

    def run(self, topic, products):

        system = """
You are a SENIOR RETAIL MERCHANDISING CURATOR.

GOAL:
Create a HIGH-CONVERTING retail product mix for a marketing campaign.

CRITICAL RULES:
- Full exact dict of selected products including image_url
- Ensure CROSS-DOMAIN diversity (top wear, bottom wear, footwear, accessories, etc).
- Think in terms of COMPLETE OUTFITS, not individual items.
- Select products that complement each other.
- Avoid duplicates from same sub-category unless necessary.

MERCHANDISING STRATEGY:
- 1 hero product (main attention grabber)
- 2-3 supporting products from different domains
- 1 add-on or accessory if available

Return STRICT JSON full exact dict of selected products.:
{
  "reasoning": "short explanation of merchandising logic",
  "selected_products": [ ... ]
}
"""

        user = f"""
Campaign Topic:
{topic}

Available Products (JSON):
{products}

TASK:
Select 4-6 products that form a COMPLETE retail story.

Example:
If topic is winter wear → include topwear + bottomwear + footwear.

ONLY return JSON.
"""

        return self.call_llm(
            system_prompt=system,
            user_prompt=user,
            expect_json=True,
            max_tokens=1600
        )
