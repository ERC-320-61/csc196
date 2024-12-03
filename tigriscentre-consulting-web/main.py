"""
main.py

This is the entry point for the FastAPI application. It initializes the app, includes routes
from modularized endpoints, and sets up configurations for authentication, database, and more.
"""

import os
from fastapi import FastAPI
from dotenv import load_dotenv
from logging_config import logger  # Use centralized logging configuration
from firebase.firebase_config import db  # Shared Firestore client
from endpoints import (
    auth_router,
    admin_router,
    consultant_router,
    client_router,
    common_router,
)

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Tigris Centre Consulting API",
    description="API for managing users, appointments, and authentication for Tigris Centre Consulting.",
    version="1.0.0",
)

# Log application startup
logger.info("Starting Tigris Centre Consulting API")

# Include modular routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(consultant_router, prefix="/consultant", tags=["Consultants"])
app.include_router(client_router, prefix="/client", tags=["Clients"])
app.include_router(common_router, prefix="/common", tags=["Common"])

# Health check route
@app.get("/")
async def root():
    """
    Health check endpoint to verify that the application is running.
    """
    logger.info("Health check endpoint accessed")
    return {"status": "OK", "message": "Welcome to the Tigris Centre Consulting API!"}

# Log application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """
    Handle application shutdown events.
    """
    logger.info("Shutting down Tigris Centre Consulting API")

# For local development or Docker
if __name__ == "__main__":
    import uvicorn

    logger.info("Running application in development mode")
    uvicorn.run(app, host="0.0.0.0", port=8000)
