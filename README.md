# streamlit-flask-login
 A barebones template for encrypted User Authentication using Streamlit as a front-end Web UI server and Flask as a back-end API server.

 ___

 <h3>Setup</h3>

1. Download the latest release from [here](https://github.com/GabrielNezovic/streamlit-flask-login/releases/tag/latest)

2. Unzip the files
 
3. Install [Python 3.9](https://www.python.org/downloads/release/python-390/)

4. Navigate to the extracted folder and install the dependencies with:  
  ```
  pip install -r requirements.txt
  ```

5. Add the Public IP address of your Streamlit Web UI server to the [flask_api.py](https://github.com/GabrielNezovic/streamlit-flask-login/blob/main/flask_api.py) file:
  ```
ui_ip = "<your.public.ip.address>" # the public ip address of your server
  ```

6. Add the Public IP address of your Streamlit Web UI server to the [start_ui_server.bat](https://github.com/GabrielNezovic/streamlit-flask-login/blob/main/start_ui_server.bat) file:
 ```
 openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout keys/ui_cert.key -out keys/ui_cert.pem  -subj "/CN=your.public.ip.address"
 ```
7. Add the Public IP address of your Flask API server to the [start_api_server.bat](https://github.com/GabrielNezovic/streamlit-flask-login/blob/main/start_api_server.bat) file:
 ```
 openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout keys/api_key.key -out keys/api_cert.crt -subj "/CN=your.public.ip.address"
 ```

<h3>Testing</h1>
Automatically generate self-signed SSL Certificates for both of the server apps and then launch the Flask API Server & Streamlit Web UI Server in series:

```
start_ui_server.bat
```

<br>

Alternatively, run the following commands separately to launch the servers -

* Start the Flask API server:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout keys/api_key.key -out keys/api_cert.crt -subj "/CN=your.public.ip.address"
python flask_api.py
```
* Start the Streamlit Web UI server:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout keys/ui_cert.key -out keys/ui_cert.pem  -subj "/CN=your.public.ip.address"
streamlit run login.py --server.address 0.0.0.0 --server.port 8008 --server.headless true --server.enableCORS false --server.runOnSave true --server.sslCertFile keys/ui_cert.pem --server.sslKeyFile keys/ui_cert.key --runner.fastReruns true --browser.gatherUsageStats false --theme.base dark --logger.level debug --client.toolbarMode minimal --client.showErrorDetails true
```

<br>

The Streamlit Web UI should then automatically be launched in your browser at:
```
https://<your.public.ip.address>:8008/
```

The Streamlit Web UI should be available locally via internal IPs, such as:

```
https://127.0.0.1:8008/
or
https://localhost:8008/
or
https://192.168.1.X:8008/
```

<br>

![image](https://github.com/GabrielNezovic/streamlit-flask-login/assets/138544043/054d0037-0ee3-4a38-accc-b0da1aa062d4)

Enter a Username, Password and some extra text to be saved against the user account and then click on the "Register" button.

This will then redirect you you to the Login page where you can log in with your new user details:
![image](https://github.com/GabrielNezovic/streamlit-flask-login/assets/138544043/62087d89-db9f-4cb5-87d1-e3b8ff6dd572)

Successful authentication will result in automatically retrieving and displaying the saved user data for that account.
![image](https://github.com/GabrielNezovic/streamlit-flask-login/assets/138544043/48a36d38-5f6d-4dfa-976e-e7d9dba8ffe2)


___
<h3>Troubleshooting</h3>

Open TCP Network Ports: 5000 + 8008 to allow communication between web browsers and both of the servers.

___
<h3>Dependencies</h3>

* [Flask](https://pypi.org/project/Flask/)
* [Streamlit](https://pypi.org/project/Streamlit/)
* [Requests](https://pypi.org/project/Requests/)
* [pythonw](https://pypi.org/project/pythonw/) (optional)


___

[@GabrielNezovic](https://github.com/GabrielNezovic) 2023




