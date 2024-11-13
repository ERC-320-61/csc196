from firebase_utils import verify_firebase_token  # Import the Firebase token verification function
from typing import List
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
import jwt  # Assuming JWTs are being used
import os

# Retrieve secret and algorithm from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Adjust if needed

# Define function to get the current user and validate token and scopes
async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """
    Validates the JWT token or Firebase ID token and checks if it contains the required scopes.

    :param security_scopes: Required scopes for the endpoint
    :param token: JWT token or Firebase ID token passed in request header
    :return: User data if authentication and authorization are successful
    :raises HTTPException: If token is invalid or scopes are missing
    """
    # Check if the token is a Firebase ID token
    try:
        decoded_token = verify_firebase_token(token)
        # Firebase tokens typically do not have "scopes"
        username = decoded_token.get("uid")  # Use Firebase UID as the username
        token_scopes = []  # Firebase tokens typically do not have scopes
    except Exception as e:
        # If not a Firebase token, treat it as a regular JWT token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")  # Retrieve the username from the token payload
            token_scopes: List[str] = payload.get("scopes", [])  # Retrieve scopes from the token payload
        except jwt.PyJWTError as e:
            # Raise exception if token is invalid
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Check if all required scopes are present in the token's scopes (if any)
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
            )

    # Return a simulated user object with username and scopes for simplicity
    return {"username": username, "scopes": token_scopes}
