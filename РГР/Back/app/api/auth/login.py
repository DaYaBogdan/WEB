from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.User import LoginData

# Предположим, у вас есть зависимость get_db для сессии БД
from app.database import get_db
# И модель пользователя (пример)    
from ...models.user import User

router = APIRouter(
    prefix="/auth",      # Все эндпоинты этого роутера будут начинаться с /auth
    tags=["authentication"]  # Для группировки в документации Swagger
)

@router.get("/")
async def getHello():
    return {"message": "Hello world"}

@router.post("/login")
async def login(
    login_data: LoginData,
    db: AsyncSession = Depends(get_db)
):
    # Здесь будет ваша логика проверки пользователя
    # Например, поиск пользователя по email
    # result = await db.execute(select(User).where(User.email == login_data.email))
    # user = result.scalar_one_or_none()
    # if not user or not verify_password(login_data.password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    # return {"access_token": create_token(user)}
    
    # Пока просто заглушка
    return {"message": f"Login attempt for {login_data.email}"}