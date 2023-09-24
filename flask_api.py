from flask import Flask, request, jsonify, redirect, url_for
import subprocess
import os
import bcrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import binascii
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import threading
import webbrowser

app = Flask(__name__)

# Load user data from a JSON file (replace with your file path)
user_data_file = "user_data.json"
# Specify the paths to your certificate and key files
cert_file = 'keys/api_cert.crt'
key_file = 'keys/api_key.key'

ui_ip = "<your.public.ip.address>" # the public ip address of your server
ui_port = "8008"

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key
jwt = JWTManager(app)

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
    padded_data = user_data.encode('utf-8') + (block_size - len(user_data) % block_size) * chr(block_size - len(user_data) % block_size).encode()
    ciphertext = cipher.encrypt(padded_data)
    return binascii.hexlify(ciphertext).decode()  # Convert ciphertext to hexadecimal string

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
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    encryption_key = get_random_bytes(32)
    iv = get_random_bytes(16)  # Generate a unique IV for each user

    # Encrypt the user data_text
    ciphertext = encrypt_user_data(user_data_text, encryption_key, iv)
    
    user_data[username] = {
        "salt": salt.decode('utf-8'),
        "hashed_password": hashed_password.decode('utf-8'),
        "encryption_key": encryption_key.hex(),
        "ciphertext": ciphertext,  # Store as a hexadecimal string
        "iv": iv.hex()
    }

    save_user_data(user_data)

    # Include encryption_key and iv in the response
    response_data = {
        "message": "User registered successfully",
        "encryption_key": encryption_key.hex(),
        "iv": iv.hex()
    }
    
    return jsonify(response_data), 201
    
# During authentication, send the encrypted user data back to Streamlit app
@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    username = data["username"]
    password = data["password"]

    user_data = load_user_data()

    if username in user_data:
        stored_salt = user_data[username]["salt"]
        stored_hashed_password = user_data[username]["hashed_password"]
        stored_encryption_key = bytes.fromhex(user_data[username]["encryption_key"])
        iv = bytes.fromhex(user_data[username]["iv"])

        # Verify the password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            if "ciphertext" in user_data[username]:
                # Send the encrypted user data back to Streamlit app
                return jsonify({"message": "Authentication successful",
                                "user_data": user_data[username]["ciphertext"],
                                "encryption_key": stored_encryption_key.hex(),
                                "iv": iv.hex()}), 200
            else:
                return jsonify({"message": "Authentication successful",
                                "user_data": None,
                                "encryption_key": stored_encryption_key.hex(),
                                "iv": iv.hex()}), 200
    return jsonify({"message": "Authentication failed"}), 401



@app.route("/startup", methods=["GET"])
def run_batch_file():
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

    # Start a new thread to run the subprocess
    subprocess_thread = threading.Thread(target=run_subprocess)
    subprocess_thread.start()

        
    return redirect(f'https://{ui_ip}:{ui_port}')
        


if __name__ == "__main__":
    print("Launch the UI Server @ https://127.0.0.1:5000/startup\n\n")
    
    webbrowser.open("https://127.0.0.1:5000/startup")
    
    app.run(host="0.0.0.0", port=5000, debug=False, ssl_context=(cert_file, key_file))
