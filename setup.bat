@echo off
echo Setting up Britô Cell E-commerce...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo Error creating virtual environment.
    pause
    exit /b 1
)

call venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Error activating virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created. Please edit it with your configuration.
) else (
    echo .env file already exists.
)

echo Creating uploads directory...
mkdir static\images\products 2>nul

echo Initializing database...
python run.py init

echo.
echo Setup complete!
echo.
echo To start the development server, run:
echo   .\venv\Scripts\activate
echo   python run.py
echo.
echo Admin access:
echo   URL:      http://localhost:5000/admin
echo   Username: admin
echo   Password: admin123
echo.
pause
