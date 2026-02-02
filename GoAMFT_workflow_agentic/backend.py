import os
import logging
import time
from azure.ai.projects import AIProjectClient
from azure.core.credentials import TokenCredential, AccessToken

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use the exact project endpoint from Azure Portal (Overview page)
# IMPORTANT: include /api/projects/<project-name>
FOUNDARY_ENDPOINT = os.getenv(
    "FOUNDARY_ENDPOINT",
    "https://goaprojectproject-resource.services.ai.azure.com/api/projects/goaprojectproject"
)

# Must exactly match the agent name in Foundry (case-sensitive)
FOUNDARY_AGENT_NAME = os.getenv("FOUNDARY_AGENT_NAME", "agentProjectCreator")


# Custom credential class for manual token
class ManualTokenCredential(TokenCredential):
    def __init__(self, token: str, expires_on: int = None):
        self._token = token
        # Default expiry = 1 hour from now if not provided
        self._expires_on = expires_on or int(time.time()) + 3600

    def get_token(self, *scopes, **kwargs):
        return AccessToken(self._token, self._expires_on)


def run_agent_workflow(prompt: str, token: str) -> str:
    """
    Execute the Foundry agent workflow with a user-provided token.
    Returns the raw textual response.
    """
    try:
        credential = ManualTokenCredential(token)
        project_client = AIProjectClient(endpoint=FOUNDARY_ENDPOINT, credential=credential)
        openai_client = project_client.get_openai_client()

        user_message = f"Prompt: {prompt}"

        response = openai_client.responses.create(
            input=[{"role": "user", "content": user_message}],
            extra_body={"agent": {"name": FOUNDARY_AGENT_NAME, "type": "agent_reference"}},
        )

        # Try to extract text directly
        raw_text = getattr(response, "output_text", None)

        # Fallback: parse response.output if needed
        if not raw_text:
            raw_text_parts = []
            for item in getattr(response, "output", []) or []:
                if isinstance(item, dict):
                    if "text" in item:
                        raw_text_parts.append(item["text"])
                    if "content" in item and isinstance(item["content"], list):
                        for c in item["content"]:
                            if isinstance(c, dict) and "text" in c:
                                raw_text_parts.append(c["text"])
                            elif isinstance(c, str):
                                raw_text_parts.append(c)
            raw_text = "\n\n".join(raw_text_parts).strip()

        if not raw_text:
            raise RuntimeError("Agent returned no textual output.")

        return raw_text

    except Exception as e:
        logger.exception("Error calling Foundry agent: %s", e)
        return f"❌ Error calling agent: {str(e)}"

