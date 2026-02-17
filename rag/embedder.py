import boto3
import json
import os

boto3_embbed_session = boto3.Session(profile_name='ch_dev_developer')

# Bedrock Runtime Client
bedrock_embbed_client = boto3_embbed_session.client(
    "bedrock-runtime"
)

EMBED_MODEL = "amazon.titan-embed-text-v2:0"


def embed(texts):
    embeddings = []

    for text in texts:

        body = json.dumps({
            "inputText": text
        })

        response = bedrock_embbed_client.invoke_model(
            modelId=EMBED_MODEL,
            body=body
        )

        response_body = json.loads(response["body"].read())

        embeddings.append(response_body["embedding"])

    return embeddings
