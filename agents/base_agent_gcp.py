import vertexai
from vertexai.generative_models import GenerativeModel
import os

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)

class BaseAgent:

    def __init__(self, role: str):
        self.role = role
        self.model = GenerativeModel("gemini-1.5-flash")

    def call_llm(self, system_prompt: str, user_prompt: str):

        prompt = f"""
        SYSTEM:
        {system_prompt}

        USER:
        {user_prompt}
        """

        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 2048
            }
        )

        return response.text
