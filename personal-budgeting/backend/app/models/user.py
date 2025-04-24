from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
import random
import string
from app.database import Base

def generate_user_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(String(6), unique=True, nullable=False, default=generate_user_id)  # User ID (6 alphanumeric)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed password
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=True)
    income = Column(Float, nullable=False)
    savings = Column(Float, nullable=False)

    # Relationships
    budgets = relationship('Budget', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')
