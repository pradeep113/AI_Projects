import streamlit as st
import pandas as pd
import os
import hashlib
import logging

USER_DB = "users.csv"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if not logger.hasHandlers():
    fh = logging.FileHandler("auth.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_DB) and os.path.getsize(USER_DB) > 0:
        return pd.read_csv(USER_DB)
    else:
        return pd.DataFrame(columns=["username", "password"])

def save_user(username, password_hash):
    df = load_users()
    new_user = pd.DataFrame([{"username": username, "password": password_hash}])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DB, index=False)
    logger.info(f"User registered: {username}")

def login():
    st.subheader("User Authentication")

    choice = st.radio("Select Option", ("Login", "Register"))

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            users = load_users()
            hashed = hash_password(password)
            if ((users["username"] == username) & (users["password"] == hashed)).any():
                st.success("Login successful!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                logger.info(f"User '{username}' logged in successfully")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
                logger.warning(f"Failed login attempt for user: {username}")

    elif choice == "Register":
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            users = load_users()
            if new_user and new_pass:
                if new_user in users["username"].values:
                    st.warning("User already exists!")
                    logger.warning(f"Attempted to register existing user: {new_user}")
                else:
                    save_user(new_user, hash_password(new_pass))
                    st.success("Registered successfully! You can now log in.")
                    logger.info(f"New user resgistered: {new_user}")
            else:
                st.warning("Please fill all fields.")

