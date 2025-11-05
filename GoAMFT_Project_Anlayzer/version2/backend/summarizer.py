# backend/summarizer.py
import os
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL", "https://pradeepazopenai.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "4ChnscFbQsgE6OpHkq7ADOnQiljXPiwPzhH7l3gcmiNdin09YEQFJQQJ99BHAC77bzfXJ3w3AAABACOG4fSG")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

def summarize_actions(actions):
    prompt = f"""Summarize the following GoAnywhere project actions. Group by module, explain each action briefly, and highlight key details like source/target paths, protocols (SFTP, Blob, MQ), file patterns, archive steps, deletions, and post-transfer actions. Format as readable text and include a table in such a way that this data does not show module name . Table shows source type/protocol/path details ,target type/protocol/path details , file pattern so that i may use it to understand clearly or to use to develop in any other tool from scratch :

{actions}
"""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=13107,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=deployment,
    )
    return response.choices[0].message.content

