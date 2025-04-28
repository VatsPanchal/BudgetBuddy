from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import user as user_routes

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Register user routes
app.include_router(user_routes.router)

# CORS middleware configuration
origins = [
    "http://localhost:8080",  # Vue development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)