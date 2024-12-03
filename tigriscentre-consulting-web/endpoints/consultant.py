"""
consultant.py

Endpoints for consultant-specific functionality, such as managing their own appointments.
Only accessible to users with the "consultant:appointments" scope.

Dependencies:
- FastAPI for building APIs
- Pydantic for request/response validation
- Firebase Firestore for database operations
"""

from fastapi import APIRouter, Security, HTTPException, status
from firebase_admin import firestore
from utils.auth_utils import get_current_user  # Use centralized function
from pydantic import BaseModel, Field
from typing import Literal

# Initialize Firestore client
db = firestore.client()

# Create a router for consultant-specific endpoints
router = APIRouter(
    prefix="/consultant",
    tags=["Consultant"],
    dependencies=[Security(get_current_user, scopes=["consultant:appointments"])],
)

# Pydantic model for updating appointment notes
class AppointmentNotes(BaseModel):
    notes: str = Field(..., description="Notes to update for the appointment")

# Pydantic model for updating appointment status
class AppointmentStatusUpdate(BaseModel):
    status: Literal["scheduled", "completed", "canceled"] = Field(
        ..., description="New status for the appointment"
    )

# Endpoint to view all appointments for the logged-in consultant
@router.get("/appointments")
async def get_consultant_appointments(
    current_user: dict = Security(get_current_user, scopes=["consultant:appointments"])
):
    """
    Fetch all appointments for the authenticated consultant.

    Args:
        current_user (dict): The current authenticated user.

    Returns:
        dict: List of the consultant's appointments.
    """
    try:
        consultant_id = current_user["username"]
        appointments_ref = db.collection("appointments").where("consultant_id", "==", consultant_id)
        appointments = [doc.to_dict() for doc in appointments_ref.stream()]
        return {"appointments": appointments}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve consultant appointments: {str(e)}",
        )

# Endpoint to update notes for a specific appointment
@router.patch("/appointments/{appointment_id}/notes")
async def update_appointment_notes(
    appointment_id: str,
    notes: AppointmentNotes,
    current_user: dict = Security(get_current_user, scopes=["consultant:appointments"])
):
    """
    Update notes for a specific appointment.

    Args:
        appointment_id (str): The ID of the appointment to update.
        notes (AppointmentNotes): The notes to update.
        current_user (dict): The current authenticated user.

    Returns:
        dict: Confirmation of the update.
    """
    try:
        consultant_id = current_user["username"]
        appointment_ref = db.collection("appointments").document(appointment_id)
        appointment = appointment_ref.get()

        if not appointment.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} not found.",
            )

        appointment_data = appointment.to_dict()
        if appointment_data.get("consultant_id") != consultant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this appointment.",
            )

        appointment_ref.update({"notes": notes.notes})
        return {"message": f"Notes for appointment {appointment_id} updated successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update appointment notes: {str(e)}",
        )

# Endpoint to update the status of an appointment
@router.patch("/appointments/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: str,
    status_update: AppointmentStatusUpdate,
    current_user: dict = Security(get_current_user, scopes=["consultant:appointments"])
):
    """
    Update the status of an appointment (e.g., scheduled, completed, canceled).

    Args:
        appointment_id (str): The ID of the appointment to update.
        status_update (AppointmentStatusUpdate): The new status of the appointment.
        current_user (dict): The current authenticated user.

    Returns:
        dict: Confirmation of the status update.
    """
    try:
        consultant_id = current_user["username"]
        appointment_ref = db.collection("appointments").document(appointment_id)
        appointment = appointment_ref.get()

        if not appointment.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} not found.",
            )

        appointment_data = appointment.to_dict()
        if appointment_data.get("consultant_id") != consultant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this appointment.",
            )

        appointment_ref.update({"status": status_update.status})
        return {"message": f"Status for appointment {appointment_id} updated to '{status_update.status}'."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update appointment status: {str(e)}",
        )
