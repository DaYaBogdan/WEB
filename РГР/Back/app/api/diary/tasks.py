from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.database import get_db

from ...models import User, Task, Customer
from app.schemas.Task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()

@router.post("/pushTask", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def pushTask(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Проверяем, существует ли customer
        pre_query_customer = select(Customer).where(Customer.id == task_data.customer_id)
        customer = await db.execute(pre_query_customer)
        if not customer.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Проверяем, существует ли master (user)
        pre_query_master = select(User).where(User.id == task_data.master_id)
        master = await db.execute(pre_query_master)
        if not master.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Master not found")
        
        # Создаём новую задачу
        new_task = Task(
            customer_id=task_data.customer_id,
            master_id=task_data.master_id,
            service=task_data.service,
            dateTime=task_data.datetime,
            cost=task_data.cost
        )
        
        # Добавляем в БД
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)  # Обновляем объект (получаем id, created_at, updated_at)
        
        return new_task
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )

@router.get("/getTasks/{user_id}")
async def getTasks(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = select(Task).where(Task.master_id == user_id)
    result = await db.execute(query)
    tasks = result.scalars().all()  # используйте scalars() вместо all()
    
    return {"tasks": [TaskResponse.model_validate(task) for task in tasks]}

@router.put("/updateTask/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновление задачи"""
    # Проверяем, существует ли задача
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Обновляем только те поля, которые были переданы
    update_data = task_update.model_dump(exclude_unset=True)
    
    if update_data:
        # Обновляем поля
        for field, value in update_data.items():
            setattr(task, field, value)
        
        # updated_at обновится автоматически благодаря onupdate в модели
        await db.commit()
        await db.refresh(task)
    
    return task

@router.delete("/deleteTask/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удаление задачи"""
    # Проверяем, существует ли задача
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    await db.delete(task)
    await db.commit()
    
    return None  # 204 No Content