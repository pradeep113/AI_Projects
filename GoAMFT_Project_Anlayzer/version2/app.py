# app.py
import streamlit as st
from backend.parser import parse_project_xml
from backend.summarizer import summarize_actions
from backend.exporter import generate_pdf

st.set_page_config(page_title="GoAnywhere Project Analyzer", layout="wide")
st.title("🔁 GoAnywhere Project Analyzer")

uploaded_file = st.file_uploader("Upload GoAnywhere Project XML", type=["xml"])
if uploaded_file:
    xml_content = uploaded_file.read().decode("utf-8")
    try:
        parsed_actions = parse_project_xml(xml_content)
        st.subheader("📋 Parsed Actions")
        st.json(parsed_actions)

        if "summary" not in st.session_state:
            with st.spinner("Summarizing with Azure OpenAI..."):
                st.session_state.summary = summarize_actions(parsed_actions)

        st.subheader("🧠 AI Summary")
        st.markdown(st.session_state.summary, unsafe_allow_html=True)

        pdf_file = generate_pdf(st.session_state.summary)
        with open(pdf_file, "rb") as f:
            st.download_button("📄 Download Summary as PDF", f, file_name="GoAnywhere_Project_Summary.pdf")

    except Exception as e:
        st.error(f"Error: {e}")

