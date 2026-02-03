import re
import streamlit as st
from backend_using_appreg import run_agent_workflow

st.title("Azure Foundry Agent Streamlit App")

prompt = st.text_area("Enter your prompt:", height=150)


if st.button("Run Agent"):
    if prompt.strip():
        with st.spinner("Calling Foundry agent..."):
            result = run_agent_workflow(prompt)
        st.subheader("Agent Response")
        st.write(result)
    else:
        st.warning("Please enter a prompt before running the agent.")

