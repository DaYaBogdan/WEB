from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://Bogdan:Smi09120923@localhost:5432/web_db" # Замените на свои данные

    class Config:
        env_file = ".env" # Указываем, откуда брать переменные

settings = Settings()