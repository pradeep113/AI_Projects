import streamlit as st
import pandas as pd
from io import BytesIO
from backend_using_appreg import run_agent_workflow

st.set_page_config(page_title="MFT Tool Comparator", layout="centered")
st.title("🔐 MFT Tool Comparison Assistant")
st.markdown("Enter your requirements and select MFT tools to compare.")

# 📦 Tool selection inside an expander
with st.expander("🧰 Select MFT Tools to Compare"):
    st.markdown("Choose one or more tools:")
    tools = {
        "GoAnywhere MFT": st.checkbox("Fortra GoAnywhere MFT"),
        "Axway SecureTransport": st.checkbox("Axway SecureTransport"),
        "IBM Sterling MFT": st.checkbox("IBM Sterling MFT"),
        "Globalscape EFT": st.checkbox("Fortra Globalscape EFT"),
        "Progress MOVEit": st.checkbox("Progress MOVEit"),
        "Cleo (CIC)": st.checkbox("Cleo (CIC)"),
        "Seeburger": st.checkbox("Seeburger BIS"),
        "TIBCO MFT": st.checkbox("TIBCO MFT"),
        "AWS Transfer family": st.checkbox("AWS Transfer family")
    }

selected_tools = [tool for tool, checked in tools.items() if checked]

# 📝 Prompt input
user_prompt = st.text_area(
    "Your Requirements",
    placeholder="e.g., SFTP, FTPS support, cloud integration like SharePoint, MQ, S3 or Blob"
)

# 🚀 Run comparison
if st.button("Compare Tools"):
    if not selected_tools:
        st.warning("Please select at least one tool.")
    elif not user_prompt.strip():
        st.warning("Please enter your requirements.")
    else:
        # Build prompt for agent
        combined_prompt = (
            f"Compare the following MFT tools: {', '.join(selected_tools)} "
            f"based on these requirements: {user_prompt}"
        )

        with st.spinner("Contacting Agent..."):
            comparison_result = run_agent_workflow(combined_prompt)

        st.subheader("📊 Comparison Result")
        st.write(comparison_result)

        # Export options
        st.markdown("### 📤 Export Options")

        # Export to text file
        st.download_button(
            label="Download as TXT",
            data=comparison_result,
            file_name="mft_comparison.txt",
            mime="text/plain"
        )

        # Export to Markdown file
        try:
            md_buffer = BytesIO(comparison_result.encode("utf-8"))
            st.download_button(
                label="Download as Markdown (.md)",
                data=md_buffer,
                file_name="mft_comparison.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"❌ Markdown export failed: {e}")

