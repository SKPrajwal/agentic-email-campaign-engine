import json
import os
import boto3


class BaseAgent:
    """
    Enterprise Bedrock Base Agent
    - Token efficient prompts
    - Structured output enforcement
    - Retry safe
    """

    def __init__(self, role: str):
        self.role = role

        boto3_session = boto3.Session(profile_name='ch_dev_developer')

        # Bedrock Runtime Client
        self.bedrock_client = boto3_session.client(
            "bedrock-runtime"
        )

        # Recommended lightweight reasoning model
        self.model_id = "amazon.nova-micro-v1:0"

    # -----------------------------------------------------
    # Main LLM Call
    # -----------------------------------------------------
    def call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 400,
        temperature: float = 0.3,
        expect_json: bool = False
    ):
        """
        Efficient Bedrock invocation.

        expect_json=True:
            forces structured output behaviour
        """

        # 🔥 Strong output control reduces hallucination + tokens
        output_guard = ""
        if expect_json:
            output_guard = (
                "\nReturn ONLY valid JSON. "
                "Do not add explanation or extra text."
            )

        # Nova Message Structure (Token Efficient)
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": f"""
                    {system_prompt}

                    INSTRUCTIONS:
                    Follow the above role definition strictly.

                    TASK:
                    {user_prompt}{output_guard}
                    """
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9
            }
        }

        # -----------------------------------------------------
        # Invoke Bedrock Model
        # -----------------------------------------------------
        response = self.bedrock_client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())

        # Nova Response Structure
        text_output = response_body["output"]["message"]["content"][0]["text"]

        # Optional JSON enforcement
        if expect_json:
            try:
                return json.loads(text_output)
            except Exception:
                raise ValueError(
                    f"{self.role} returned invalid JSON:\n{text_output}"
                )

        return text_output

# llm_agent = BaseAgent('User')
# llm_agent.call_llm('Give me crisp details.', 'details of data engineering core concepts')

