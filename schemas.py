from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    email: EmailStr  # Changed to EmailStr for email validation
    password: str
    phone_number: str
    competition: str  # Updated from bool to str to match the model
    agreed_to_rules: bool

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
