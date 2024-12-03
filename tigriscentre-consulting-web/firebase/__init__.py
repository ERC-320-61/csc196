"""
__init__.py

Initializes the `firebase` package and exposes the `db` Firestore client
for application-wide use.

Usage:
    from firebase import db
"""

from .firebase_config import db

# Define the public API for this module
__all__ = ["db"]
