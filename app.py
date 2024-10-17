from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, permissions, repositories
from database import engine, Base
import logging

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Include routers
app.include_router(users.router)
app.include_router(permissions.router)
app.include_router(repositories.router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the user management system"}

# Ensure all tables are created at startup
@app.on_event("startup")
async def startup_event():
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created!")
