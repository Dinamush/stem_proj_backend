from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    email: EmailStr
    phone_number: str
    password: str
    competition: str
    agreed_to_rules: bool

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: date
    competition: str
    agreed_to_rules: bool
    is_active: bool

    class Config:
        orm_mode = True
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

