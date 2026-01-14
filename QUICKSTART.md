# AI Job Matcher - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in:

```env
DJANGO_SECRET_KEY=your-secret-key
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
OPENAI_API_KEY=sk-your-key-here
DEBUG=True
```

### 3. Setup Firebase

**Detailed guide**: See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for complete instructions.

**Quick version**:
1. Create Firebase project: https://console.firebase.google.com/
2. Enable Google Authentication in Authentication section
3. Download service account JSON → save as `firebase-credentials.json` in project root
4. Get Web API config and update `analyzer/templates/analyzer/home.html` (line 158)
5. Verify setup: `python scripts/validate_firebase.py`

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

Open http://localhost:8000

## ✅ Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`requirements.txt`)
- [ ] `.env` file configured with all keys
- [ ] Firebase project created with Google Auth enabled
- [ ] Firebase credentials downloaded and saved as `firebase-credentials.json`
- [ ] Firebase web config updated in `home.html`
- [ ] Firebase setup validated: `python scripts/validate_firebase.py`
- [ ] Database migrated
- [ ] Server running successfully

## 🆘 Common Issues

**"Firebase not configured"**
- Check `FIREBASE_CREDENTIALS_PATH` in `.env`
- Verify JSON file exists and is valid
- Run `python scripts/validate_firebase.py` for diagnostics

**"OpenAI API Error"**
- Confirm `OPENAI_API_KEY` is correct
- Verify you have API credits

**"Module not found"**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**"Sign in failed"**
- Updat[FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed Firebase configuration
- Read full [README.md](README.md) for detailed documentation
- Customize LLM prompts in `analyzer/services/llm_client.py`
- Adjust rate limits in `.env`
- Deploy to production (Gunicorn + Nginx recommended)

---

**Need help?** Check FIREBASE_SETUP.md, README.md,er/services/llm_client.py`
- Adjust rate limits in `.env`
- Deploy to production (Gunicorn + Nginx recommended)

---

**Need help?** Check the README.md or open an issue.
