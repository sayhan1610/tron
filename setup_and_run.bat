@echo off
:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and add it to your PATH.
    pause
    exit /b
)

:: Create a virtual environment
python -m venv venv
call venv\Scripts\activate

:: Install the dependencies
pip install -r requirements.txt

:: Run the game
python main.py

:: Deactivate the virtual environment
deactivate
