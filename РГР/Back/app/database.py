from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

# Создаем асинхронный движок
# Параметры pool_size и max_overflow настраивают пул подключений
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,                # Логирует все SQL-запросы (полезно при разработке)
    pool_size=5,              # Количество постоянных соединений в пуле
    max_overflow=10,          # Максимум временных соединений сверх pool_size
    pool_pre_ping=True,       # Проверять соединение перед использованием
)

# Фабрика сессий. Она будет создавать новые сессии для каждого запроса
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,   # Важно: объекты модели не будут устаревать после коммита
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session