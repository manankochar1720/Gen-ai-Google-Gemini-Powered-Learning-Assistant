@echo off
title EduGenie Master Launcher
echo ===================================================
echo   🧞 Welcome to EduGenie Learning Assistant 🧞
echo ===================================================
echo.
echo [1/2] Launching FastAPI Backend Server...
start "" "%~dp0run_backend.bat"
echo.
echo Waiting for backend server initialization (3 seconds)...
timeout /t 3 /nobreak > nul
echo.
echo [2/2] Launching Streamlit Frontend Dashboard...
start "" "%~dp0run_frontend.bat"
echo.
echo 🧞 EduGenie is fully active! 
echo Check your browser at http://localhost:8501
echo.
echo (You can close this launcher window now. To stop the app, close the two terminal windows that popped up.)
timeout /t 5 > nul
exit
