import logging
import os
import streamlit as st
import httpx
from azure.identity import ClientSecretCredential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load secrets
tenant_id = st.secrets["AZURE_TENANT_ID"]
client_id = st.secrets["AZURE_CLIENT_ID"]
client_secret = st.secrets["AZURE_CLIENT_SECRET"]

FOUNDARY_ENDPOINT = st.secrets["FOUNDARY_ENDPOINT"]  # base URL only
FOUNDARY_AGENT_NAME = st.secrets["FOUNDARY_AGENT_NAME"]
PROJECT_NAME = st.secrets.get("FOUNDARY_PROJECT_NAME", "GoAMFT_workflow_agentic")
API_VERSION = st.secrets.get("OPENAI_API_VERSION", "2025-11-15-preview")

# Azure credential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

def run_agent_workflow(prompt: str) -> str:
    """Send a prompt to the Foundry agent via direct REST call and return its response."""
    try:
        # Construct the agent endpoint URL
        url = f"{FOUNDARY_ENDPOINT}/api/projects/{PROJECT_NAME}/agents/{FOUNDARY_AGENT_NAME}/responses?api-version={API_VERSION}"

        # Get a bearer token for Cognitive Services
        token = credential.get_token("https://cognitiveservices.azure.com/.default").token
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

