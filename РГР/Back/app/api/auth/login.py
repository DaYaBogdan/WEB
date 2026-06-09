from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...security import verify_password

from ...schemas.User import LoginData, UserResponse
from ...schemas.Settings import SettingsCreate

# Предположим, у вас есть зависимость get_db для сессии БД
from app.database import get_db
# И модель пользователя (пример)    
from ...models import User, Settings

router = APIRouter()

@router.post("/login")
async def login(
    login_data: LoginData,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.login == login_data.login))
    user = result.scalar_one_or_none()

    post_result = await db.execute(select(Settings).where(Settings.user_id == user.id))
    settings = post_result.scalar_one_or_none()
    
    # Проверка пароля
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"user": UserResponse.model_validate(user), "settings": settings, "access_token": "sfsfrhgereh"}

# ПЕРЕДЕЛАТЬ, НЕ ДОЛЖЕН ПАРОЛЬ ПОПАДАТЬ С ЮЗЕРОМ НА ФРОНТ