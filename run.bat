@echo off
taskkill /f /im pythonw.exe

start /B pythonw -m flask_api.py
start /B pythonw -m streamlit run login.py --browser.gatherUsageStats false --client.toolbarMode minimal --theme.base dark --logger.level info --server.port 8008 --server.enableStaticServing true