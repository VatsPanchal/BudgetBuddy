from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from fastapi import HTTPException

def create_user(db: Session, user: UserCreate):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
