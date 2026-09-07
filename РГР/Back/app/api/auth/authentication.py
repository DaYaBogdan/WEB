from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.core.security import verify_password, hash_password, create_access_token

from app.schemas.Token import Token
from app.schemas.User import UserCreate, LoginData, UserResponse

from app.db.database import get_db
from app.api.deps import get_current_user, require_role
from app.models import User, Settings


router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(require_role("admin"))
):
    stmt = select(User).where(User.login == user_data.login)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login already registered"
        )

    hashed_password = hash_password(user_data.password)

    new_user = User(
        fio=user_data.fio,
        login=user_data.login,
        password=hashed_password,
        role="master"
    )
    db.add(new_user)
    await db.flush()

    settings = Settings(
        user_id=new_user.id,
        theme="light",
        language="ru"
    )
    db.add(settings)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login already registered"
        )

    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginData,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.login == login_data.login))
    user = result.scalar_one_or_none()

    # Check user existence AND password BEFORE touching user.id anywhere else
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    settings_result = await db.execute(select(Settings).where(Settings.user_id == user.id))
    settings = settings_result.scalar_one_or_none()

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})

    user.token = access_token
    await db.commit()
    await db.refresh(user)

    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(user),
        settings=settings,
    )
    
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user