from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Settings
from app.schemas.Settings import SettingsResponse, SettingsUpdate

router = APIRouter()

# GET - получить настройки пользователя
@router.get("/get/{user_id}", response_model=SettingsResponse)
async def get_settings(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Settings).where(Settings.user_id == user_id)
    )
    settings = result.scalar_one_or_none()
    
    if not settings:
        # Если настроек нет, создаем с значениями по умолчанию
        settings = Settings(
            user_id=user_id,
            theme="light",
            language="ru"
        )
        db.add(settings)
        await db.commit()
        await db.refresh(settings)
    
    return settings

# PUT - обновление настроек
@router.put("/update/{user_id}", response_model=SettingsResponse)
async def update_settings(
    user_id: int,
    settings_data: SettingsUpdate,
    db: AsyncSession = Depends(get_db)
):
    # Ищем по user_id, а не по id
    result = await db.execute(
        select(Settings).where(Settings.user_id == user_id)
    )
    settings = result.scalar_one_or_none()
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settings not found"
        )
    
    # Обновляем поля
    if settings_data.theme is not None:
        settings.theme = settings_data.theme
    if settings_data.language is not None:
        settings.language = settings_data.language
    
    await db.commit()
    await db.refresh(settings)
    
    return settings