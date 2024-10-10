from fastapi import FastAPI
from routers import users, permissions

app = FastAPI()

# Register the routers
app.include_router(users.router)
app.include_router(permissions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the user management system"}
