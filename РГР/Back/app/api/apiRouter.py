from fastapi import APIRouter
from .auth.authRouter import api_router as auth_router
from .diary.diaryRouter import api_router as diary_router
from .managing.managingRouter import api_router as managing_router
from .masters.mastersRouter import api_router as masters_router
from .settings.settingsRouter import api_router as settings_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(diary_router)
api_router.include_router(managing_router)
api_router.include_router(masters_router)
api_router.include_router(settings_router)