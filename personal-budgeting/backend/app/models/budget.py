from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    # Relationships
    user = relationship('User', back_populates='budgets')
    category = relationship('Category', back_populates='budgets')
