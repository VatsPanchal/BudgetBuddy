from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Create the user (but don't worry about income/setup yet)
    new_user = crud.create_user(db=db, 
                                username=user.username, 
                                email=user.email, 
                                password=user.password,
                                first_name=user.firstName,
                                last_name=user.lastName,
                                phone=user.phone)  # optional phone field
    return {"message": "Account created successfully. Please proceed to setup your profile.", "user_id": new_user.id}
