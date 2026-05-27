from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, AsyncSessionLocal
from app.api.apiRouter import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этот код выполнится ПРИ ЗАПУСКЕ приложения
    print("Starting up...")
    # Движок уже создан, ничего делать не нужно, если только вы не хотите проверить соединение
    # Например, можно выполнить простой запрос для проверки:
    # async with engine.connect() as conn:
    #     await conn.execute("SELECT 1")
    yield
    # Этот код выполнится ПРИ ОСТАНОВКЕ приложения
    print("Shutting down...")
    await engine.dispose() # Закрываем все соединения в пуле

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],  # Адрес вашего Vite сервера
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")