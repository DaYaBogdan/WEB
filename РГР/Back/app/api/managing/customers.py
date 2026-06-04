# app/routers/customers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.database import get_db
from app.models.__init__ import Customer, Task
from app.schemas.Customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter()

# POST - создание клиента
@router.post("/newClient", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    # Проверка на дубликат по телефону
    existing = await db.execute(
        select(Customer).where(Customer.phone == customer_data.phone)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this phone already exists"
        )
    
    # Создаём нового клиента (поля created_at и updated_at добавятся автоматически)
    new_customer = Customer(
        FIO=customer_data.FIO,
        phone=customer_data.phone
    )
    
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    
    return new_customer

# GET - получить всех клиентов
@router.get("/getAllClients", response_model=list[CustomerResponse])
async def get_all_customers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Customer).offset(skip).limit(limit).order_by(Customer.id)
    )
    customers = result.scalars().all()
    return customers

# GET - получить одного клиента по ID
# @router.get("/GetExactClient/{customer_id}", response_model=CustomerResponse)
# async def get_customer_by_id(
#     customer_id: int,
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
    
#     return customer

# PUT - полное обновление клиента
@router.put("/updateClient/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Обновляем поля
    if customer_data.FIO is not None:
        customer.FIO = customer_data.FIO
    if customer_data.phone is not None:
        # Проверка дубликата нового телефона
        existing = await db.execute(
            select(Customer).where(
                Customer.phone == customer_data.phone,
                Customer.id != customer_id
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already used by another customer"
            )
        customer.phone = customer_data.phone
    
    # updated_at обновится автоматически благодаря onupdate=func.now()
    await db.commit()
    await db.refresh(customer)
    
    return customer

# DELETE - удалить клиента
@router.delete("/deleteClient/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    await db.execute(
        delete(Task).where(Task.customer_id == customer_id)
    )
    
    await db.delete(customer)
    await db.commit()
    
    return None