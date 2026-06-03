from fastapi import APIRouter
from app.api.auth.login import router as log_router
from app.api.auth.register import router as rg_router

api_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
    )
api_router.include_router(log_router)
api_router.include_router(rg_router)