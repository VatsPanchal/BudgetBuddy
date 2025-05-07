from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db_setup import engine, Base
from routes import auth, budget, profile

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budget Buddy API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Local development
        "https://budget-buddy-frontend-ip.nip.io",  # Cloud CDN URL
        "https://budget-buddy-frontend-ip.nip.io:443"  # Cloud CDN URL with port
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Add headers middleware
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin", "http://localhost:8080")
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(budget.router, prefix="/api/budget", tags=["budget"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"])

@app.get("/")
async def root():
    return {"message": "Welcome to Budget Buddy API"} 