# 🎯 AI Job Matcher

A production-quality, privacy-first Django web application that uses AI to analyze how well a candidate's CV matches a job description. Built with Firebase Authentication and OpenAI integration.

## 🌟 Key Features

- **🔒 Privacy-First Design**: All files processed in memory, nothing stored on disk or database
- **🔐 Firebase Authentication**: Secure Google sign-in with token verification
- **🤖 AI-Powered Analysis**: OpenAI-compatible LLM provides structured matching insights
- **📊 Comprehensive Scoring**: Match score (0-100%), strengths, gaps, and actionable suggestions
- **🚀 Modern SaaS UI**: Clean, professional interface with real-time feedback
- **⚡ Stateless Architecture**: No user data persistence, fully ephemeral processing
- **🛡️ Security Features**: Rate limiting, CSRF protection, input validation
- **📄 Multi-Format Support**: Handles PDF and DOCX files up to 2MB

## 🏗️ Architecture

### Core Principles

1. **Zero Persistence**: CVs and job descriptions are never written to disk or database
2. **In-Memory Processing**: All file parsing happens in BytesIO objects
3. **Stateless API**: Each request is independent, no session state maintained
4. **Token-Based Auth**: Firebase ID tokens verified on each request

### Technology Stack

- **Backend**: Django 4.2+ (Python 3.11+)
- **Authentication**: Firebase Admin SDK
- **AI/LLM**: OpenAI API (gpt-4o-mini recommended)
- **File Parsing**: pdfplumber (PDF), python-docx (DOCX)
- **Frontend**: Vanilla JavaScript + Firebase JS SDK
- **Styling**: Pure CSS with modern design patterns

### System Flow

```
User → Firebase Google Sign-In → Get ID Token
    ↓
Paste Job Description + Upload CV → POST /analyze/
    ↓
Django Backend:
  1. Verify Firebase Token ✓
  2. Validate Inputs (size, format, length) ✓
  3. Parse CV in Memory (BytesIO) ✓
  4. Send to LLM API ✓
  5. Parse JSON Response ✓
  6. Return Results ✓
    ↓
Display Analysis Results
    ↓
Data Discarded (nothing persisted)
```

## 🔒 Privacy & Security

### Privacy Design

- **No Database Storage**: The application uses Django's minimal database only for sessions. No user data, CVs, or job descriptions are stored.
- **In-Memory Only**: Files are read directly into memory using `BytesIO` and processed without touching the filesystem.
- **Immediate Disposal**: All document data is garbage collected immediately after analysis.
- **No Logging of Sensitive Data**: Only metadata (email, timestamps) logged, never file contents.

### Security Features

- **Firebase Token Verification**: Every API request validated against Firebase
- **Rate Limiting**: 10 requests per hour per IP/UID (configurable)
- **CSRF Protection**: Django's built-in CSRF middleware
- **Input Validation**: 
  - File size limits (2MB)
  - File type restrictions (PDF/DOCX only)
  - Job description length limits (10,000 chars)
- **HTTPS Enforcement**: SSL redirect in production mode
- **Secure Headers**: XSS protection, frame denial, content type sniffing prevention

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip and virtualenv
- Firebase project with Authentication enabled
- OpenAI API key (or compatible LLM endpoint)

### Step 1: Clone and Setup Virtual Environment

```bash
git clone <repository-url>
cd resume-job-match

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Firebase Setup

**⚠️ IMPORTANT**: Follow the comprehensive [Firebase Setup Guide](FIREBASE_SETUP.md) for step-by-step instructions.

**Quick summary:**
1. Create Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable **Authentication** → **Google Sign-In**
3. Download service account credentials → save as `firebase-credentials.json`
4. Get web config and update `analyzer/templates/analyzer/home.html`
5. Validate setup: `python scripts/validate_firebase.py`

See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed instructions with screenshots.

### Step 3: Environment Configuration

A `.env` file has been created for you. Update it with your credentials:

```bash
# Edit .env with your credentials
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

Required environment variables:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Firebase - Point to your credentials file
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# OpenAI - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
```
Validate Firebase Configuration

Before starting the server, validate your Firebase setup:

```bash
python scripts/validate_firebase.py
```

This checks:
- ✅ Firebase credentials file exists and is valid
- ✅ Environment variables are correctly set
- ✅ Firebase Admin SDK can initialize
- ✅ OpenAI API key is configured

If all checks pass, proceed to the next step. Otherwise, see [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for troubleshooting.
```

Get these values from Firebase Console → Project Settings → General → Your apps

### Step 5: Initialize Django

```bash
# Run migrations (only for Django sessions)
python manage.py migrate

# Collect static files
python manage.py colle (optional for development)ctstatic --noinput

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

**Test the application:**
1. Go to `/app/` or click "Start Free" on landing page
2. Click "Sign in with Google"
3. Authorize with your Google account
4. Upload a CV (PDF or DOCX) and paste a job description
5. Click "Analyze Match" and wait for results!

## 🚀 Production Deployment

### Environment Configuration

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECRET_KEY=use-a-strong-random-key-here
```

### Using Gunicorn

```bash
pip install gunicorn whitenoise

# Run with Gunicorn
gunicorn resume_matcher.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/resume-job-match/staticfiles/;
    }
}
```

