@echo off
:: Check if ui_cert.pem file exists
if not exist keys/ui_cert.pem (
    echo Generating self-signed SSL certificate...
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout keys/ui_cert.key -out keys/ui_cert.pem  -subj "/CN=120.155.216.212"
    if errorlevel 1 (
        echo Failed to generate SSL certificate. Exiting.
        exit /b 1
    )
    echo SSL certificate generated successfully.
)

start /B pythonw -m streamlit run login.py --server.address 0.0.0.0 --server.port 8008 --server.headless true --server.enableCORS false --server.runOnSave true --server.sslCertFile keys/ui_cert.pem --server.sslKeyFile keys/ui_cert.key --runner.fastReruns true --browser.gatherUsageStats false --theme.base dark --logger.level debug --client.toolbarMode minimal --client.showErrorDetails true