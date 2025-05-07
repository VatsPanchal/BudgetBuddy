from sqlalchemy import Column, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database.db_setup import Base

class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    income = Column(Float, nullable=False)
    savings_goal = Column(Float, nullable=False)
    categories = Column(JSON, nullable=False)  # Stores category allocations as JSON

    user = relationship("User", back_populates="budgets") 