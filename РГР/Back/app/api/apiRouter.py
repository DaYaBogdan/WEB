from fastapi import APIRouter
from app.api.auth.authRouter import api_router as auth_router
from app.api.diary.diaryRouter import api_router as diary_router
from app.api.managing.managingRouter import api_router as managing_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(diary_router)
api_router.include_router(managing_router)