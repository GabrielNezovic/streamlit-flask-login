# streamlit-flask-login
 A barebones template for encrypted User Authentication using Streamlit as a front-end Web UI server and Flask as a back-end API server.

 ___
 
Install requirements:
* [Python 3.9](https://www.python.org/downloads/release/python-390/)
* [git](https://github.com/git-guides/install-git)

Clone this repo:
```
git clone https://github.com/GabrielNezovic/streamlit-flask-login.git
```
Install dependencies:
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

Open up the streamlit page in your browser:
```
http://localhost:8008/
```

<br>

Verify User Authentication using the following credentials:

```
user1: password1
user2: password2
```

___
<h3>Dependencies</h3>

* [Flask](https://pypi.org/project/Flask/)
* [Streamlit](https://pypi.org/project/Streamlit/)
* [Requests](https://pypi.org/project/Requests/)
* [pythonw](https://pypi.org/project/pythonw/) (optional)


___

[@GabrielNezovic](https://github.com/GabrielNezovic) 2023
