from fastapi import FastAPI
from routers import users, permissions
from database import engine, Base

app = FastAPI()

# Register the routers
app.include_router(users.router)
app.include_router(permissions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the user management system"}

@app.get("/users/")
def get_users():
    return {"message": "Here are the users"}

# Ensure all tables are created at startup
@app.on_event("startup")
def startup():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")