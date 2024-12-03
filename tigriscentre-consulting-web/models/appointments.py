"""
appointments.py

Defines the Pydantic model for the `appointments` collection in Firestore.
This model is used for data validation and type checking when handling appointment-related data.
"""

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Literal, Optional
from logging_config import logger


class Appointment(BaseModel):
    """Pydantic model for appointment data validation."""

    appointment_id: Optional[str] = Field(None, description="Unique ID for the appointment.")
    client_id: str = Field(..., description="Reference to the client user document.")
    consultant_id: str = Field(..., description="Reference to the consultant user document.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the appointment was created.")
    notes: Optional[str] = Field("", description="Additional notes for the appointment.")
    scheduled_time: datetime = Field(..., description="Scheduled time for the appointment.")
    status: Literal["scheduled", "completed", "canceled"] = Field(..., description="Current status of the appointment.")

    def __init__(self, **data):
        """Initialize and validate appointment data."""
        try:
            super().__init__(**data)
            logger.info(f"Appointment created successfully for client_id: {data.get('client_id')} and consultant_id: {data.get('consultant_id')}")
        except ValidationError as e:
            logger.error(f"Validation error while creating appointment: {e}")
            raise e

    def to_dict(self) -> dict:
        """
        Convert the appointment instance to a dictionary, omitting None values.

        Returns:
            dict: Dictionary representation of the appointment instance.
        """
        appointment_dict = {key: value for key, value in self.dict().items() if value is not None}
        logger.debug(f"Converted appointment object to dictionary: {appointment_dict}")
        return appointment_dict


# Example usage (for testing or development purposes)
if __name__ == "__main__":
    try:
        # Creating an appointment instance for testing
        appointment = Appointment(
            client_id="client123",
            consultant_id="consultant456",
            scheduled_time=datetime(2024, 12, 15, 14, 30),
            status="scheduled",
        )
        print(appointment.to_dict())
    except ValidationError as e:
        logger.error(f"Appointment creation failed: {e}")
