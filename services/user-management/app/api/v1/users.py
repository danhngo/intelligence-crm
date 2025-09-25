"""User management endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserInDB)
async def read_user_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user."""
    return current_user


@router.put("/me", response_model=UserInDB)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update current user."""
    async with db as session:
        if user_in.email and user_in.email != current_user.email:
            result = await session.execute(
                select(User).where(User.email == user_in.email)
            )
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
                
        for field, value in user_in.dict(exclude_unset=True).items():
            if field == "password":
                setattr(current_user, "hashed_password", get_password_hash(value))
            else:
                setattr(current_user, field, value)
                
        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)
        
        return current_user


@router.get("/", response_model=List[UserInDB])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_active_superuser)
) -> Any:
    """Get all users."""
    async with db as session:
        result = await session.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()


@router.post("/", response_model=UserInDB)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
    _: User = Depends(get_current_active_superuser)
) -> Any:
    """Create new user."""
    async with db as session:
        # Check if user exists
        result = await session.execute(
            select(User).where(User.email == user_in.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        # Create new user
        db_user = User(
            email=user_in.email,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            hashed_password=get_password_hash(user_in.password),
            is_active=user_in.is_active,
            is_superuser=False,
            email_verified=False
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        
        return db_user


@router.get("/{user_id}", response_model=UserInDB)
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get user by ID."""
    async with db as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        if not current_user.is_superuser and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
            
        return user


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """Update user."""
    async with db as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        if user_in.email and user_in.email != user.email:
            result = await session.execute(
                select(User).where(User.email == user_in.email)
            )
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
                
        for field, value in user_in.dict(exclude_unset=True).items():
            if field == "password":
                setattr(user, "hashed_password", get_password_hash(value))
            else:
                setattr(user, field, value)
                
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        return user


@router.delete("/{user_id}", response_model=UserInDB)
async def delete_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str,
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """Delete user."""
    async with db as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        await session.delete(user)
        await session.commit()
        
        return user
