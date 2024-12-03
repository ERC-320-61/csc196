"""
endpoints/__init__.py

Initializes the `endpoints` package and sets up logging for the module.
Also imports and exposes all routers for use in the FastAPI application.
"""

from logging_config import logger  # Use the centralized logger for consistency

# Log initialization message
logger.info("Initializing the `endpoints` package")

# Import routers from individual endpoint modules
from .auth_router import router as auth_router
from .admin import router as admin_router
from .client import router as client_router
from .common import router as common_router
from .consultant import router as consultant_router

# Expose routers for use in the main application
__all__ = [
    "auth_router",
    "admin_router",
    "client_router",
    "common_router",
    "consultant_router",
]
