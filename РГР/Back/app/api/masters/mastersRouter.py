from fastapi import APIRouter
from .masters import router as masters_router

api_router = APIRouter(
    prefix="/masters",
    tags=["Masters"]
)
api_router.include_router(masters_router)