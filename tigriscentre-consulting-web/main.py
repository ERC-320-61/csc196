# Import necessary libraries
from fastapi import FastAPI, Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel
import jwt  # Import JWT for token decoding and verification
from typing import Optional

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

# Dummy user database
users_db = {
    "admin": {"username": "admin", "scopes": ["admin:manage", "admin:analytics"]},
    "consultant": {"username": "consultant", "scopes": ["consultant:profile", "consultant:appointments"]},
    "client": {"username": "client", "scopes": ["client:appointments"]},
}


# Define a function to verify the token and scopes
async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_scopes = payload.get("scopes", [])

        # Check for required scopes
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
                )

        return {"username": username, "scopes": token_scopes}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Define models for the token response
class Token(BaseModel):
    access_token: str
    token_type: str


# Route to obtain token (dummy token generation here for testing)
@app.post("/token", response_model=Token)
async def login():
    # This is a dummy implementation that issues a hardcoded token
    token_data = {
        "sub": "admin",
        "scopes": ["admin:manage", "admin:analytics"],
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


# Admin-only endpoint for analytics
@app.get("/admin/analytics")
async def get_analytics(current_user: dict = Security(get_current_user, scopes=["admin:analytics"])):
    return {"data": "Admin analytics data"}


# Consultant profile endpoint
@app.get("/consultant/profile")
async def get_consultant_profile(current_user: dict = Security(get_current_user, scopes=["consultant:profile"])):
    return {"profile": "Consultant profile details"}


# Client appointment booking endpoint
@app.post("/client/appointments")
async def book_appointment(current_user: dict = Security(get_current_user, scopes=["client:appointments"])):
    return {"status": "Appointment booked"}


# Run the app with uvicorn (for local development or Docker)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
