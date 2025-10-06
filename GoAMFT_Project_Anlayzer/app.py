# app.py
import streamlit as st
from backend import parse_project_xml, summarize_actions, generate_pdf

st.set_page_config(page_title="GoAnywhere Project Analyzer", layout="wide")
st.title("🔁 GoAnywhere Project Analyzer")

uploaded_file = st.file_uploader("Upload GoAnywhere Project XML", type=["xml"])
if uploaded_file:
    xml_content = uploaded_file.read().decode("utf-8")
    parsed_actions = parse_project_xml(xml_content)
    st.subheader("📋 Parsed Actions")
    st.json(parsed_actions)

    with st.spinner("Summarizing with Azure OpenAI..."):
        summary = summarize_actions(parsed_actions)
        st.subheader("🧠 AI Summary")
        st.markdown(summary)

        pdf_file = generate_pdf(summary)
        with open(pdf_file, "rb") as f:
            st.download_button("📄 Download Summary as PDF", f, file_name=pdf_file)

