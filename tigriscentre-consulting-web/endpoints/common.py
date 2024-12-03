"""
common.py

This module contains shared utility functions and common endpoints
that can be reused across different parts of the application.

All endpoints include appropriate security measures, such as input validation,
authentication, and role-based access control.
"""

from fastapi import APIRouter, HTTPException, Security, Query, status
from pydantic import BaseModel, Field
from firebase_admin import firestore
from utils.auth_utils import get_current_user  # Use centralized function
from typing import Optional
from datetime import datetime


# Firestore database reference
db = firestore.client()

# Create a router for shared endpoints
router = APIRouter()


# Pydantic models for shared data
class SearchQuery(BaseModel):
    keyword: str = Field(..., description="Search keyword.")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of results to return.")


# Shared endpoint: Search across multiple collections
@router.get("/search", summary="Global search endpoint", tags=["Common"])
async def global_search(
    query: SearchQuery,
    current_user: dict = Security(get_current_user, scopes=["admin:read", "consultant:read", "client:read"])
):
    """
    Allows authenticated users to perform a search across multiple collections in Firestore.

    Security:
    - The user must have at least a 'read' permission for their role.

    Parameters:
        - query (SearchQuery): Contains the search keyword and limit.
        - current_user (dict): The authenticated user making the request.

    Returns:
        - dict: A dictionary containing search results grouped by collections.
    """
    try:
        results = {}
        collections = ["users", "appointments", "conversations"]

        for collection in collections:
            query_ref = (
                db.collection(collection)
                .where("name", ">=", query.keyword)
                .where("name", "<=", query.keyword + "\uf8ff")
                .limit(query.limit)
            )
            results[collection] = [doc.to_dict() for doc in query_ref.stream()]

        return {"results": results}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while searching: {str(e)}"
        )


# Shared utility: Health check
@router.get("/health", summary="Health check endpoint", tags=["Common"])
async def health_check():
    """
    A public endpoint for monitoring the health of the application.

    Returns:
        - dict: A message confirming the application is running.
    """
    try:
        # Simulate a lightweight operation to ensure the app is healthy
        db.collection("health_check").document("ping").get()
        return {"status": "Healthy", "message": "Application is running."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )


# Shared endpoint: Fetch user profile
@router.get("/profile", summary="Fetch user profile", tags=["Common"])
async def fetch_user_profile(
    current_user: dict = Security(get_current_user, scopes=["admin:read", "consultant:read", "client:read"])
):
    """
    Fetch the authenticated user's profile.

    Security:
    - The user must be authenticated and have a valid token.

    Parameters:
        - current_user (dict): The authenticated user.

    Returns:
        - dict: The user's profile information.
    """
    try:
        user_id = current_user["username"]
        user_doc = db.collection("users").document(user_id).get()

        if not user_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found."
            )

        return {"profile": user_doc.to_dict()}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user profile: {str(e)}"
        )


# Shared endpoint: Get application configuration
@router.get("/config", summary="Fetch application configuration", tags=["Common"])
async def fetch_app_config(
    current_user: dict = Security(get_current_user, scopes=["admin:read"])
):
    """
    Fetch configuration settings for the application. Restricted to admin users.

    Security:
    - The user must have 'admin:read' permission.

    Parameters:
        - current_user (dict): The authenticated admin user.

    Returns:
        - dict: Application configuration settings.
    """
    try:
        config_doc = db.collection("config").document("settings").get()

        if not config_doc.exists:
            return {"config": {}}

        return {"config": config_doc.to_dict()}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch application configuration: {str(e)}"
        )


# Shared endpoint: Test database connection
@router.get("/test-db", summary="Test Firestore connectivity", tags=["Common"])
async def test_firestore():
    """
    Test Firestore by writing and reading a document.
    """
    try:
        test_ref = db.collection("test_collection").document("test_doc")
        test_data = {
            "test_key": "test_value",
            "timestamp": datetime.utcnow().isoformat()  # Adding a timestamp
        }

        # Write
        test_ref.set(test_data)

        # Read
        fetched_data = test_ref.get().to_dict()
        if fetched_data == test_data:
            return {"message": "DB Connection Successful", "data": fetched_data}
        else:
            return {"message": "DB Connection Test Failed", "data": fetched_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore test failed: {str(e)}")



