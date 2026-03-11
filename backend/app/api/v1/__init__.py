"""API v1 routes."""
from fastapi import APIRouter

from . import settings

api_router = APIRouter()

# Include all v1 routes
api_router.include_router(settings.router)

__all__ = ["api_router"]
