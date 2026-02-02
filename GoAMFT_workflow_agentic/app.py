import streamlit as st
from backend import run_agent_workflow

st.set_page_config(page_title="Azure Foundry Agent Runner", layout="centered")
st.title("🤖 Agentic Workflow Executor")

# Prompt input
user_prompt = st.text_area("Enter your prompt", placeholder="e.g., Compare MFT tools with HIPAA compliance")

# Token input
user_token = st.text_input("Enter your Azure AI Foundry token", type="password")

# Submit button
if st.button("Run Workflow"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    elif not user_token.strip():
        st.warning("Please enter your token.")
    else:
        with st.spinner("Executing workflow..."):
            response_text = run_agent_workflow(user_prompt, user_token)
            st.markdown("### 🧾 Workflow Response")
            st.write(response_text)

