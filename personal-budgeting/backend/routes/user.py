from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import user as user_model
from schemas import user as user_schemas
from database import SessionLocal, engine
from crud import User_crud
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=user_schemas.UserOut)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Received registration request for user: {user.email}")
    try:
        result = User_crud.create_user(db=db, user=user)
        logger.info(f"User created successfully: {result.email}")
        return result
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))