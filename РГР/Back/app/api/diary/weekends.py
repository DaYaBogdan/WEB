from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db

from ...models import User, Weekend
from app.schemas.Weekend import WeekendResponse, WeekendSchema

router = APIRouter()

@router.post("/makeWeekend", response_model=WeekendResponse, status_code=status.HTTP_201_CREATED)
async def makeWeekend(
    weekend_data: WeekendSchema,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Проверяем, существует ли master (user)
        pre_query_master = select(User).where(User.id == weekend_data.master_id)
        master = await db.execute(pre_query_master)
        if not master.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Master not found")
        
        # Проверяем, существует ли выходной на этот день
        stmt = select(Weekend).where(
            Weekend.master_id == weekend_data.master_id,
            Weekend.date == weekend_data.date
        )
        result = await db.execute(stmt)
        existing_weekend = result.scalar_one_or_none()
        if existing_weekend:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Weekend already pushed"
            )
        
        # Создаём новую задачу
        new_weekend = Weekend(
            master_id=weekend_data.master_id,
            date=weekend_data.date
        )
        
        db.add(new_weekend)
        await db.commit()
        await db.refresh(new_weekend)  
        
        return new_weekend
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )

@router.get("/getWeekends/{user_id}")
async def getTasks(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = select(Weekend).where(Weekend.master_id == user_id)
    result = await db.execute(query)
    weekends = result.scalars().all()
    
    return {"weekends": [WeekendResponse.model_validate(weekend) for weekend in weekends]}

@router.delete("/deleteWeekend/{weekend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    weekend_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удаление задачи"""
    # Проверяем, существует ли задача
    query = select(Weekend).where(Weekend.id == weekend_id)
    result = await db.execute(query)
    weekend = result.scalar_one_or_none()
    
    if not weekend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    await db.delete(weekend)
    await db.commit()
    
    return None  # 204 No Content