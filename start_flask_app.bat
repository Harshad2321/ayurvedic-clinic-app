@echo off
echo.
echo ===================================
echo   Ayurvedic Clinic Management App
echo ===================================
echo.
echo Starting the clinic app...
echo.

cd /d "c:\Users\harsh\clinic"
call .\venv\Scripts\Activate.ps1
python flask_app.py

echo.
echo App stopped. Press any key to close this window.
pause > nul