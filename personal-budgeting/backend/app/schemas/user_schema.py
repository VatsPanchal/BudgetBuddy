from pydantic import BaseModel
from typing import Optional  # To make phone optional

class UserCreate(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: Optional[str] = None  # Optional field (phone number is not required)

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy models
