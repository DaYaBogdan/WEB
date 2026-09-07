from fastapi import APIRouter
from .authentication import router as auth_router

api_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
    )
api_router.include_router(auth_router)