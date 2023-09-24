import streamlit as st
import requests
from Crypto.Cipher import AES
import binascii
import ssl

# Initialise login status
if "login" not in st.session_state:
    st.session_state["login"] = False

# Path to your self-signed certificate file for the flask server https auth
cert_file = "keys/api_cert.crt"
api_ip = "127.0.0.1"

def main():
    st.set_page_config(
        page_title="streamlit-flask-login",
        page_icon="🙌",
        layout="centered",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://everydayswag.org',
            'Report a Bug': 'mailto:dj@everydayswag.org',
        }
    )


    title = st.empty()


    # Add page styling and formatting
    st.markdown("""
        <style>
            [data-testid="stHeader"] {
                display: none;
            }
            
            footer {
                display: none;
            }

            [data-testid="block-container"] {
                top: -4rem;
            }
            
            .css-1xw8zd0 {
                border: 0;
            }
            
            button[data-testid="baseButton-secondary"] {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 420;
            }
            
        </style>
        """,
        unsafe_allow_html=True
    )

    # Check login status
    login = st.session_state["login"]

    if login:
        title.title("User Authentication")
        login_box = st.empty()
        response = ""
        authenticated = ""
        with login_box.container():
            with st.form("Login Page"):
                col1, col2, col3 = st.columns([1,1,0.5])
                with col1:
                    username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
                with col2:
                    password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
                with col3:
                    if st.form_submit_button("Login", use_container_width=True):
                        if username and password:
                            data = {
                                "username": username,
                                "password": password
                            }
                            response = requests.post(f'https://{api_ip}:5000/authenticate', json=data, verify=False)


                        if response and response.status_code == 200:
                            st.success("Authentication successful!")
                            authenticated = True

                        else:
                            st.error("Authentication failed. Check your credentials.")
     
        if authenticated:
            login_box.empty()
            title.empty()
                        
        if response:
            st.success("Decrypted User Data")
            st.toast("Login successful!")
            user_data_encrypted = response.json().get("user_data")
            
            if user_data_encrypted:
                encryption_key = bytes.fromhex(response.json()["encryption_key"])
                iv = bytes.fromhex(response.json()["iv"])

                # Convert the received hexadecimal data back to bytes
                user_data_bytes = binascii.unhexlify(user_data_encrypted)

                cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
                decrypted_data = cipher.decrypt(user_data_bytes)
                
                # Remove PKCS7 padding
                padding_length = decrypted_data[-1]
                decrypted_data = decrypted_data[:-padding_length]
            
                decrypted_text = decrypted_data.decode('utf-8')
                
                # Display the decrypted user data
                st.text_input("User Data", value=decrypted_text, type="password", label_visibility="collapsed")
            else:
                st.warning("No user data available for this user.")

    else:
        title.title("User Registration")
        with st.form("Registration Form"):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
            with col2:
                password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            
            user_data = st.text_area("User Data", placeholder="Data saved to the user account will be salted, hashed and encrypted with AES256 CBC encryption.", label_visibility="collapsed")
            login_message = st.empty()

            if st.form_submit_button("Register", use_container_width=True):
                if username and password and user_data:
                    data = {
                        "username": username,
                        "password": password,
                        "user_data": user_data
                    }
                    response = requests.post(f'https://{api_ip}:5000/register', json=data, verify=False)
                    
                    if response.status_code == 201:
                        login_message.success("Registration successful!")
                        login = True
                        st.session_state["login"] = login
                        st.experimental_rerun()

                    else:
                        login_message.error("Registration failed. Username may already exist.")

        # Create a button in the bottom right corner
        button_col, chat_col = st.columns([1, 4])
            
        # Use CSS to position the button in the bottom right corner by setting it to secondary type 
        with chat_col:
            login_button = st.empty()
            if login_button.button("Login", type="secondary"):
                login = True
                st.session_state["login"] = login
                st.experimental_rerun()
            
if __name__ == "__main__":
    main()