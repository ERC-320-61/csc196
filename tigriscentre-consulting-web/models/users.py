"""
users.py

Defines the Pydantic model for the `users` collection in Firestore.
This model is used for data validation and type checking when handling user-related data.
"""

from pydantic import BaseModel, EmailStr, Field, ValidationError
from typing import Literal, Optional
from logging_config import logger


class User(BaseModel):
    """Pydantic model for user data validation."""

    user_id: Optional[str] = Field(None, description="Unique ID for the user.")
    name: str = Field(..., description="Full name of the user.")
    email: EmailStr = Field(..., description="Email address of the user.")
    profile_image: Optional[str] = Field(None, description="URL to the user's profile image.")
    bio: Optional[str] = Field("", description="Short biography of the user.")
    role: Literal["admin", "consultant", "client"] = Field(..., description="Role assigned to the user.")

    def __init__(self, **data):
        """Initialize and validate user data."""
        try:
            super().__init__(**data)
            logger.info(f"User data validated successfully for email: {data.get('email')}")
        except ValidationError as e:
            logger.error(f"Validation error while creating user: {e}")
            raise e

    def to_dict(self) -> dict:
        """
        Convert the user instance to a dictionary, omitting None values.

        Returns:
            dict: Dictionary representation of the user instance.
        """
        user_dict = {key: value for key, value in self.dict().items() if value is not None}
        logger.debug(f"Converted user object to dictionary: {user_dict}")
        return user_dict


# Example utility functions for user-related operations
def validate_user_email(email: str):
    """Validate a user email address."""
    try:
        valid_email = EmailStr.validate(email)
        logger.info(f"Validated email address: {email}")
        return valid_email
    except ValidationError as e:
        logger.error(f"Invalid email address: {email}. Error: {e}")
        raise e


# Example usage (can be removed or commented in production)
if __name__ == "__main__":
    try:
        # Creating a user instance for testing
        user = User(
            user_id="12345",
            name="John Doe",
            email="john.doe@example.com",
            role="consultant",
        )
        print(user.to_dict())
    except ValidationError as e:
        logger.error(f"User creation failed: {e}")
