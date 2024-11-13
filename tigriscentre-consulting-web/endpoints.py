# Import FastAPI dependencies and the get_current_user function
from fastapi import Security
from main import app  # Import the FastAPI app instance
from auth_utils import get_current_user  # Import the authorization utility function


# Admin-only endpoint to access analytics data
@app.get("/admin/analytics")
async def get_analytics(
        current_user: dict = Security(get_current_user, scopes=["admin:analytics"])
):
    """
    Access analytics data (admin only).

    :param current_user: The current authenticated user with the necessary 'admin:analytics' scope
    :return: Analytics data if the user is authorized
    """
    # Example response, replace with actual analytics retrieval logic
    return {"data": "Admin analytics data"}


# Consultant-only endpoint to view and edit their profile
@app.get("/consultant/profile")
async def get_consultant_profile(
        current_user: dict = Security(get_current_user, scopes=["consultant:profile"])
):
    """
    Access consultant's profile (consultant only).

    :param current_user: The current authenticated user with the necessary 'consultant:profile' scope
    :return: Consultant's profile data if the user is authorized
    """
    # Example response, replace with actual profile data retrieval logic
    return {"profile": "Consultant profile details"}


# Client-only endpoint to book an appointment
@app.post("/client/appointments")
async def book_appointment(
        current_user: dict = Security(get_current_user, scopes=["client:appointments"])
):
    """
    Book an appointment (client only).

    :param current_user: The current authenticated user with the necessary 'client:appointments' scope
    :return: Confirmation of appointment booking if the user is authorized
    """
    # Example response, replace with actual booking logic
    return {"status": "Appointment booked"}
