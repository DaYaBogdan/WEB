from fastapi import APIRouter
from .tasks import router as tasks_router
from .weekends import router as weekends_router

api_router = APIRouter(
    prefix="/diary",
    tags=["Diary"]
)
api_router.include_router(tasks_router)
api_router.include_router(weekends_router)
