import streamlit as st
import os
import base64
from openai import AzureOpenAI
from auth import login  # Assuming 'auth.py' handles login logic

# Session state to manage login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Page Configuration
st.set_page_config(page_title="GoAnywhere AI Assistant", layout="wide")

# Login First
if not st.session_state["logged_in"]:
    login()  # Redirects to login function
else:
    # Sidebar for API Key Input (Shown Only After Login)
    with st.sidebar:
        st.title("Settings ⚙️")

        with st.expander("Enter API Key 🔑"):
            api_key = st.text_input("API Key", type="password")  # Masked input field for security
            if api_key:
                st.success("API Key saved successfully!")

    # Main App Layout
    st.title("🚀 GoAnywhere AI Assistant")
    # Logout Button
    if st.button("Logout"):
        st.session_state["logged_in"] = False  # Reset login state
        st.success("Logged out successfully! Please refresh the page to log in again.")
    st.write("Enter a prompt below to interact with Azure OpenAI.")

    # Check if API Key is entered before proceeding
    if api_key:
        prompt = st.text_area("Enter your query:", placeholder="Ask something...")

        if st.button("Get Response"):
            try:
                # Initialize Azure OpenAI client with user-provided API key
                client = AzureOpenAI(
                    azure_endpoint="https://pradeep-azai-openai.openai.azure.com/",
                    api_key=api_key,  # Use the input API key
                    api_version="2025-01-01-preview",
                )

                # Prepare the chat prompt
                chat_prompt = [
                    {"role": "system", "content": [{"type": "text", "text": "You are a Fortra GoAnywhere MFT expert and help people provide information."}]},
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ]

                # Generate completion response
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=chat_prompt,
                    max_tokens=800,
                    temperature=0.7,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    stream=False
                )

                # Display the response
                response_text = completion.choices[0].message.content
                st.subheader("AI Response:")
                st.write(response_text)

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning("⚠️ Please enter your API key in the sidebar before proceeding.")



