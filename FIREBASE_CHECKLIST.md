# Firebase Setup Checklist

Use this checklist to ensure your Firebase setup is complete.

## ☐ Step 1: Create Firebase Project

- [ ] Go to https://console.firebase.google.com/
- [ ] Click "Add project" or "Create a project"
- [ ] Name your project (e.g., "ai-job-matcher")
- [ ] Complete project creation

## ☐ Step 2: Enable Authentication

- [ ] Open "Authentication" in Firebase Console sidebar
- [ ] Click "Get started"
- [ ] Go to "Sign-in method" tab
- [ ] Enable "Google" provider
- [ ] Add support email
- [ ] Save

## ☐ Step 3: Add Web App

- [ ] Click gear icon ⚙️ > "Project settings"
- [ ] Scroll to "Your apps"
- [ ] Click web icon `</>`
- [ ] Register app with a nickname
- [ ] Copy the `firebaseConfig` object
- [ ] Save the config for later

## ☐ Step 4: Download Service Account Credentials

- [ ] Still in "Project settings", click "Service accounts" tab
- [ ] Click "Generate new private key"
- [ ] Confirm and download JSON file
- [ ] Rename file to `firebase-credentials.json`
- [ ] Move to project root directory (same folder as `manage.py`)

## ☐ Step 5: Update Backend Configuration

- [ ] Open `.env` file in project root
- [ ] Confirm `FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json`
- [ ] Add your OpenAI API key: `OPENAI_API_KEY=sk-...`
- [ ] Save `.env` file

## ☐ Step 6: Update Frontend Configuration

- [ ] Open `analyzer/templates/analyzer/home.html`
- [ ] Find the Firebase config section (around line 158)
- [ ] Replace the placeholder config with YOUR `firebaseConfig` from Step 3
- [ ] Save the file

## ☐ Step 7: Validate Setup

Run the validation script:
```bash
python scripts/validate_firebase.py
```

Expected output:
- [ ] ✅ FIREBASE_CREDENTIALS_PATH is set
- [ ] ✅ Credentials file exists
- [ ] ✅ JSON format is valid
- [ ] ✅ All required fields present
- [ ] ✅ Firebase Admin SDK initialized
- [ ] ✅ OpenAI API key configured

## ☐ Step 8: Test the Application

```bash
# Start the server
python manage.py runserver
```

In your browser:
- [ ] Visit http://localhost:8000
- [ ] Click "Start Free" or go to `/app/`
- [ ] Click "Sign in with Google"
- [ ] Authorize with your Google account
- [ ] Verify you see "Signed in as [Your Name]"
- [ ] Upload a test CV (PDF or DOCX)
- [ ] Paste a sample job description
- [ ] Click "Analyze Match"
- [ ] Receive analysis results with match score

## 🎉 If All Steps Pass

Your Firebase setup is complete! You can now:
- Use the application for CV analysis
- Share with others (update authorized domains in Firebase)
- Deploy to production

## ❌ If Something Fails

Check the detailed guide:
- See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for step-by-step instructions
- Review error messages from `validate_firebase.py`
- Check Django console for backend errors
- Check browser console (F12) for frontend errors

## 🔒 Security Reminders

- [ ] `firebase-credentials.json` is NOT committed to git (in `.gitignore`)
- [ ] `.env` file is NOT committed to git (in `.gitignore`)
- [ ] Never share your service account credentials publicly
- [ ] Keep your OpenAI API key secret
- [ ] For production: Set `DEBUG=False` in `.env`
- [ ] For production: Add your domain to Firebase authorized domains

---

**Need Help?** See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed instructions.
