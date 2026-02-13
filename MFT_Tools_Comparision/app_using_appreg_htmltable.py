import streamlit as st
import pandas as pd
from io import BytesIO
from backend_using_appreg_test import run_agent_workflow

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
        combined_prompt = (
            f"Compare the following MFT tools: {', '.join(selected_tools)} "
            f"based on these requirements: {user_prompt}"
        )

        with st.spinner("Contacting Foundry agent..."):
            comparison_result = run_agent_workflow(combined_prompt)

        st.subheader("📊 Comparison Result")
        st.write(comparison_result)

        # Export options
        st.markdown("### 📤 Export Options")

        # TXT export
        st.download_button(
            label="Download as TXT",
            data=comparison_result,
            file_name="mft_comparison.txt",
            mime="text/plain"
        )

        # Markdown export
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

        # HTML export with table handling
        try:
            html_content = "<!DOCTYPE html><html><head><meta charset='utf-8'><title>MFT Comparison</title></head><body>"
            html_content += "<h1>MFT Tool Comparison Result</h1>"

            # Try to detect tabular structure
            try:
                # If the response looks like CSV/Markdown table, attempt to parse
                df = pd.read_csv(BytesIO(comparison_result.encode("utf-8")), sep="|", engine="python")
                html_content += df.to_html(index=False, escape=False)
            except Exception:
                # Fallback: render as preformatted text
                html_content += f"<pre>{comparison_result}</pre>"

            html_content += "</body></html>"

            html_buffer = BytesIO(html_content.encode("utf-8"))
            st.download_button(
                label="Download as HTML",
                data=html_buffer,
                file_name="mft_comparison.html",
                mime="text/html"
            )
        except Exception as e:
            st.error(f"❌ HTML export failed: {e}")

