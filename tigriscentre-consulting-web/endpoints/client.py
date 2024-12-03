"""
client.py

Endpoints for client-specific functionality, such as booking and managing their own appointments.
Only accessible to users with the "client:appointments" scope.

Dependencies:
- FastAPI for building APIs
- Pydantic for request/response validation
- Firebase Firestore for database operations
"""

from fastapi import APIRouter, Security, HTTPException, status
from firebase_admin import firestore
from utils.auth_utils import get_current_user  # Use centralized function
from pydantic import BaseModel, Field
from datetime import datetime

# Initialize Firestore client
db = firestore.client()

# Create a router for client-specific endpoints
router = APIRouter(
    prefix="/client",
    tags=["Client"],
    dependencies=[Security(get_current_user, scopes=["client:appointments"])],
)

# Pydantic model for booking an appointment
class AppointmentBooking(BaseModel):
    date: str = Field(..., description="Date of the appointment in YYYY-MM-DD format")
    time: str = Field(..., description="Time of the appointment in HH:MM format")
    consultant_id: str = Field(..., description="ID of the consultant")
    notes: str = Field(None, description="Optional notes for the appointment")


# Endpoint to book an appointment
@router.post("/appointments", summary="Book a new appointment")
async def book_appointment(
    appointment: AppointmentBooking,
    current_user: dict = Security(get_current_user, scopes=["client:appointments"]),
):
    """
    Book a new appointment for the authenticated client.

    Args:
        appointment (AppointmentBooking): Appointment details.
        current_user (dict): The current authenticated user.

    Returns:
        dict: Confirmation of the booked appointment.
    """
    try:
        client_id = current_user["username"]
        appointment_data = appointment.dict()
        appointment_data["client_id"] = client_id
        appointment_data["status"] = "scheduled"
        appointment_data["created_at"] = datetime.utcnow().isoformat()

        # Generate a new appointment document
        appointment_ref = db.collection("appointments").document()
        appointment_ref.set(appointment_data)

        return {
            "message": "Appointment booked successfully.",
            "appointment_id": appointment_ref.id,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to book appointment: {str(e)}",
        )


# Endpoint to view all appointments for the logged-in client
@router.get("/appointments", summary="View client appointments")
async def view_client_appointments(
    current_user: dict = Security(get_current_user, scopes=["client:appointments"]),
):
    """
    Fetch all appointments for the authenticated client.

    Args:
        current_user (dict): The current authenticated user.

    Returns:
        dict: List of the client's appointments.
    """
    try:
        client_id = current_user["username"]
        appointments_ref = db.collection("appointments").where("client_id", "==", client_id)
        appointments = [doc.to_dict() for doc in appointments_ref.stream()]

        return {"appointments": appointments}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve client appointments: {str(e)}",
        )


# Endpoint to cancel an appointment
@router.delete("/appointments/{appointment_id}", summary="Cancel an appointment")
async def cancel_appointment(
    appointment_id: str,
    current_user: dict = Security(get_current_user, scopes=["client:appointments"]),
):
    """
    Cancel an appointment.

    Args:
        appointment_id (str): The ID of the appointment to cancel.
        current_user (dict): The current authenticated user.

    Returns:
        dict: Confirmation of the cancellation.
    """
    try:
        client_id = current_user["username"]
        appointment_ref = db.collection("appointments").document(appointment_id)
        appointment = appointment_ref.get()

        # Check if the appointment exists
        if not appointment.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} not found.",
            )

        appointment_data = appointment.to_dict()

        # Verify the client owns the appointment
        if appointment_data.get("client_id") != client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to cancel this appointment.",
            )

        # Update the appointment status to "canceled"
        appointment_ref.update({"status": "canceled"})

        return {
            "message": f"Appointment {appointment_id} canceled successfully.",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel appointment: {str(e)}",
        )
