#### [flask_api.py]
from flask import Flask, request, jsonify, redirect, url_for
import subprocess
import os
import bcrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import binascii
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
)
import threading
import webbrowser
from datetime import timedelta
import urllib3

app = Flask(__name__)
app.config['SERVER_NAME'] = '<your.public.ip.address>:5000'  # Replace with your custom domain and port
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Replace with your secret key

jwt = JWTManager(app)

# Declare a global variable to track the subprocess_thread
subprocess_thread = None

# Disable SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load user data from a JSON file (replace with your file path)
user_data_file = "user_data.json"
# Specify the paths to your certificate and key files
cert_file = "keys/api_cert.crt"
key_file = "keys/api_key.key"

# <your.public.ip.address>
ui_ip = "<your.public.ip.address>"  # the public ip address of your streamlit server
ui_port = "8008"

# <your.public.ip.address>
api_ip = "<your.public.ip.address>" # the public ip address of your flask server
api_port = "5000"

def load_user_data():
    try:
        with open(user_data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open(user_data_file, "w") as file:
        json.dump(data, file)

# During registration, encrypt and save user data in JSON file
def encrypt_user_data(user_data, encryption_key, iv):
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    block_size = 16
    padded_data = (
        user_data.encode("utf-8")
        + (block_size - len(user_data) % block_size)
        * chr(block_size - len(user_data) % block_size).encode()
    )
    ciphertext = cipher.encrypt(padded_data)
    return binascii.hexlify(ciphertext).decode()  # Convert ciphertext to hexadecimal string
    
# Function to retrieve user data based on the current user's identity
def retrieve_user_data(username):
    user_data = load_user_data()
    if username in user_data:
        encryption_key = bytes.fromhex(user_data[username]["encryption_key"])
        iv = bytes.fromhex(user_data[username]["iv"])
        user_data_encrypted = user_data[username]["ciphertext"]

        # Convert the received hexadecimal data back to bytes
        user_data_bytes = binascii.unhexlify(user_data_encrypted)

        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(user_data_bytes)

        # Remove PKCS7 padding
        padding_length = decrypted_data[-1]
        decrypted_data = decrypted_data[:-padding_length]

        try:
            # Attempt to decode the decrypted text as JSON
            decrypted_text = decrypted_data.decode("utf-8")
            user_data = decrypted_text
            # Return the decrypted text as a JSON response
            return user_data
        except:
            # Handle the case where decrypted_text is not valid JSON
            print(f"Decrypted text is not valid: {decrypted_text}")

    else:
        return {"error": "User not found or data not available"}

# New route to check for presence of JWT token in the "Authorization" header
@app.route("/check_token", methods=["GET"])
@jwt_required()
def check_token():
    current_user = get_jwt_identity()
    if current_user:
        user_data = retrieve_user_data(current_user)  # Retrieve user data based on the current user
        print(user_data)
        if user_data:
            return jsonify(user_data), 200  # Return user data as JSON response

    return jsonify({"message": "User not found or data not available"}), 404

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    user_data_text = data["user_data"]  # Change variable name to distinguish from user_data dictionary

    user_data = load_user_data()

    if username in user_data:
        return jsonify({"message": "Username already exists"}), 400

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    encryption_key = get_random_bytes(32)
    iv = get_random_bytes(16)  # Generate a unique IV for each user

    # Encrypt the user data_text
    ciphertext = encrypt_user_data(user_data_text, encryption_key, iv)

    user_data[username] = {
        "salt": salt.decode("utf-8"),
        "hashed_password": hashed_password.decode("utf-8"),
        "encryption_key": encryption_key.hex(),
        "ciphertext": ciphertext,  # Store as a hexadecimal string
        "iv": iv.hex(),
    }

    save_user_data(user_data)

    # Include encryption_key and iv in the response
    response_data = {
        "message": "User registered successfully",
        "encryption_key": encryption_key.hex(),
        "iv": iv.hex(),
    }

    return jsonify(response_data), 201

# During authentication, save the JWT token and send the JWT token back to the Streamlit app
@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    username = data["username"]
    password = data["password"]

    user_data = load_user_data()

    if username in user_data:
        stored_salt = user_data[username]["salt"]
        stored_hashed_password = user_data[username]["hashed_password"]
        # Verify the password
        if bcrypt.checkpw(
            password.encode("utf-8"), stored_hashed_password.encode("utf-8")
        ):
            access_token = create_access_token(
                identity=username, expires_delta=timedelta(days=1)
            )  # Token expires in 1 day

            # Save the JWT token in the user's account data
            user_data[username]["jwt_token"] = access_token

            save_user_data(user_data)

            return jsonify(
                {"message": "Authentication successful", "access_token": access_token}
            ), 200

    return jsonify({"message": "Authentication failed"}), 401

@app.route("/startup", methods=["GET"])
def run_batch_file():
    global subprocess_thread
    
    # Check if the subprocess_thread is already running
    if subprocess_thread and subprocess_thread.is_alive():
        return redirect(f"https://{ui_ip}:{ui_port}/")

    batch_file_path = os.path.join(os.path.dirname(__file__), "start_ui_server.bat")

    cmd = f'"{batch_file_path}"'
    print(cmd)

    def run_subprocess():
        try:
            subprocess.run(cmd, text=True, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            batch_message.error(f"❌ Error: {e}")
        except FileNotFoundError:
            batch_message.error(f"❌ Error: {batch_file_path} not found")

    # Start the Flask app in a new thread
    subprocess_thread = threading.Thread(target=run_subprocess)
    subprocess_thread.start()

    # Redirect to the Streamlit Web UI Public IP
    return redirect(f"https://{ui_ip}:{ui_port}/")

# Create a Protected endpoint that requires the JWT token to be provided in the request header
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected_route():

    current_user = get_jwt_identity()

    user_data = load_user_data()

    if current_user in user_data:
        encryption_key = bytes.fromhex(user_data[current_user]["encryption_key"])
        iv = bytes.fromhex(user_data[current_user]["iv"])
        user_data_encrypted = user_data[current_user]["ciphertext"]

        # Convert the received hexadecimal data back to bytes
        user_data_bytes = binascii.unhexlify(user_data_encrypted)

        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(user_data_bytes)

        # Remove PKCS7 padding
        padding_length = decrypted_data[-1]
        decrypted_data = decrypted_data[:-padding_length]
        
        # decrypt the user data and send it back to the streamlit app
        decrypted_text = decrypted_data.decode("utf-8")

        return jsonify(
            {"message": "User data decrypted successfully", "user_data": decrypted_text}
        ), 200
    else:
        return jsonify({"message": "User not found or data not available"}), 404

if __name__ == "__main__":
    # Open the streamlit web ui on launch
    webbrowser.open(f'https://{api_ip}:{api_port}/startup')
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=(cert_file, key_file))