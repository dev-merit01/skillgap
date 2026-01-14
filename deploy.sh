#!/bin/bash

# Deployment script for AI Job Matcher
# Usage: ./deploy.sh [development|production]

set -e

ENV=${1:-development}

echo "🚀 Deploying AI Job Matcher in $ENV mode..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found! Copy .env.example to .env and configure it."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ $(echo "$PYTHON_VERSION 3.11" | awk '{print ($1 >= $2)}') -ne 1 ]]; then
    echo "❌ Python 3.11 or higher required. Current: $PYTHON_VERSION"
    exit 1
fi

# Activate virtual environment or create if doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# Run tests
echo "🧪 Running tests..."
pytest --tb=short || echo "⚠️  Some tests failed, but continuing deployment..."

if [ "$ENV" = "production" ]; then
    echo "🏭 Starting production server with Gunicorn..."
    
    # Check if Gunicorn is installed
    pip install gunicorn whitenoise
    
    # Kill existing process if running
    pkill -f gunicorn || true
    
    # Start Gunicorn in background
    gunicorn resume_matcher.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --timeout 120 \
        --access-logfile logs/access.log \
        --error-logfile logs/error.log \
        --daemon
    
    echo "✅ Production server started on port 8000"
    echo "📊 Logs: logs/access.log and logs/error.log"
else
    echo "🧑‍💻 Starting development server..."
    python manage.py runserver 0.0.0.0:8000
fi

echo "✅ Deployment complete!"
