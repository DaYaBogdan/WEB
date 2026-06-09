# app/routers/customers.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.database import get_db
from app.models import User, Task, Settings
from app.schemas.User import UserResponse, UserCreate, UserUpdate
from app.security import get_password_hash

router = APIRouter()


# GET - получить всех мастеров
@router.get("/getAllMasters", response_model=List[UserResponse])
async def get_all_masters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).offset(skip).limit(limit).order_by(User.id)
    )
    masters = result.scalars().all()
    return masters

# GET - получить мастера по ID
@router.get("/getMaster/{master_id}", response_model=UserResponse)
async def get_master(
    master_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == master_id)
    )
    master = result.scalar_one_or_none()
    
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    return master

# POST - создать мастера
@router.post("/addMaster", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_master(
    master_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Проверяем существование логина
    result = await db.execute(
        select(User).where(User.login == master_data.login)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login already registered"
        )
    
    # Хешируем пароль
    hashed_password = get_password_hash(master_data.password)
    
    # Создаем мастера
    new_master = User(
        fio=master_data.fio,
        login=master_data.login,
        password=hashed_password,
        role=master_data.role if hasattr(master_data, 'role') else "master"
    )
    
    db.add(new_master)
    await db.commit()
    await db.refresh(new_master)
    
    return new_master

# PUT - обновить мастера
@router.put("/updateMaster/{master_id}", response_model=UserResponse)
async def update_master(
    master_id: int,
    master_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == master_id)
    )
    master = result.scalar_one_or_none()
    
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    
    # Обновляем поля
    if master_data.fio is not None:
        master.fio = master_data.fio
    
    if master_data.role is not None:
        master.role = master_data.role
    
    if master_data.password is not None and master_data.password.strip():
        master.password = get_password_hash(master_data.password)
    
    await db.commit()
    await db.refresh(master)
    
    return master

# DELETE - удалить мастера
@router.delete("/deleteMaster/{master_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_master(
    master_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == master_id)
    )
    master = result.scalar_one_or_none()
    
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    
    # Удаляем связанные задачи
    await db.execute(
        delete(Task).where(Task.master_id == master_id)
    )
    
    await db.execute(
        delete(Settings).where(Settings.user_id == master_id)
    )
    
    await db.delete(master)
    await db.commit()
    
    return None

# DELETE - удалить нескольких мастеров
@router.delete("/deleteMasters", status_code=status.HTTP_204_NO_CONTENT)
async def delete_masters(
    master_ids: List[int],
    db: AsyncSession = Depends(get_db)
):
    if not master_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No master IDs provided"
        )
    
    # Удаляем задачи всех мастеров
    await db.execute(
        delete(Task).where(Task.master_id.in_(master_ids))
    )
    
    # Удаляем мастеров
    await db.execute(
        delete(User).where(User.id.in_(master_ids))
    )
    
    await db.commit()
    return None