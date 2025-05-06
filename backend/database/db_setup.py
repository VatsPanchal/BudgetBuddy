import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Determine environment
if os.getenv("GAE_ENV", "").startswith("standard"):
    # Running on Google App Engine
    DB_PATH = "/tmp/budget_buddy.db"
    ORIGINAL_DB_PATH = "./budget_buddy.db"
    if not os.path.exists(DB_PATH) and os.path.exists(ORIGINAL_DB_PATH):
        shutil.copyfile(ORIGINAL_DB_PATH, DB_PATH)
else:
    # Running locally
    DB_PATH = "./budget_buddy.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