### Cloud Deployment Options

- **Google Cloud Run**: Native Firebase integration
- **AWS Elastic Beanstalk**: Easy Django deployment
- **Heroku**: Quick setup with buildpacks
- **DigitalOcean App Platform**: Managed containers

## 🔧 Configuration Options

### LLM Settings

```env
# Use different models
OPENAI_MODEL=gpt-4  # More accurate but slower
OPENAI_MODEL=gpt-3.5-turbo  # Faster, less expensive

# Adjust response quality
OPENAI_MAX_TOKENS=1500  # Longer responses
OPENAI_TEMPERATURE=0.5  # More creative (0.0-1.0)

# Use alternative providers (Anthropic, Azure, etc.)
OPENAI_API_BASE=https://api.anthropic.com/v1
```

### Rate Limiting

```env
RATE_LIMIT_REQUESTS=20  # Increase to 20 per window
RATE_LIMIT_WINDOW=7200  # 2 hours (in seconds)
```

### File Upload Limits

Edit `resume_matcher/settings.py`:

```python
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
MAX_JOB_DESCRIPTION_LENGTH = 20000  # 20k chars
```

## 📖 API Documentation

### POST /analyze/

Analyze CV against job description (requires authentication).

**Headers:**
```
Authorization: Bearer <firebase_id_token>
Content-Type: multipart/form-data
```

**Body:**
- `job_description` (text): Full job posting text
- `cv_file` (file): PDF or DOCX file

**Success Response (200):**
```json
{
  "success": true,
  "user": {
    "email": "user@example.com",
    "name": "John Doe"
  },
  "analysis": {
    "match_score": 75,
    "strengths": [
      "Strong Python and Django experience",
      "5+ years in backend development",
      "Experience with cloud platforms"
    ],
    "missing_skills": [
      "Kubernetes certification",
      "GraphQL experience"
    ],
    "improvement_suggestions": [
      "Obtain AWS certification",
      "Build projects demonstrating GraphQL",
      "Add metrics to quantify achievements"
    ],
    "summary": "Strong candidate with relevant experience..."
  }
}
```

**Error Responses:**

- `401 Unauthorized`: Invalid or missing Firebase token
- `400 Bad Request`: Missing fields or invalid file
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Processing or LLM error

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-django

# Run tests
pytest

# Run with coverage
pytest --cov=analyzer --cov-report=html
```

## 🤔 How It Works

### Firebase Authentication Flow

1. User clicks "Sign in with Google" button
2. Firebase JS SDK opens Google OAuth popup
3. User approves access
4. Firebase returns ID token to frontend
5. Frontend includes token in `Authorization` header
6. Django backend verifies token with Firebase Admin SDK
7. Extracts `uid` and `email` from verified token
8. Proceeds with request if valid

### CV Parsing Process

```python
# File never touches disk
file_content = request.FILES['cv_file'].read()  # bytes in memory
pdf_file = BytesIO(file_content)  # in-memory file object

# Parse directly from memory
with pdfplumber.open(pdf_file) as pdf:
    text = extract_text(pdf)

# After this function returns, all objects are garbage collected
```

### LLM Integration

The system uses a structured prompt that forces JSON output:

```
System: You are an HR analyst. Respond ONLY with valid JSON...

User: Analyze this CV against this job...
JOB DESCRIPTION: ...
CANDIDATE CV: ...

LLM Response:
{
  "match_score": 75,
  "strengths": [...],
  "missing_skills": [...],
  ...
}
```

The response is validated to ensure all required fields exist and have correct types.

## 🐛 Troubleshooting

### Firebase Authentication Fails

- Check Firebase credentials path is correct
- Verify Firebase project has Authentication enabled
- Confirm Google sign-in method is enabled in Firebase Console
- Check frontend Firebase config matches your project

### LLM API Errors

- Verify OpenAI API key is valid and has credits
- Check `OPENAI_API_BASE` is correct for your provider
- Ensure model name is valid (e.g., `gpt-4o-mini`)
- Monitor token usage if hitting rate limits

### File Parsing Errors

- Ensure uploaded file is actually PDF or DOCX
- Check file isn't corrupted or password-protected
- Verify file contains extractable text (not just images)

### Rate Limiting Issues

- Clear rate limit history by restarting Django server
- Adjust `RATE_LIMIT_REQUESTS` in settings
- Check if using proxy (X-Forwarded-For header)

## 📝 Development Notes

### Adding New File Formats

To support additional formats (e.g., .txt, .rtf):

1. Add extension to `ALLOWED_FILE_EXTENSIONS` in settings
2. Create parser method in `cv_parser.py`
3. Update validation logic in `CVParserService`

### Customizing LLM Prompts

Edit `LLMClientService.SYSTEM_PROMPT` in `llm_client.py` to adjust:
- Analysis criteria
- Output format
- Scoring methodology
- Tone and style

### Extending Authentication

To add other auth providers (GitHub, Microsoft, etc.):
- Enable provider in Firebase Console
- Update frontend sign-in buttons
- Backend verification remains the same (Firebase handles all providers)

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a pull request

## 📧 Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review Firebase and Django official docs

---

**Built with ❤️ using Django, Firebase, and OpenAI**

*Last updated: January 2026*
