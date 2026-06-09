from fastapi import APIRouter
from .userSettings import router as settings_router

api_router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)
api_router.include_router(settings_router)