# streamlit-flask-login
 A barebones template for encrypted User Authentication using Streamlit as a front-end web UI and Flask as a back-end API server.

 ___
 
 Install requirements:
 * Python 3.9
 ```
pip install -r requirements.txt
```
 
Windows user can start both servers at the same time with:
```
run.bat
```

Alternatively, run these commands in 2 separate consoles:
```
pythow flask_api.py
```
```
streamlit run login.py --browser.gatherUsageStats false --client.toolbarMode minimal --theme.base dark --logger.level info --server.port 8008 --server.enableStaticServing true
```

Open up the streamlit page:
```
http://localhost:8008/
```

Verify User Authentication using sample credentials:

```
user1: password1
user2: password2
```

___

[@GabrielNezovic](https://github.com/GabrielNezovic)
