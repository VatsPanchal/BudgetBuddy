from sqlalchemy import Column, Integer, Float, ForeignKey, String
from app.database import Base
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)  # Optional description of the transaction
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')
