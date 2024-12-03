"""
__init__.py

Initializes the `models` package and provides direct access to model classes.
"""

from .appointments import Appointment
from .users import User
from logging_config import logger

# Log the initialization of the models package
logger.debug("Initializing models package with Appointment and User models.")

# Expose model classes for easy imports
__all__ = ["Appointment", "User"]
