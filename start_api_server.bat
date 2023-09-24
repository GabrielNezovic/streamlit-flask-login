@echo off
:: Check if cert.pem file exists
if not exist keys/api_cert.pem (
    echo Generating self-signed SSL certificate...
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout keys/api_key.key -out keys/api_cert.crt -subj "/CN=120.155.216.212"
    if errorlevel 1 (
        echo Failed to generate SSL certificate. Exiting.
        exit /b 1
    )
    echo SSL certificate generated successfully.
)

start pythonw flask_api.py