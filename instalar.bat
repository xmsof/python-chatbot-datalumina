@echo off
cd /d "%~dp0"
echo ========================================
echo   Monica AI - Instalador
echo ========================================
echo.
py --version
if errorlevel 1 (
    echo.
    echo ERROR: Instala Python desde https://www.python.org/downloads/
    echo.
    pause
    exit /b
)
echo Instalando dependencias...
py -m pip install -r requirements.txt
echo.
echo Listo! Ahora doble clic en iniciar.bat
echo.
pause
