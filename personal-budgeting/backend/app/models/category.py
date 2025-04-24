from sqlalchemy import Column, Integer, String
from app.database import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Name of the category (e.g., Food & Dining)
    emoji = Column(String(5))  # Emoji representation (e.g., 🍔)

    def __repr__(self):
        return f"<Category(name={self.name}, emoji={self.emoji})>"