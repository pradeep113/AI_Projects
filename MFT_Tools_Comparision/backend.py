"""
backend.py

Azure Foundry (AI Projects) client wrapper to call an agent and return:
    (raw_text, parsed_dataframe)

Usage:
    from backend import get_comparison
    raw_text, df = get_comparison(user_prompt, selected_tools, uploaded_files)

Notes:
- Requires azure-identity and azure-ai-projects packages.
- Configure environment variables: FOUNDARY_ENDPOINT, FOUNDARY_AGENT_NAME.
- Authentication uses DefaultAzureCredential (managed identity / CLI / env vars).
"""

import os
import logging
from typing import List, Optional, Tuple

import pandas as pd
import re

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment-configurable values
FOUNDARY_ENDPOINT = os.getenv(
    "FOUNDARY_ENDPOINT",
    "https://pradeepazaifoundry.services.ai.azure.com/api/projects/mftcomparision",
)
FOUNDARY_AGENT_NAME = os.getenv("FOUNDARY_AGENT_NAME", "agentMFTtoolscomparison")

# Initialize clients (lazily to avoid side effects on import)
_project_client: Optional[AIProjectClient] = None
_openai_client = None


def _init_clients():
    global _project_client, _openai_client
    if _project_client is None:
        credential = DefaultAzureCredential()
        _project_client = AIProjectClient(endpoint=FOUNDARY_ENDPOINT, credential=credential)
        logger.info("Initialized AIProjectClient for endpoint: %s", FOUNDARY_ENDPOINT)
    if _openai_client is None:
        _openai_client = _project_client.get_openai_client()
        logger.info("Retrieved OpenAI client from project client")


def parse_markdown_table(markdown: str) -> pd.DataFrame:
    """
    Parse the first Markdown table found in the text into a pandas DataFrame.
    Returns an empty DataFrame if no valid table is found.
    """
    # Collect lines that look like table rows (contain pipes)
    lines = [line.strip() for line in markdown.splitlines() if "|" in line]
    if not lines:
        return pd.DataFrame()

    # Normalize and split rows
    rows = [re.split(r'\s*\|\s*', line.strip("| ")) for line in lines]

    # Find header and separator rows (header followed by a separator like ---)
    if len(rows) >= 2 and all(re.match(r'^-+$', cell.strip('- ')) for cell in rows[1]):
        header = rows[0]
        data_rows = rows[2:]
    else:
        # If no explicit separator, assume first row is header and rest are data
        header = rows[0]
        data_rows = rows[1:]

    # Clean header and rows
    header = [h.strip() for h in header if h.strip() != ""]
    cleaned_rows = []
    for r in data_rows:
        # Pad or trim to match header length
        r = [c.strip() for c in r]
        if len(r) < len(header):
            r += [""] * (len(header) - len(r))
        cleaned_rows.append(r[: len(header)])

    try:
        df = pd.DataFrame(cleaned_rows, columns=header)
    except Exception:
        df = pd.DataFrame()
    return df


def get_comparison(prompt: str, tools: List[str], uploaded_files: Optional[List[str]] = None) -> Tuple[str, pd.DataFrame]:
    """
    Call the configured Foundry agent with the user's prompt and selected tools.

    Returns:
        (raw_text, dataframe) where raw_text is the agent's full textual response,
        and dataframe is the parsed Markdown table (or empty DataFrame on failure).
    """
    _init_clients()

    # Build user message content
    tool_list = ", ".join(tools) if tools else "No tools selected"
    files_list = ", ".join(uploaded_files) if uploaded_files else "No uploaded files provided"
    user_message = (
        f"Selected tools: {tool_list}\n"
        f"Requirements: {prompt}\n"
    )

    try:
        # Reference the agent and request a response
        response = _openai_client.responses.create(
            input=[{"role": "user", "content": user_message}],
            extra_body={"agent": {"name": FOUNDARY_AGENT_NAME, "type": "agent_reference"}},
        )

        # Prefer output_text if available (simple), otherwise try to extract from output structure
        raw_text = getattr(response, "output_text", None)
        if not raw_text:
            # Fallback: try to extract textual content from response.output
            raw_text_parts = []
            for item in getattr(response, "output", []) or []:
                # Each item may have 'content' or 'text' fields depending on SDK version
                content = item.get("content") if isinstance(item, dict) else None
                if content:
                    # content may be a list of dicts
                    if isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict) and "text" in c:
                                raw_text_parts.append(c["text"])
                            elif isinstance(c, str):
                                raw_text_parts.append(c)
                    elif isinstance(content, str):
                        raw_text_parts.append(content)
                # Try 'text' field directly
                text = item.get("text") if isinstance(item, dict) else None
                if text:
                    raw_text_parts.append(text)
            raw_text = "\n\n".join(raw_text_parts).strip()

        if not raw_text:
            raise RuntimeError("Agent returned no textual output.")

        # Parse the first Markdown table found in the response
        df = parse_markdown_table(raw_text)

        return raw_text, df

    except Exception as e:
        logger.exception("Error calling Foundry agent: %s", e)
        # Always return a tuple (error message, empty DataFrame) to keep caller unpacking consistent
        return f"❌ Error calling agent: {str(e)}", pd.DataFrame()


# Optional: simple CLI test when run directly
if __name__ == "__main__":
    sample_prompt = "HIPAA compliance, SFTP support, cloud integration"
    sample_tools = ["IBM Sterling MFT", "Progress MOVEit"]
    text, table = get_comparison(sample_prompt, sample_tools)
    print("=== RAW TEXT ===")
    print(text[:2000])  # print a portion for quick inspection
    print("\n=== PARSED TABLE ===")
    if not table.empty:
        print(table.head().to_string(index=False))
    else:
        print("No table parsed.")

