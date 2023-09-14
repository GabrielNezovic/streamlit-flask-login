@echo off
taskkill /f /im pythonw.exe

start /B pythonw flask_api.py
start /B pythonw -m streamlit run login.py --server.port 8008 --theme.base dark --browser.gatherUsageStats false --logger.level info