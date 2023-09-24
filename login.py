####  [login.py]
import streamlit as st
import requests
from Crypto.Cipher import AES
import binascii
import ssl
import streamlit.components.v1 as components  # Import the HTML component
import urllib3
from requests.exceptions import ConnectionError
import extra_streamlit_components as stx
import json

# Disable SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialise login status
if "login" not in st.session_state:
    st.session_state["login"] = False

# Check login status
login = st.session_state["login"]
# Path to your self-signed certificate file for the flask server https auth
cert_file = "keys/api_cert.crt"

# <your.public.ip.address>
ui_ip = "<your.public.ip.address>"  # the public ip address of your streamlit server
ui_port = "8008"

# <your.public.ip.address>
api_ip = "<your.public.ip.address>" # the public ip address of your flask server
api_port = "5000"

def main():
    st.set_page_config(
        page_title="streamlit-flask-login",
        page_icon="🙌",
        layout="centered",
        initial_sidebar_state="collapsed",
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
    
    if "cookie_sesh" not in st.session_state:
        st.session_state["cookie_sesh"] = ""
        
    cookie_sesh = st.session_state["cookie_sesh"]
    
    def cookie_time():
        # Create a Cookie Manager component
        cookie_manager = stx.CookieManager()
        # Get all cookies
        cookies = cookie_manager.get_all()
        # Check for the JWT token cookie
        jwt_token_cookie = cookies.get("jwt_token")
        # If JWT token cookie is found, proceed with authentication
        if jwt_token_cookie:
            headers = {"Authorization": f"Bearer {jwt_token_cookie}"}
            try:
                response = requests.get(f'https://{api_ip}:{api_port}/check_token', headers=headers, verify=False)

                if response.status_code == 200:  # if token is valid
                    st.session_state["jwt_token_cookie"] = jwt_token_cookie  # Set jwt_token_cookie in session state
                    try:
                        json_data = response.json()  # Parse JSON response from the server
                        # Convert JSON data to a formatted string
                        json_str = json.dumps(json_data, indent=4)
                        # Display the formatted JSON data using st.markdown
                        st.markdown(f"```json\n{json_str}\n```")
                        st.session_state["cookie_sesh"] = True
                        st.session_state["login"] = True
                    
                    except Exception as json_error:
                        st.error(f"Error parsing JSON response: {str(json_error)}")
                else:
                    st.error(f"Error: Status code {response.status_code}")
                    st.error(response.text)

            except Exception as request_error:
                st.error(f"Error making the request: {str(request_error)}")
    try:
        cookie_time()
    except:
        print("?")
        
    # Check login status
    login = st.session_state["login"]
    cookie_sesh = st.session_state["cookie_sesh"]

    if login:
        if not cookie_sesh:
            # Check jwt_token_cookie
            jwt_token_cookie = st.session_state.get("jwt_token_cookie", None)
            if jwt_token_cookie:
               headers = {"Authorization": f"Bearer {jwt_token_cookie}"}
            else:
               headers = {}
               
            title.title("User Authentication")
            login_box = st.empty()
            login_message_display = st.empty()
            response = ""
            if "authenticated" not in st.session_state:
                st.session_state["authenticated"] = ""
                
            authenticated = st.session_state["authenticated"]
            
            # Create a session cookie to store the JWT token
            jwt_token_cookie = st.session_state.pop("jwt_token_cookie", None)
            
            if jwt_token_cookie:
                # If the JWT token cookie exists, set the token in the headers
                headers = {"Authorization": f"Bearer {jwt_token_cookie}"}
            else:
                headers = {}

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
                                response = requests.post(f'https://{api_ip}:{api_port}/authenticate', json=data, verify=False)


                            if response and response.status_code == 200:
                                jwt_token = response.json().get("access_token")
                                print(jwt_token)
                                # When setting the JWT token cookie, specify an expiration time (in seconds)
                                # For example, set it to expire in 1 day (24 hours * 60 minutes * 60 seconds)
                                jwt_token_expiration_seconds = 24 * 60 * 60  # 1 day in seconds
                                st.session_state["jwt_token_cookie"] = jwt_token  # Store in session state
                                login_message_display.success("Authentication successful.")
                                st.session_state["authenticated"] = True
                            else:
                                login_message_display.error("Authentication failed. Check your credentials.")
                                
            authenticated = st.session_state["authenticated"]

            # If authenticated, update the login state and rerun the Streamlit app
            if authenticated:
                login_box.empty()
                login_message_display.empty()
                st.session_state["login"] = True
 
            if response:                        
                # Save the JWT token as a session cookie
                components.html(
                    f'<script>document.cookie="jwt_token={jwt_token};path=/;max-age={jwt_token_expiration_seconds}";</script>',
                    height=0,
                )
                st.success("Decrypted User Data")
                st.toast("Login successful!")
                
                # Make a request to the protected route using the JWT token in the request header
                protected_response = requests.get(f'https://{api_ip}:{api_port}/protected', headers={"Authorization": f"Bearer {jwt_token}"}, verify=False)
                

                if protected_response.status_code == 200:
                    decrypted_text = protected_response.json().get("user_data")
                    if decrypted_text:
                        print(decrypted_text)
                        # Display the decrypted user data as a password field
                        user_data_input = st.text_input("User Data", value=decrypted_text, type="password", label_visibility="collapsed")
                        ## Update user data if changed
                        #if user_data_input != decrypted_text:
                        #    # Handle user data update logic here, e.g., update the user_data on the server
                        #    new_user_data = user_data_input  # Get the new user data from the input field
                        #    # Make a request to update user data on the server
                        #    update_response = requests.post(
                        #        f'https://{api_ip}:{api_port}/update_user_data',
                        #        headers={"Authorization": f"Bearer {jwt_token}"},
                        #        json={"user_data": new_user_data},
                        #        verify=False
                        #    )
                        #    if update_response.status_code == 200:
                        #        st.success("User data updated successfully.")
                        #    else:
                        #        st.error("Failed to update user data.")
                    else:
                        st.warning("No user data available for this user.")
                else:
                    st.error("Failed to retrieve decrypted user data.")
        else:
            if st.button("Logout"):
                st.code("Log me out bb.")
    else:
        # Check login status
        login = st.session_state["login"]
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
                    response = requests.post(f'https://{api_ip}:{api_port}/register', json=data, verify=False)
                    
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