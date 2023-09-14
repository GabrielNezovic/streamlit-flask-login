from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Sample user data
user_data = {
    "user1": "password1",
    "user2": "password2",
}

# Use a secret key or unique text string here - can be anything you like
hash = "molemander"

# Dictionary to store single-use special keys
special_keys = {}

# Function to generate a special key from a custom input
def generate_special_key(custom_input):
    # Generate a random 8-digit number
    random_number = random.randint(10000000, 99999999)
    
    # Calculate the key as the combined numerical value of each character
    # in the custom input string multiplied by the random number
    key_value = sum([ord(char) for char in custom_input]) * random_number
    
    # Convert the key value to a string
    key = str(key_value)
    
    # Store the key in the special_keys dictionary
    special_keys[key] = True
    
    return key

# Function to validate and invalidate a special key
def validate_and_invalidate_special_key(key):
    if key in special_keys:
        del special_keys[key]
        return True
    return False

def validate_username_password(username, encrypted_password, special_key):
    # Decrypt the password received from the Streamlit app
    decrypted_password = decrypt_password(encrypted_password, special_key)

    # Check if the username and decrypted password match the stored data
    if username in user_data and user_data[username] == decrypted_password:
        return True
    return False

# Function to decrypt the password
def decrypt_password(encrypted_password, key):
    decrypted_password = []
    for i in range(len(encrypted_password)):
        char = encrypted_password[i]
        key_char = key[i % len(key)]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        decrypted_password.append(decrypted_char)
    return "".join(decrypted_password)

def generate_api_token(username):
    # Generate a secure API token here
    # Using a static token as example:
    return "your-api-token-for-" + username

@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    username = data["username"]
    encrypted_password = data["password"]
    special_key = data.get("special_key")  # Get the special key from the request

    # Username/password validation 
    if validate_username_password(username, encrypted_password, special_key):
        # Generate an API token and return it to the Streamlit app
        api_token = generate_api_token(username)
        return jsonify({"api_token": api_token}), 200
    else:
        return jsonify({"message": "Authentication failed"}), 401

@app.route("/generate-special-key", methods=["POST"])
def generate_and_return_special_key():
    # Generate a single-use special key based on the hash
    key = generate_special_key(hash)
    return jsonify({"special_key": key}), 200

if __name__ == "__main__":
    app.run()
