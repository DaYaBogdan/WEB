from fastapi import APIRouter
from .tasks import router as tasks_router

api_router = APIRouter(
    prefix="/diary",
    tags=["Tasks"]
)
api_router.include_router(tasks_router)