from fastapi import FastAPI
from app.database import init_db
from app.api import user_routes

app = FastAPI()

# Initialize the database
init_db()

# Include the routes for the API
app.include_router(user_routes.router)
