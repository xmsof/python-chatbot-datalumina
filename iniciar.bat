@echo off
cd /d "%~dp0"
py python_chatbot_gui.py
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo ejecutar. Instala Python desde python.org
    echo.
    pause
)
