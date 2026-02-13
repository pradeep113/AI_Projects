import logging
import os
import streamlit as st
import httpx
from azure.identity import ClientSecretCredential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tenant_id = st.secrets["AZURE_TENANT_ID"]
client_id = st.secrets["AZURE_CLIENT_ID"]
client_secret = st.secrets["AZURE_CLIENT_SECRET"]

FOUNDARY_ENDPOINT = st.secrets["FOUNDARY_ENDPOINT"]
FOUNDARY_AGENT_NAME = st.secrets["FOUNDARY_AGENT_NAME"]
PROJECT_NAME = st.secrets.get("FOUNDARY_PROJECT_NAME", "GoAMFT_workflow_agentic")
API_VERSION = st.secrets.get("OPENAI_API_VERSION", "2025-11-15-preview")

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

def run_agent_workflow(prompt: str) -> str:
    try:
        url = f"{FOUNDARY_ENDPOINT}/api/projects/{PROJECT_NAME}/agents/{FOUNDARY_AGENT_NAME}/responses?api-version={API_VERSION}"

        # IMPORTANT: request token for Foundry resource, not Cognitive Services
        scope = f"{FOUNDARY_ENDPOINT}/.default"
        token = credential.get_token(scope).token

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        body = {
            "input": [{"role": "user", "content": prompt}],
            "version": "latest"
        }

        resp = httpx.post(url, headers=headers, json=body, timeout=60)
        resp.raise_for_status()

        data = resp.json()
        return data.get("output_text", str(data))
    except Exception as e:
        logger.exception("Error calling Foundry agent")
        return f"❌ Error: {e}"

