import os
import re
import xml.etree.ElementTree as ET
import streamlit as st
from backend_using_appreg import run_agent_workflow

st.title(" GoA Agent Workflow App")

prompt = st.text_area("Enter your prompt:", height=150)


def extract_valid_xml_blocks(response_text: str, tag: str):
    """
    Extracts valid XML blocks for a given tag from the response text.
    Skips invalid fragments that cannot be parsed.
    """
    pattern = fr"<{tag}.*?</{tag}>"
    matches = re.findall(pattern, response_text, re.DOTALL)
    valid_blocks = []
    for m in matches:
        try:
            ET.fromstring(m)  # validate XML
            valid_blocks.append(m)
        except ET.ParseError:
            continue
    return valid_blocks


def write_xml_files(response_text: str, output_dir: str = "xml_outputs"):
    """
    Extracts project, resource, and webuser XML blocks from the response text
    and writes them into separate numbered files.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Project XMLs
    projects = extract_valid_xml_blocks(response_text, "project")
    for i, xml in enumerate(projects, start=1):
        filename = f"{output_dir}/project_{i}.xml"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"✅ Wrote {filename}")

    # Resource XMLs
    resources = extract_valid_xml_blocks(response_text, "resource")
    for i, xml in enumerate(resources, start=1):
        filename = f"{output_dir}/resource_{i}.xml"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"✅ Wrote {filename}")

    # WebUser XMLs
    webusers = extract_valid_xml_blocks(response_text, "webuser")
    for i, xml in enumerate(webusers, start=1):
        filename = f"{output_dir}/webuser_{i}.xml"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"✅ Wrote {filename}")
    
    #st.success("XML files have been extracted and saved to xml_outputs/")



if st.button("Submit"):
    if prompt.strip():
        with st.spinner("Submitting ..."):
            result = run_agent_workflow(prompt)

        #st.subheader("Agent Response")
        st.write(result)

        write_xml_files(result, output_dir="xml_outputs")

    else:
        st.warning("Please enter a prompt before Submit.")

