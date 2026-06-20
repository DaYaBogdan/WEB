from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, AsyncSessionLocal
from app.api.apiRouter import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],  # Адрес вашего Vite сервера
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")