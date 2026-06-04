# app/routers/customers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.database import get_db
from app.models import User, Task
from app.schemas.User import UserResponse

router = APIRouter()

# GET - получить всех клиентов
@router.get("/getAllMasters", response_model=list[UserResponse])
async def get_all_masters(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).offset(skip).limit(limit).order_by(User.id)
    )
    masters = result.scalars().all()
    
    # Явная конвертация (хотя FastAPI должен сделать это автоматически)
    return [UserResponse.model_validate(master) for master in masters]

# PUT - полное обновление клиента
# @router.put("/updateClient/{customer_id}", response_model=UserResponse)
# async def update_customer(
#     customer_id: int,
#     customer_data: CustomerUpdate,
#     db: AsyncSession = Depends(get_db)
# ):
#     result = await db.execute(
#         select(Customer).where(Customer.id == customer_id)
#     )
#     customer = result.scalar_one_or_none()
    
#     if not customer:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Customer not found"
#         )
    
#     # Обновляем поля
#     if customer_data.FIO is not None:
#         customer.FIO = customer_data.FIO
#     if customer_data.phone is not None:
#         # Проверка дубликата нового телефона
#         existing = await db.execute(
#             select(Customer).where(
#                 Customer.phone == customer_data.phone,
#                 Customer.id != customer_id
#             )
#         )
#         if existing.scalar_one_or_none():
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Phone number already used by another customer"
#             )
#         customer.phone = customer_data.phone
    
#     # updated_at обновится автоматически благодаря onupdate=func.now()
#     await db.commit()
#     await db.refresh(customer)
    
#     return customer

# DELETE - удалить клиента
@router.delete("/deleteMaster/{master_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
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
            detail="Customer not found"
        )
    
    await db.execute(
        delete(Task).where(Task.master_id == master_id)
    )
    
    await db.delete(master)
    await db.commit()
    
    return None