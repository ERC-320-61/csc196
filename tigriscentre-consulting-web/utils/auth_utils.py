"""
utils/auth_utils.py

Handles authentication utilities like token creation and validation.
"""

import os
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import HTTPException, status
from logging_config import logger  # Centralized logging

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT token with the provided data.

    Args:
        data (dict): Data to encode in the token.
        expires_delta (timedelta, optional): Token expiration time.

    Returns:
        str: Encoded JWT token.
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})  # Add expiration claim
        logger.debug(f"Creating token for payload: {to_encode}")
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.error(f"Error creating JWT token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating authentication token."
        )


def get_current_user(token: str) -> dict:
    """
    Validate the provided JWT token and return user information.

    Args:
        token (str): JWT token.

    Returns:
        dict: Decoded user information.

    Raises:
        HTTPException: If token validation fails.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        email = payload.get("email")
        exp = payload.get("exp")

        if user_id is None or email is None:
            logger.warning("Token payload missing 'sub' or 'email'")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        # Check token expiration
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            logger.warning("Token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

        logger.info(f"Authenticated user: {user_id}")
        return {"username": user_id, "email": email}
    except JWTError as e:
        logger.error(f"JWT validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
