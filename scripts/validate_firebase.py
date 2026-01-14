#!/usr/bin/env python3
"""
Firebase Configuration Validator
Checks if Firebase is properly configured for the AI Job Matcher application.
"""
import os
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_matcher.settings')
import django
django.setup()

from django.conf import settings
from analyzer.services.firebase_auth import FirebaseAuthService


def print_header(text):
    """Print a formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print('=' * 60)


def print_check(text, status, details=""):
    """Print a check result"""
    icon = "✅" if status else "❌"
    print(f"{icon} {text}")
    if details:
        print(f"   {details}")


def validate_firebase_setup():
    """Validate Firebase configuration and setup"""
    
    print_header("Firebase Configuration Validator")
    print("Checking Firebase setup for AI Job Matcher...\n")
    
    all_checks_passed = True
    
    # Check 1: Environment variables
    print_header("1. Environment Variables")
    
    firebase_creds_path = settings.FIREBASE_CREDENTIALS_PATH
    firebase_project_id = settings.FIREBASE_PROJECT_ID
    
    if firebase_creds_path:
        print_check("FIREBASE_CREDENTIALS_PATH is set", True, f"Path: {firebase_creds_path}")
    elif firebase_project_id:
        print_check("FIREBASE_PROJECT_ID is set", True, f"Project ID: {firebase_project_id}")
    else:
        print_check("Firebase configuration", False, "Neither FIREBASE_CREDENTIALS_PATH nor FIREBASE_PROJECT_ID is set")
        all_checks_passed = False
        print("\n⚠️  Please configure Firebase in your .env file:")
        print("   FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json")
        print("   OR")
        print("   FIREBASE_PROJECT_ID=your-project-id")
        return False
    
    # Check 2: Credentials file exists (if using file path)
    if firebase_creds_path:
        print_header("2. Credentials File")
        
        creds_file = Path(firebase_creds_path)
        
        if creds_file.is_absolute():
            file_path = creds_file
        else:
            file_path = project_root / firebase_creds_path
        
        if file_path.exists():
            print_check("Credentials file exists", True, f"Location: {file_path}")
        else:
            print_check("Credentials file exists", False, f"File not found at: {file_path}")
            all_checks_passed = False
            print("\n⚠️  Download your Firebase service account key:")
            print("   1. Go to Firebase Console > Project Settings > Service Accounts")
            print("   2. Click 'Generate new private key'")
            print("   3. Save as 'firebase-credentials.json' in project root")
            return False
        
        # Check 3: Validate JSON format
        print_header("3. Credentials File Validation")
        
        try:
            with open(file_path, 'r') as f:
                creds_data = json.load(f)
            
            print_check("JSON format is valid", True)
            
            # Check required fields
            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
            missing_fields = [field for field in required_fields if field not in creds_data]
            
            if not missing_fields:
                print_check("All required fields present", True)
                print_check("Service account type", True, f"Type: {creds_data.get('type')}")
                print_check("Project ID", True, f"ID: {creds_data.get('project_id')}")
                print_check("Client email", True, f"Email: {creds_data.get('client_email')}")
            else:
                print_check("Required fields check", False, f"Missing: {', '.join(missing_fields)}")
                all_checks_passed = False
                
        except json.JSONDecodeError as e:
            print_check("JSON format is valid", False, f"Invalid JSON: {e}")
            all_checks_passed = False
            return False
        except Exception as e:
            print_check("File reading", False, f"Error: {e}")
            all_checks_passed = False
            return False
    
    # Check 4: Initialize Firebase Admin SDK
    print_header("4. Firebase Admin SDK Initialization")
    
    try:
        FirebaseAuthService.initialize()
        print_check("Firebase Admin SDK initialized", True, "Connection successful!")
    except Exception as e:
        print_check("Firebase Admin SDK initialization", False, f"Error: {e}")
        all_checks_passed = False
        print("\n⚠️  Possible issues:")
        print("   - Invalid credentials file")
        print("   - Network connectivity issues")
        print("   - Firebase project does not exist")
        return False
    
    # Check 5: Additional recommendations
    print_header("5. Additional Checks")
    
    # Check OpenAI API key
    openai_key = settings.OPENAI_API_KEY
    if openai_key and openai_key != 'your-openai-api-key-here':
        print_check("OpenAI API key configured", True, "LLM analysis will work")
    else:
        print_check("OpenAI API key configured", False, "Analysis will fail without API key")
        print("   Add to .env: OPENAI_API_KEY=sk-your-key-here")
    
    # Check if running in debug mode
    if settings.DEBUG:
        print_check("Debug mode", True, "Running in development mode")
    else:
        print_check("Debug mode", False, "Running in production mode")
    
    # Summary
    print_header("Summary")
    
    if all_checks_passed:
        print("\n🎉 Firebase setup is complete!")
        print("\nYou can now:")
        print("  1. Start the server: python manage.py runserver")
        print("  2. Visit: http://localhost:8000/app/")
        print("  3. Sign in with Google")
        print("  4. Upload a CV and analyze!")
        
        print("\n⚠️  Remember to:")
        print("  - Update Firebase web config in analyzer/templates/analyzer/home.html")
        print("  - Add your OpenAI API key to .env if not already done")
        print("  - Never commit firebase-credentials.json or .env to git")
        
        return True
    else:
        print("\n❌ Firebase setup incomplete")
        print("\nPlease fix the issues above and run this script again.")
        print("\nFor detailed setup instructions, see: FIREBASE_SETUP.md")
        return False


if __name__ == '__main__':
    try:
        success = validate_firebase_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Validation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
