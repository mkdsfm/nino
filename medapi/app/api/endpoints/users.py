from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models
from app.schemas import user as user_schemas
from app.api.dependencies import get_user_by_id

router = APIRouter()


@router.post("/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: user_schemas.UserCreate,
) -> Any:
    """
    Create a new user
    """
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user_in.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Create new user
    user = models.User(
        username=user_in.username,
        age=user_in.age,
        gender=user_in.gender,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=List[user_schemas.User])
def read_users(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users
    """
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(
    *,
    user: models.User = Depends(get_user_by_id),
) -> Any:
    """
    Get a specific user by id
    """
    return user


@router.put("/{user_id}", response_model=user_schemas.User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user_by_id),
    user_in: user_schemas.UserUpdate,
) -> Any:
    """
    Update a user
    """
    if user_in.username is not None:
        # Check if new username already exists for a different user
        existing_user = db.query(models.User).filter(models.User.username == user_in.username).first()
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        user.username = user_in.username
    
    if user_in.age is not None:
        user.age = user_in.age
    
    if user_in.gender is not None:
        user.gender = user_in.gender
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=user_schemas.User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user_by_id),
) -> Any:
    """
    Delete a user
    """
    db.delete(user)
    db.commit()
    return user
