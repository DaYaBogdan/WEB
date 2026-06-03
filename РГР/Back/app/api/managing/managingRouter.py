from fastapi import APIRouter
from .customers import router as customer_router

api_router = APIRouter(
    prefix="/managing",
    tags=["Managing"]
)
api_router.include_router(customer_router)