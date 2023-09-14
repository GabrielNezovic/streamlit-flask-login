import streamlit as st
import requests

# Function to encrypt the password
def encrypt_password(password, key):
    encrypted_password = []
    for i in range(len(password)):
        char = password[i]
        key_char = key[i % len(key)]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        encrypted_password.append(encrypted_char)
    return "".join(encrypted_password)

# Function to authenticate the user
def authenticate_user(username, password, special_key):
    # Encrypt the password before sending it
    encrypted_password = encrypt_password(password, special_key)

    data = {"username": username, "password": encrypted_password, "special_key": special_key}
    response = requests.post("http://127.0.0.1:5000/authenticate", json=data)
    return response

# Streamlit UI for username and password input
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    # Get the special key from the Flask app
    special_key_response = requests.post("http://127.0.0.1:5000/generate-special-key")
    special_key = special_key_response.json().get("special_key")

    if special_key:
        response = authenticate_user(username, password, special_key)
        if response.status_code == 200:
            api_token = response.json()["api_token"]
            st.success("Login successful!")
            st.write(f"Your API token: {api_token}")
        else:
            st.error("Authentication failed. Please check your credentials.")
    else:
        st.error("Failed to obtain the special key.")