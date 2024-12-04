"""
endpoints/auth_router.py

Defines API endpoints for user authentication and sign-up.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from firebase_admin import auth as admin_auth, exceptions as firebase_exceptions
from utils.auth_utils import create_access_token  # Import only what is needed
from logging_config import logger  # Centralized logging
import os
import requests

# Initialize router
router = APIRouter()

# Firebase API Key (required for REST API password authentication)
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# Models for input and response validation
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str


class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Helper Function: Verify Firebase User Password Using REST API
def verify_firebase_user_password(email: str, password: str):
    """
    Verifies the user's email and password using Firebase Authentication REST API.

    Args:
        email (str): User's email.
        password (str): User's password.

    Returns:
        dict: Firebase user details on successful authentication.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()  # Firebase returns user details, including `localId` and `idToken`.
    else:
        logger.error(f"Firebase authentication failed: {response.json()}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response.json().get("error", {}).get("message", "Invalid email or password"),
        )


# Endpoint: Sign up a new user
@router.post("/signup", response_model=dict)
async def sign_up(user_data: SignUpRequest):
    try:
        # Create user in Firebase Authentication
        user = admin_auth.create_user(
            email=user_data.email,
            password=user_data.password,
        )
        logger.info(f"User created successfully in Firebase Authentication: {user.uid}")

        return {"message": "User created successfully", "user_id": user.uid}
    except firebase_exceptions.FirebaseError as e:
        logger.error(f"Error creating user in Firebase Authentication: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user in Firebase Authentication: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user.",
        )


# Endpoint: Sign in a user
@router.post("/signin", response_model=SignInResponse)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Authenticate user using REST API
        firebase_user = verify_firebase_user_password(form_data.username, form_data.password)

        # Validate token using Firebase Admin SDK
        id_token = firebase_user["idToken"]
        decoded_token = admin_auth.verify_id_token(id_token)

        # Generate JWT token for API usage
        access_token = create_access_token(data={"sub": decoded_token["uid"], "email": decoded_token["email"]})

        return SignInResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=30 * 60  # Token expiration in seconds
        )
    except Exception as e:
        logger.error(f"Error in sign-in: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or token validation failed."
        )
