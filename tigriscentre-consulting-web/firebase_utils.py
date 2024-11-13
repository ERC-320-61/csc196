import os
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.exceptions import InvalidIdTokenError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize the Firebase Admin SDK with environment variable
def initialize_firebase():
    if not firebase_admin._apps:  # Check if Firebase is already initialized
        firebase_cred_path = os.getenv("FIREBASE_ADMIN_CREDENTIALS")
        if not firebase_cred_path:
            raise ValueError("FIREBASE_ADMIN_CREDENTIALS environment variable not set.")

        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized.")


# Call the initializer
initialize_firebase()


def verify_firebase_token(id_token: str):
    """
    Verify the Firebase ID token.

    :param id_token: Firebase ID token from the client
    :return: Decoded token payload if valid
    :raises: InvalidIdTokenError if token is invalid
    """
    try:
        # Verify the ID token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        logger.info("Firebase token verified successfully.")
        return decoded_token
    except InvalidIdTokenError as e:
        logger.error(f"Invalid Firebase token: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error verifying Firebase token: {e}")
        raise
