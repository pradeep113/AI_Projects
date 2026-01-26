import streamlit as st
import pandas as pd
from io import BytesIO
from backend import get_comparison

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
user_prompt = st.text_area("Your Requirements", placeholder="e.g., SFTP,FTPS support, cloud integration like sharepoint, MQ, S3 or blob")

# 🚀 Submit button
if st.button("Compare Tools"):
    if not user_prompt.strip():
        st.warning("Please enter your requirements.")
    elif not selected_tools:
        st.warning("Please select at least one MFT tool to compare.")
    else:
        with st.spinner("Generating comparison..."):
            result_text, result_df = get_comparison(user_prompt, selected_tools)
            st.markdown("### 🧾 Comparison Result")
            st.write(result_text)

            if not result_df.empty:
                st.markdown("### 📊 Structured Comparison Table")
                st.dataframe(result_df)

                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    result_df.to_excel(writer, index=False, sheet_name="MFT Comparison")
                st.download_button(
                    label="📥 Download Excel",
                    data=buffer.getvalue(),
                    file_name="mft_comparison.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("No structured table found in the response.")
