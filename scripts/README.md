# Scripts

Helper scripts for AI Job Matcher configuration and validation.

## Available Scripts

### `validate_firebase.py`

Validates your Firebase configuration and setup.

**Usage:**
```bash
python scripts/validate_firebase.py
```

**What it checks:**
- ✅ Environment variables are set
- ✅ Firebase credentials file exists and is valid
- ✅ JSON format and required fields
- ✅ Firebase Admin SDK can initialize
- ✅ OpenAI API key is configured

**Exit codes:**
- `0` - All checks passed, Firebase is ready
- `1` - Some checks failed, see output for details

Run this script after following the [Firebase Setup Guide](../FIREBASE_SETUP.md) to ensure everything is configured correctly.
