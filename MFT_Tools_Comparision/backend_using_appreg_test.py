import logging
import streamlit as st
from azure.identity import ClientSecretCredential
from azure.ai.projects import AIProjectClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tenant_id = st.secrets["AZURE_TENANT_ID"]
client_id = st.secrets["AZURE_CLIENT_ID"]
client_secret = st.secrets["AZURE_CLIENT_SECRET"]

FOUNDARY_ENDPOINT = st.secrets["FOUNDARY_ENDPOINT"]
FOUNDARY_AGENT_NAME = st.secrets["FOUNDARY_AGENT_NAME"]

credential = ClientSecretCredential(tenant_id, client_id, client_secret)
project_client = AIProjectClient(endpoint=FOUNDARY_ENDPOINT, credential=credential)

def run_agent_workflow(prompt: str) -> str:
    """Send a prompt to the Foundry agent and return its response."""
    try:
        response = project_client.agents.responses.create(
            agent_name=FOUNDARY_AGENT_NAME,
            input=[{"role": "user", "content": prompt}],
            extra_body={"version": "latest"}
        )
        return getattr(response, "output_text", "No response text")
    except Exception as e:
        logger.exception("Error calling Foundry agent")
        return f"❌ Error: {e}"

