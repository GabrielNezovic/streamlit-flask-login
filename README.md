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

5. Add the Public IP address of your Streamlit Web UI server to the /flask.py file:
  ```
ui_ip = "<your.public.ip.address>" # the public ip address of your server
  ```

<h3>Testing</h1>
Automatically generate self-signed SSL Certificates and launch the Flask API Server & Streamlit Web UI Server

```
start_ui_server.bat
```

<br>

Alternatively, run the following 2 commands separately -
* Start the Flask API server:
```
python flask_api.py
```
* Start the Streamlit Web UI server:
```
streamlit run login.py --server.address 0.0.0.0 --server.port 8008 --server.headless true --server.enableCORS false --server.runOnSave true --server.sslCertFile keys/ui_cert.pem --server.sslKeyFile keys/ui_cert.key --runner.fastReruns true --browser.gatherUsageStats false --theme.base dark --logger.level debug --client.toolbarMode minimal --client.showErrorDetails true
```

<br>

The following page will automatically be launched in your browser:
```
https://localhost:8008/
```

A public URL will also be made available at:

```
https://<your.public.ip.address>:8008/
```

<br>

Enter a Username, Password and some extra text to save against the user account and then click on the "Register" button.
This will automatically take you to the Login page - try to log in with your new details to retrieve and display the user data.

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
