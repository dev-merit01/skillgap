# Registration Troubleshooting Guide

## "Registration failed. Please try again" Error

If users are seeing this error message when trying to register, follow this troubleshooting guide to identify and fix the issue.

## Step 1: Check Browser Console for Detailed Errors

1. **Open the registration page** (`/register/`)
2. **Open browser developer tools:**
   - Chrome/Edge: Press `F12` or `Ctrl+Shift+I`
   - Firefox: Press `F12` or `Ctrl+Shift+I`
3. **Go to the Console tab** (not Network tab)
4. **Try to register with test credentials**
5. **Look for error messages** in the console - they will show the actual Firebase error code

## Step 2: Common Firebase Error Codes and Solutions

### `auth/operation-not-allowed`
**Problem:** Email/password authentication is not enabled in Firebase

**Solution:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (`ai-job-matcher-90698`)
3. Click **Authentication** in the left sidebar
4. Go to **Sign-in method** tab
5. Click on **Email/Password**
6. Make sure the toggle is **ON** (enabled)
7. If it's grayed out, you may need to:
   - Check if the project has Blaze (pay-as-you-go) plan
   - Some Firebase features require the Blaze plan

### `auth/network-request-failed`
**Problem:** Network connectivity issue or CORS problem

**Solution:**
1. Check your internet connection
2. Clear browser cache (`Ctrl+Shift+Delete`)
3. Try in a different browser or incognito mode
4. Check if Firebase domain is accessible:
   - Go to https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js
   - Should load without errors

### `auth/invalid-email`
**Problem:** Email format is invalid

**Solution:**
- Make sure the email follows standard format: `user@domain.com`
- No spaces or special characters allowed

### `auth/weak-password`
**Problem:** Password doesn't meet Firebase requirements

**Solution:**
- Password must be at least 8 characters
- Should contain uppercase, lowercase, numbers, and symbols
- Example: `Test@1234`

### `auth/email-already-in-use`
**Problem:** Email is already registered

**Solution:**
- Try a different email address, or
- Use the **Sign In** page if you have an existing account

## Step 3: Check Firebase Configuration

Run the debug endpoint to check if Firebase is properly configured:

1. **Open this URL:** `http://localhost:8000/debug/`
2. **Look for the following:**
   ```json
   {
     "debug_mode": true,
     "firebase_auth_disabled": false,
     "firebase_credentials_path": false,
     "firebase_project_id": false,
     "firebase_service_account_json": false,
     "openai_api_key": false,
     "allowed_hosts": ["localhost", "127.0.0.1"]
   }
   ```

**Expected values in development:**
- `debug_mode`: should be `true`
- `firebase_auth_disabled`: should be `false`
- Other Firebase fields: can be `false` (not used in development for registration)

## Step 4: Check Firebase Project Settings

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (`ai-job-matcher-90698`)
3. Click **⚙️ Project Settings** (gear icon) → **Project Settings**
4. In the **General** tab, verify:
   - Project ID: `ai-job-matcher-90698`
   - Web API Key: Should be present
5. Go to **Authentication** → **Sign-in method**
6. Verify **Email/Password** is **ENABLED**

## Step 5: Verify Firebase Web Configuration

The registration page uses this Firebase configuration:
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

**Verify these values match your Firebase project:**
1. In Firebase Console → **Project Settings** → **Your apps** section
2. Click the **web icon** to see the config
3. If values don't match, update them in:
   - `analyzer/templates/analyzer/register.html`
   - `analyzer/templates/analyzer/login.html`
   - `analyzer/templates/analyzer/forgot_password.html`

## Step 6: Browser Console Debugging

When registration fails, the console will show detailed error information:
```javascript
Registration error: {
    code: "auth/operation-not-allowed",
    message: "Email/password accounts are not enabled..."
}
```

**Common patterns to look for in the console:**
- `Firebase initialization error:` - Firebase SDK didn't load
- `Firebase auth not initialized` - Auth object is null
- `auth/operation-not-allowed` - Email/password not enabled in Firebase
- `auth/network-request-failed` - Network or CORS issue

## Step 7: Enable Better Error Messages

The registration form now includes enhanced logging. Check the console for:
- "Attempting to create user:" - shows email being registered
- "User created successfully:" - shows Firebase UID
- "Verification email sent to:" - shows registration succeeded

## Advanced Troubleshooting

### Check if Firebase SDK is loading
1. Open browser console
2. Type: `typeof firebase` - should return `"object"`
3. Type: `firebase.auth` - should show the auth module
4. Type: `firebase.apps` - should show the initialized app

### Test Firebase directly in console
```javascript
// Test creating a user
firebase.auth().createUserWithEmailAndPassword('test@example.com', 'Test@1234')
  .then(result => console.log('Success:', result))
  .catch(error => console.log('Error:', error.code, error.message))
```

### Check for CORS issues
1. Open Network tab in DevTools
2. Look for requests to `gstatic.com` or `firebaseapp.com`
3. Check if any are **blocked** or show CORS errors
4. If blocked, the domain may be restricted

## Contact Support

If you've tried all the above steps and registration still doesn't work:
1. Open browser console (F12)
2. Attempt registration again
3. Screenshot the error messages
4. Note the exact Firebase error code (e.g., `auth/operation-not-allowed`)
5. Contact support with this information

## Quick Fixes

**Most common issue:** Email/password authentication not enabled in Firebase

**Quick fix:**
1. Go to https://console.firebase.google.com/
2. Select `ai-job-matcher-90698`
3. Click **Authentication** → **Sign-in method**
4. Click **Email/Password**
5. Toggle **Enable** to **ON**
6. Click **Save**
7. Try registration again

This usually resolves 90% of registration issues!
