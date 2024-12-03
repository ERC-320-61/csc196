"""
endpoints/auth_router.py

Defines API endpoints for user authentication and sign-up.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from firebase_admin import auth, exceptions as firebase_exceptions
from utils.auth_utils import create_access_token  # Import only what is needed
from logging_config import logger  # Centralized logging

# Initialize router
router = APIRouter()

# Models for input and response validation
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    profile_image: str = None  # Optional field for profile image


class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Endpoint: Sign up a new user
@router.post("/auth/signup", response_model=dict)
async def sign_up(user_data: SignUpRequest):
    try:
        user = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.name,
            photo_url=user_data.profile_image,
        )
        logger.info(f"User created successfully: {user.uid}")
        return {"message": "User created successfully", "user_id": user.uid}
    except firebase_exceptions.FirebaseError as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}",
        )


# Endpoint: Sign in a user
@router.post("/auth/signin", response_model=SignInResponse)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Fetch user by email
        user = auth.get_user_by_email(form_data.username)

        # Verify password (Placeholder logic)
        if form_data.password != "firebase_password_placeholder":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # Create JWT token
        access_token = create_access_token(data={"sub": user.uid, "email": user.email})
        logger.info(f"User signed in successfully: {user.uid}")
        return SignInResponse(
            access_token=access_token,
            expires_in=30,  # Default expiration in minutes
        )
    except firebase_exceptions.FirebaseError as e:
        logger.error(f"Authentication failed for user {form_data.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
