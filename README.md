# streamlit-flask-login
 A barebones template for encrypted User Authentication using Streamlit as a front-end Web UI server and Flask as a back-end API server.

 ___
 
 Install requirements:
 * Python 3.9
 ```
pip install -r requirements.txt
```

<br>

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
streamlit run login.py --browser.gatherUsageStats false --client.toolbarMode minimal --theme.base dark --logger.level info --server.port 8008 --server.enableStaticServing true
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

[@GabrielNezovic](https://github.com/GabrielNezovic) 2023
