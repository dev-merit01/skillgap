"""
Firebase Authentication Service
Verifies Firebase ID tokens and extracts user information.
"""
import json
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class FirebaseAuthService:
    """
    Service for Firebase authentication and token verification.
    Initializes Firebase Admin SDK and verifies ID tokens.
    """
    
    _initialized = False
    
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
                service_account = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_JSON)
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
