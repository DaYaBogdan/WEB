# app/api/auth/register.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.schemas.User import UserCreate, UserResponse
from app.security import get_password_hash

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким логином
    stmt = select(User).where(User.login == user_data.login)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login already registered"
        )
    
    # Хешируем пароль
    hashed_password = get_password_hash(user_data.password)
    
    # Создаём нового пользователя
    new_user = User(
        fio=user_data.fio,
        login=user_data.login,
        password=hashed_password,
        role='master'
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Возвращаем данные пользователя (без пароля)
    return new_user