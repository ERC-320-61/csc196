"""
firebase_config.py

This module initializes the Firebase Admin SDK and provides a reusable Firestore client (`db`)
for secure and authenticated database operations, such as reading, writing, and querying data.

Usage:
- Import the `db` object to interact with the Firestore database.

Dependencies:
- Firebase Admin SDK (firebase_admin)
"""

import os
import logging
from firebase_admin import firestore, initialize_app, credentials
from logging_config import logger

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK using credentials from an environment variable
    and returns a Firestore client instance.

    Returns:
        firestore.Client: A Firestore client for database operations.

    Raises:
        EnvironmentError: If the FIREBASE_ADMIN_CREDENTIALS environment variable is not set.
    """
    try:
        # Fetch the path to Firebase Admin credentials
        credentials_path = os.getenv("FIREBASE_ADMIN_CREDENTIALS")
        if not credentials_path:
            raise EnvironmentError(
                "Environment variable FIREBASE_ADMIN_CREDENTIALS is not set. "
                "Ensure the path to the Firebase Admin SDK JSON file is properly configured."
            )

        logger.info("Initializing Firebase Admin SDK with credentials at: %s", credentials_path)

        # Load credentials and initialize the Firebase Admin SDK
        cred = credentials.Certificate(credentials_path)
        initialize_app(cred)
        logger.info("Firebase Admin SDK successfully initialized.")

        # Return a Firestore client instance
        return firestore.client()

    except Exception as e:
        logger.error("Failed to initialize Firebase Admin SDK: %s", str(e))
        raise

# Firestore client for global use
try:
    db = initialize_firebase()
    logger.debug("Firestore client is ready for database operations.")
except Exception as init_error:
    logger.critical("Unable to create Firestore client: %s", str(init_error))
    db = None  # Avoid crashing the application, but make db explicit
