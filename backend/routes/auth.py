from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import hashlib
import secrets
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import logging
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username": username}


# Environment variables or hardcode for now
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Exception("Invalid token")
        return username
    except JWTError:
        raise Exception("Token is invalid")


from database.db_setup import get_db
from models.user import User
from models.expense import Expense
from models.budget import Budget


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address for password reset")

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, description="New password must be at least 8 characters long")

class DeleteAccountRequest(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest() + ":" + salt

def verify_password(password: str, hashed_password: str) -> bool:
    stored_hash, salt = hashed_password.split(":")
    return hashlib.sha256((password + salt).encode()).hexdigest() == stored_hash

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import traceback

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = hash_password(user.password)
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 🔥 Create JWT token for new user
    access_token = create_access_token(data={"sub": new_user.username})
    
    return {
        "message": "User created successfully",
        "token": access_token,
        "token_type": "bearer"
    }


@router.post("/login")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Try to find user by username or email
    user = db.query(User).filter(
        (User.username == login_data.username) | 
        (User.email == login_data.username)
    ).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": user.username,  # Using username as token for now
        "token_type": "bearer"
    }

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    logging.info(f"Received forgot password request for email: {request.email}")
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        logging.info(f"No user found with email: {request.email}")
        return {"message": "If an account exists with this email, a password reset link has been sent"}
    logging.info(f"User found with email: {request.email}")
    # In a real application, send an email with a reset token
    return {"message": "If an account exists with this email, a password reset link has been sent"}

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    logging.info(f"Received reset password request for token: {request.token}")
    user = db.query(User).filter(User.email == request.token).first()
    if not user:
        logging.info(f"No user found with token: {request.token}")
        raise HTTPException(status_code=400, detail="Invalid reset token")
    
    user.hashed_password = hash_password(request.new_password)
    db.commit()
    logging.info(f"Password reset successful for user: {user.email}")
    return {"message": "Password updated successfully"}

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Find user by username (which is our token)
    user = db.query(User).filter(User.username == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email
    }

@router.delete("/delete-account")
async def delete_account(
    request: DeleteAccountRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        # Verify the token matches the username
        if token != request.username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Find the user
        user = db.query(User).filter(User.username == request.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify password
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )
        
        # Delete all expenses associated with the user
        db.query(Expense).filter(Expense.user_id == user.id).delete()
        
        # Delete the user's budget
        db.query(Budget).filter(Budget.user_id == user.id).delete()
        
        # Delete the user
        db.delete(user)
        db.commit()
        
        return {"message": "Account deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 