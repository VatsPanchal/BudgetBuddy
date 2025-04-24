from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, username: str, email: str, hashed_password: str, first_name: str, last_name: str, phone: float):
    db_user = User(username=username, email=email, password=hashed_password, first_name=first_name, last_name=last_name, phone=phone, income=0, savings=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

