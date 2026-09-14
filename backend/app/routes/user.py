from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas.user import UserResponse, UserCreate

router = APIRouter(tags=["Users"])


@router.get("/users", response_model=List[UserResponse])
@router.get("/users/", response_model=List[UserResponse])
@router.get("/user", response_model=List[UserResponse])
@router.get("/user/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@router.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@router.post("/user/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name=user_in.name,
        email=user_in.email,
        is_active=user_in.is_active,
        preferences=user_in.preferences,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user