"""Firebase Authentication Service.

Verifies Firebase ID tokens and extracts user information.
"""

import base64
import json
import logging

import firebase_admin
from firebase_admin import auth, credentials
from django.conf import settings

logger = logging.getLogger(__name__)


class FirebaseAuthService:
    """
    Service for Firebase authentication and token verification.
    Initializes Firebase Admin SDK and verifies ID tokens.
    """
    
    _initialized = False

    @staticmethod
    def _parse_service_account_json(raw_value: str) -> dict:
        """Parse service account JSON from an env var.

        Supports:
        - Raw JSON object text
        - JSON-string-wrapped JSON (requires 2x json.loads)
        - Base64-encoded JSON

        Also normalizes `private_key` so it contains real newlines.
        """
        if not raw_value or not isinstance(raw_value, str):
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON is empty")

        candidate: str = raw_value.strip()

        # Optional base64 support (handy when dashboards escape characters).
        if not candidate.startswith("{"):
            try:
                decoded = base64.b64decode(candidate, validate=True).decode("utf-8")
                if decoded.lstrip().startswith("{"):
                    candidate = decoded.strip()
            except Exception:
                pass

        parsed = None
        for _ in range(2):
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                break
            if isinstance(parsed, str):
                candidate = parsed.strip()
                continue
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON must decode to a JSON object")

        if not isinstance(parsed, dict):
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON did not decode to an object")

        private_key = parsed.get("private_key")
        if isinstance(private_key, str):
            # Fix the common case where the key is double-escaped and starts with '\\'.
            # PEM parsing expects actual newlines.
            normalized = private_key.replace("\\r\\n", "\n").replace("\\n", "\n")
            # If there are still literal backslashes, replace the escaped newlines again.
            if "\\n" in normalized:
                normalized = normalized.replace("\\n", "\n")
            parsed["private_key"] = normalized

        return parsed
    
    @classmethod
    def initialize(cls):
        """
        Initialize Firebase Admin SDK with service account credentials.
        This should be called once at application startup.
        """
        if cls._initialized:
            return
        
        try:
            if getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_JSON', None):
                service_account = cls._parse_service_account_json(settings.FIREBASE_SERVICE_ACCOUNT_JSON)
                cred = credentials.Certificate(service_account)
                firebase_admin.initialize_app(cred)
            elif settings.FIREBASE_CREDENTIALS_PATH:
                # Initialize with service account file
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
            elif settings.FIREBASE_PROJECT_ID:
                # Initialize with default credentials (useful for Cloud Run/GCP)
                firebase_admin.initialize_app(options={
                    'projectId': settings.FIREBASE_PROJECT_ID
                })
            else:
                raise ValueError(
                    "Firebase configuration missing. Set FIREBASE_SERVICE_ACCOUNT_JSON, "
                    "FIREBASE_CREDENTIALS_PATH, or FIREBASE_PROJECT_ID in environment variables."
                )
            
            cls._initialized = True
            logger.info("Firebase Admin SDK initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
            raise
    
    @classmethod
    def verify_token(cls, id_token: str) -> dict:
        """
        Verify a Firebase ID token and extract user information.
        
        Args:
            id_token: The Firebase ID token from the client
            
        Returns:
            dict containing:
                - uid: User's Firebase UID
                - email: User's email address
                - name: User's display name (if available)
                
        Raises:
            ValueError: If token is invalid, expired, or verification fails
        """
        if not cls._initialized:
            cls.initialize()
        
        if not id_token or not isinstance(id_token, str):
            raise ValueError("Invalid token format")
        
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            
            # Extract user information
            user_info = {
                'uid': decoded_token.get('uid'),
                'email': decoded_token.get('email'),
                'name': decoded_token.get('name', decoded_token.get('email', 'User')),
                'email_verified': decoded_token.get('email_verified', False),
            }
            
            if not user_info['uid']:
                raise ValueError("Token missing user ID")
            
            logger.info(f"Successfully verified token for user: {user_info['uid']}")
            return user_info
            
        except auth.InvalidIdTokenError:
            logger.warning("Invalid ID token provided")
            raise ValueError("Invalid authentication token")
        except auth.ExpiredIdTokenError:
            logger.warning("Expired ID token provided")
            raise ValueError("Authentication token has expired")
        except auth.RevokedIdTokenError:
            logger.warning("Revoked ID token provided")
            raise ValueError("Authentication token has been revoked")
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            raise ValueError(f"Authentication failed: {str(e)}")


# Initialize Firebase on module import
try:
    FirebaseAuthService.initialize()
except Exception as e:
    logger.warning(f"Firebase initialization deferred: {e}")
