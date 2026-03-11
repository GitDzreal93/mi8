from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ...services.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    """
    Simple login endpoint for local development.
    In production, this should verify against a real user database.
    For now, any username/password combination will work.
    """
    # In a real application, verify credentials against database
    # For local dev, we accept any credentials
    access_token = create_access_token(data={"sub": payload.username})
    return TokenResponse(access_token=access_token)

@router.post("/token", response_model=TokenResponse)
async def get_token(payload: LoginRequest):
    """OAuth2 compatible token endpoint."""
    return await login(payload)
