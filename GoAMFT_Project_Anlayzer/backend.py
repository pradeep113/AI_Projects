# backend.py
import xml.etree.ElementTree as ET
import openai
from fpdf import FPDF
import os
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL", "https://pradeepazopenai.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "4ChnscFbQsgE6OpHkq7ADOnQiljXPiwPzhH7l3gcmiNdin09YEQFJQQJ99BHAC77bzfXJ3w3AAABACOG4fSG")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

def parse_project_xml(xml_content):
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()

    actions = []
    for module in root.findall("module"):
        mod_name = module.get("name", "Unnamed")
        for elem in module:
            tag = elem.tag.lower()
            label = elem.get("label", "No Label")
            details = {k: v for k, v in elem.attrib.items()}
            actions.append({
                "Module": mod_name,
                "Action": tag,
                "Label": label,
                "Details": details
            })
    return actions

def summarize_actions(actions):
    prompt = f"""Summarize the following GoAnywhere project actions. Group by module, explain each action briefly, and highlight key details like source/target paths, protocols (SFTP, Blob, MQ), file patterns, archive steps, deletions, and post-transfer actions. Format as readable text and include a table:

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

def generate_pdf(summary_text, filename="GoAnywhere_Project_Summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in summary_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

