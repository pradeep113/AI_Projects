import openai
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import pandas as pd
import re

#load_dotenv()

endpoint = os.getenv("ENDPOINT_URL", "https://pradeepazopenai.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "4ChnscFbQsgE6OpHkq7ADOnQiljXPiwPzhH7l3gcmiNdin09YEQFJQQJ99BHAC77bzfXJ3w3AAABACOG4fSG")

#endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
#deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
#subscription_key = os.getenv("AZURE_OPENAI_KEY")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# 🔍 Comparison function
def get_comparison(prompt: str, tools: list):
    try:
        tool_list = ", ".join(tools)
        full_prompt = (
            f"Compare MFT tools: {tool_list}. "
            f"Based on the following requirements: {prompt}. "
            f"Provide a comparison table and suggest the best tool for the input."
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert in MFT tools."},
                {"role": "user", "content": full_prompt}
            ],
            max_completion_tokens=13107,
            temperature=1.0,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            model=deployment,
        )

        raw_text = response.choices[0].message.content
        df = parse_markdown_table(raw_text)
        return raw_text, df
    except Exception as e:
        # Always return a tuple
        return f"❌ Error: {str(e)}", pd.DataFrame()

def parse_markdown_table(markdown: str) -> pd.DataFrame:
    lines = [line.strip() for line in markdown.splitlines() if "|" in line]
    rows = [re.split(r'\s*\|\s*', line.strip("|")) for line in lines]
    return pd.DataFrame(rows[2:], columns=rows[0]) if len(rows) > 2 else pd.DataFrame()
