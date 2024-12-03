"""
admin.py

Endpoints for administrative tasks, such as managing users and viewing appointments.
Only accessible to users with the "admin:manage" scope.

Dependencies:
- FastAPI for building APIs
- Pydantic for request/response validation
- Firebase Firestore for database operations
"""

from fastapi import APIRouter, Security, HTTPException, status
from firebase_admin import firestore
from utils.auth_utils import get_current_user  # Use centralized function
from pydantic import BaseModel, Field
from logging_config import logger  # Import centralized logger

# Initialize Firestore client
db = firestore.client()

# Create a router for admin-specific endpoints
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Security(get_current_user, scopes=["admin:manage"])],
)

# Pydantic model for user creation/update
class UserModel(BaseModel):
    email: str = Field(..., description="Email of the user")
    name: str = Field(..., description="Name of the user")
    role: str = Field(..., pattern="^(admin|consultant|client)$", description="Role of the user")  # Changed regex to pattern
    bio: str = Field(None, description="Bio of the user")
    profile_image: str = Field(None, description="URL of the profile image")



# Endpoint to view all appointments
@router.get("/appointments")
async def view_all_appointments():
    """
    Fetch all appointments from Firestore.

    Returns:
        dict: List of all appointments.
    """
    try:
        logger.info("Fetching all appointments from Firestore.")
        appointments_ref = db.collection("appointments")
        appointments = [doc.to_dict() for doc in appointments_ref.stream()]
        return {"appointments": appointments}
    except Exception as e:
        logger.error(f"Failed to retrieve appointments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve appointments: {str(e)}"
        )


# Endpoint to create or update a user
@router.post("/users")
async def create_or_update_user(user: UserModel):
    """
    Create or update a user in the Firestore database.

    Args:
        user (UserModel): The user data to create or update.

    Returns:
        dict: Confirmation of user creation/update.
    """
    try:
        logger.info(f"Creating/updating user: {user.email}")
        user_ref = db.collection("users").document(user.email)
        user_ref.set(user.dict())
        return {"message": f"User {user.email} has been created/updated successfully."}
    except Exception as e:
        logger.error(f"Failed to create/update user {user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create/update user: {str(e)}"
        )


# Endpoint to delete a user
@router.delete("/users/{email}")
async def delete_user(email: str):
    """
    Delete a user from Firestore.

    Args:
        email (str): The email of the user to delete.

    Returns:
        dict: Confirmation of user deletion.
    """
    try:
        logger.info(f"Attempting to delete user: {email}")
        user_ref = db.collection("users").document(email)
        if not user_ref.get().exists:
            logger.warning(f"User with email {email} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {email} not found."
            )
        user_ref.delete()
        logger.info(f"User {email} deleted successfully.")
        return {"message": f"User {email} has been deleted successfully."}
    except Exception as e:
        logger.error(f"Failed to delete user {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )


# Endpoint to view all users
@router.get("/users")
async def view_all_users():
    """
    Fetch all users from Firestore.

    Returns:
        dict: List of all users.
    """
    try:
        logger.info("Fetching all users from Firestore.")
        users_ref = db.collection("users")
        users = [doc.to_dict() for doc in users_ref.stream()]
        return {"users": users}
    except Exception as e:
        logger.error(f"Failed to retrieve users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )
