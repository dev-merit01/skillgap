@echo off
REM Deployment script for AI Job Matcher on Windows
REM Usage: deploy.bat [development|production]

set ENV=%1
if "%ENV%"=="" set ENV=development

echo 🚀 Deploying AI Job Matcher in %ENV% mode...

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found! Copy .env.example to .env and configure it.
    exit /b 1
)

REM Check if venv exists, create if not
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py migrate --noinput

REM Collect static files
echo 📂 Collecting static files...
python manage.py collectstatic --noinput

REM Run tests
echo 🧪 Running tests...
pytest --tb=short
if errorlevel 1 (
    echo ⚠️  Some tests failed, but continuing deployment...
)

if "%ENV%"=="production" (
    echo 🏭 Starting production server with Waitress...
    pip install waitress
    waitress-serve --port=8000 resume_matcher.wsgi:application
) else (
    echo 🧑‍💻 Starting development server...
    python manage.py runserver 0.0.0.0:8000
)

echo ✅ Deployment complete!
