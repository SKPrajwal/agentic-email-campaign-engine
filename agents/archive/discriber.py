from agents.base_agent import BaseAgent

class ProductDescAgent(BaseAgent):

    def run(self, product):

        # 🔹 System prompt defines the behaviour of the agent
        system = """
You are a Retail Product Content Agent.

Your task:
- Generate a concise 1-2 line ecommerce product description.
- Keep tone premium, clean, and customer-friendly.
- Focus on style, usage, and key attributes.
- Do NOT invent features not present in the input.

Output Rules:
- Return JSON only.
- Field name must be: product_description
- Max 40 words.
"""

        # 🔹 User prompt passes structured product context
        user = f"""
Create a short product description using these attributes:

ProductId: {product.get("ProductId")}
Gender: {product.get("Gender")}
Category: {product.get("Category")}
SubCategory: {product.get("SubCategory")}
ProductType: {product.get("ProductType")}
Colour: {product.get("Colour")}
Usage: {product.get("Usage")}
ProductTitle: {product.get("ProductTitle")}
"""

        return self.call_llm(
            system_prompt=system,
            user_prompt=user,
            expect_json=True,
            max_tokens=300
        )
