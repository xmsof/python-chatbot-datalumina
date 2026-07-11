@echo off
echo ========================================
echo   Monica AI - Instalador
echo ========================================
echo.
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo ========================================
echo   Instalacion completa!
echo ========================================
echo.
echo Para ejecutar la interfaz grafica:
echo   python python_chatbot_gui.py
echo.
echo Para ejecutar en consola:
echo   python python_chatbot.py
echo.
echo La primera vez te pedira tu API key de Groq.
echo Gratis en: https://console.groq.com/keys
echo.
pause
