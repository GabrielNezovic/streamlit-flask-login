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
<h3>Testing</h1>
Windows users can start both servers at the same time with: 

```
run.bat
```

<br>

Alternatively, run the following 2 commands separately -
* Start the Flask API server:
```
python flask_api.py
```
* Start the Streamlit Web UI server:
```
streamlit run login.py --server.port 8008 --theme.base dark --logger.level info --browser.gatherUsageStats false
```

<br>

The following page will automatically be launched in your browser:
```
http://localhost:8008/
```

A public URL will also be made available at:

```
http://<your.public.ip.address>:8008/
```

<br>

User Authentication can then be verified using the following credentials:

```
user1: password1
user2: password2
```

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
