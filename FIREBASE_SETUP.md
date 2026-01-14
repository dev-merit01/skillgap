# 🔥 Firebase Setup Guide for AI Job Matcher

This guide will walk you through setting up Firebase Authentication for the AI Job Matcher application.

## Prerequisites

- Google account
- Basic understanding of Firebase Console

## Step-by-Step Setup

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter project name: `ai-job-matcher` (or your preferred name)
4. (Optional) Enable Google Analytics - you can disable this for simplicity
5. Click **"Create project"** and wait for it to be ready
6. Click **"Continue"** once the project is created

### 2. Enable Google Authentication

1. In the Firebase Console, click on **"Authentication"** in the left sidebar
2. Click **"Get started"** button
3. Go to the **"Sign-in method"** tab
4. Click on **"Google"** provider
5. Toggle the **"Enable"** switch to ON
6. Enter a support email (your email address)
7. Click **"Save"**

### 3. Add Your Domain to Authorized Domains

1. Stay in the **"Authentication"** section
2. Go to the **"Settings"** tab (top right)
3. Scroll to **"Authorized domains"**
4. By default, `localhost` should already be there
5. For production, click **"Add domain"** and add your deployment domain

### 4. Get Firebase Web Configuration

1. Click the **gear icon** ⚙️ next to "Project Overview" at the top left
2. Select **"Project settings"**
3. Scroll down to **"Your apps"** section
4. Click the **web icon** `</>` to add a web app
5. Give it a nickname: `AI Job Matcher Web`
6. (Optional) Enable Firebase Hosting - not required for this project
7. Click **"Register app"**
8. Copy the `firebaseConfig` object - you'll need this later
9. Click **"Continue to console"**

Your config will look like this:
```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.firebasestorage.app",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123",
  measurementId: "G-ABC123XYZ"
};
```

**IMPORTANT**: Save this config - you'll add it to your HTML template in Step 6.

### 5. Download Service Account Credentials (Backend)

1. Still in **"Project settings"**, click the **"Service accounts"** tab
2. Click **"Generate new private key"** button
3. Click **"Generate key"** in the confirmation dialog
4. A JSON file will download - **this contains sensitive credentials!**
5. Rename the file to `firebase-credentials.json`
6. Move it to your project root directory (same folder as `manage.py`)
7. **NEVER commit this file to git** (it's already in `.gitignore`)

### 6. Update Frontend Configuration

1. Open `analyzer/templates/analyzer/home.html`
2. Find the Firebase configuration section (around **line 170**)
3. Replace the `firebaseConfig` object with YOUR config from Step 4

**Current placeholder config (line 170-178):**
```javascript
const firebaseConfig = {
    apiKey: "AIzaSyCR0--hTXPwbw29CNjC-JkBBXrUsdCGqb4",
    authDomain: "ai-job-matcher-90698.firebaseapp.com",
    projectId: "ai-job-matcher-90698",
    storageBucket: "ai-job-matcher-90698.firebasestorage.app",
    messagingSenderId: "677178545276",
    appId: "1:677178545276:web:668d3a4f6803ffc633e5f9",
    measurementId: "G-PY7TS2P96L"
};
```

**Replace with YOUR config** (from Step 4).

### 7. Update Environment Variables

1. Open the `.env` file in the project root
2. Update the Firebase configuration:

```env
# Make sure this points to your downloaded JSON file
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

3. Also add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

### 8. Verify File Structure

Your project should now have:
```
resume-job-match/
├── firebase-credentials.json     ← Your service account file (DO NOT COMMIT)
├── .env                          ← Updated with paths and keys
├── .env.example                  ← Template (safe to commit)
├── manage.py
└── ...
```

### 9. Test Firebase Setup

Run the validation script:
```bash
python scripts/validate_firebase.py
```

This will check:
- ✅ Firebase credentials file exists
- ✅ JSON is valid
- ✅ Firebase Admin SDK can initialize
- ✅ Project ID matches

### 10. Start the Application

```bash
# Make sure virtual environment is activated
python manage.py runserver
```

Visit `http://localhost:8000` and test:
1. Click "Start Free" or go to `/app/`
2. Click "Sign in with Google"
3. Select your Google account
4. You should see "Signed in as [Your Name]"
5. The analysis form should appear

## Security Checklist

Before deploying to production:

- [ ] `firebase-credentials.json` is in `.gitignore` (already done)
- [ ] `.env` is in `.gitignore` (already done)
- [ ] Never commit actual API keys to git
- [ ] Use environment variables in production (Cloud Run, Heroku, etc.)
- [ ] Set `DEBUG=False` in production
- [ ] Enable SSL/HTTPS for production domains
- [ ] Add production domain to Firebase authorized domains
- [ ] Restrict Firebase Web API key by HTTP referrers in console
- [ ] Set up rate limiting in production environment

## Troubleshooting

### "Firebase credentials not found"
- Check that `firebase-credentials.json` exists in the project root
- Verify `FIREBASE_CREDENTIALS_PATH` in `.env` points to the correct location
- Use relative path `./firebase-credentials.json` or absolute path

### "Invalid credentials" or "Permission denied"
- Re-download the service account JSON from Firebase Console
- Make sure you downloaded the **Admin SDK** credentials, not web config
- Check file has correct JSON format (should start with `{ "type": "service_account", ...`)

### "Auth domain not authorized"
- Add your domain to Firebase Console > Authentication > Settings > Authorized domains
- For localhost development, `localhost` should already be there

### "Sign in popup blocked"
- Allow popups in your browser for localhost
- Check browser console for detailed error messages

### Firebase initialized but sign-in fails
- Verify you replaced the firebaseConfig in `home.html` with YOUR config
- Check Firebase Console > Authentication is enabled
- Check Google sign-in provider is enabled

## Additional Resources

- [Firebase Authentication Docs](https://firebase.google.com/docs/auth)
- [Firebase Admin SDK Setup](https://firebase.google.com/docs/admin/setup)
- [Google Sign-In](https://firebase.google.com/docs/auth/web/google-signin)

## Need Help?

If you encounter issues:
1. Check the Django console for error messages
2. Check browser console (F12) for frontend errors
3. Run `python scripts/validate_firebase.py` for diagnostics
4. Verify all steps above were completed

---

**Next Steps**: Once Firebase is working, configure your OpenAI API key in `.env` to enable CV analysis.
