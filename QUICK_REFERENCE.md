# 🚀 Quick Start - Firebase Setup

**First time?** Follow this guide to get Firebase running in 10 minutes.

## 📁 Important Files You'll Work With

1. **`.env`** - Your local configuration (already created!)
2. **`firebase-credentials.json`** - Download from Firebase Console (you'll create this)
3. **`analyzer/templates/analyzer/home.html`** - Line 158: Add your web config

## 🔥 5-Step Setup

### 1️⃣ Create Firebase Project (3 min)
```
→ https://console.firebase.google.com/
→ Click "Create a project"
→ Name it (e.g., "my-job-matcher")
→ Finish creation
```

### 2️⃣ Enable Google Sign-In (1 min)
```
→ Click "Authentication" in sidebar
→ Click "Get started"
→ Enable "Google" provider
→ Add your email as support email
→ Save
```

### 3️⃣ Get Credentials (2 min)

**Backend (Service Account):**
```
→ Click ⚙️ icon → "Project settings"
→ "Service accounts" tab
→ "Generate new private key"
→ Download → Rename to firebase-credentials.json
→ Move to project root folder
```

**Frontend (Web Config):**
```
→ Still in "Project settings"
→ Scroll to "Your apps"
→ Click web icon </> → Register app
→ Copy the firebaseConfig object
→ Save for next step
```

### 4️⃣ Update Configuration Files (2 min)

**Backend - .env file:**
```env
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
OPENAI_API_KEY=sk-your-key-here
```

**Frontend - home.html (line 158):**
Replace the placeholder config with YOUR firebaseConfig:
```javascript
const firebaseConfig = {
    apiKey: "YOUR-API-KEY",
    authDomain: "YOUR-PROJECT.firebaseapp.com",
    projectId: "YOUR-PROJECT-ID",
    // ... rest of your config
};
```

### 5️⃣ Validate & Run (2 min)

**Validate setup:**
```bash
# Windows
validate_firebase.bat

# Mac/Linux
./validate_firebase.sh

# Or directly
python scripts/validate_firebase.py
```

**Start app:**
```bash
python manage.py runserver
```

**Test:**
```
→ Open http://localhost:8000/app/
→ Click "Sign in with Google"
→ Upload CV + paste job description
→ Analyze!
```

## ✅ Verification Checklist

Run the validator - you should see:
- ✅ FIREBASE_CREDENTIALS_PATH is set
- ✅ Credentials file exists
- ✅ JSON format is valid
- ✅ Firebase Admin SDK initialized
- ✅ OpenAI API key configured

If all ✅ → You're ready! 🎉

If any ❌ → See troubleshooting below

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Credentials not found" | Put `firebase-credentials.json` in project root (same folder as `manage.py`) |
| "Sign in popup blocked" | Allow popups in browser, or check if you updated `home.html` with YOUR config |
| "Module not found" | Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux) |
| "Invalid credentials" | Re-download service account JSON from Firebase Console |
| "OpenAI error" | Get API key from https://platform.openai.com/api-keys and add to `.env` |

## 📚 Need More Help?

- **Detailed guide**: [FIREBASE_SETUP.md](FIREBASE_SETUP.md)
- **Step-by-step checklist**: [FIREBASE_CHECKLIST.md](FIREBASE_CHECKLIST.md)
- **Full documentation**: [README.md](README.md)
- **What changed**: [SETUP_COMPLETE.md](SETUP_COMPLETE.md)

## 🎯 What's Already Done

✅ Backend Firebase authentication service
✅ Frontend Google sign-in integration
✅ Security middleware and rate limiting
✅ Environment configuration template
✅ Validation scripts
✅ Complete documentation

**You just need to:**
1. Create your Firebase project
2. Download credentials
3. Update config files
4. Run validator
5. Start coding!

---

**Time required**: 10-15 minutes | **Difficulty**: Beginner-friendly

Let's go! 🚀
