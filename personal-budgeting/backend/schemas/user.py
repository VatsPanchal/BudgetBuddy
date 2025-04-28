from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str]

    class Config:
        orm_mode = True
