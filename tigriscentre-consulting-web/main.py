# Import necessary libraries
from fastapi import FastAPI, Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt  # Import JWT for token decoding and verification

# Initialize FastAPI application
app = FastAPI()

# Define secret key and algorithm for JWT token encoding and decoding
SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
ALGORITHM = "HS256"

# Define OAuth2PasswordBearer for handling token-based authentication
# with specified scopes for each role
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "admin:manage": "Full access for managing consultants, clients, appointments.",
        "admin:analytics": "Access analytics and reporting.",
        "consultant:profile": "Manage own profile.",
        "consultant:availability": "Set and update own availability.",
        "consultant:appointments": "Manage own appointments.",
        "consultant:messages": "Communicate with clients.",
        "client:browse_consultants": "Browse consultants.",
        "client:appointments": "Manage own appointments.",
        "client:messages": "Message consultants.",
    },
)
