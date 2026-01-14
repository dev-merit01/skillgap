@echo off
REM Firebase Setup Validator for Windows
REM Runs the Firebase validation script with proper environment

echo ========================================
echo Firebase Setup Validator
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please create it first: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run validation script
python scripts\validate_firebase.py

REM Keep window open to see results
echo.
pause
