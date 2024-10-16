from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    birth_date: date = Field(..., example="1990-01-01")
    email: EmailStr = Field(..., example="john.doe@example.com")
    phone_number: str = Field(..., example="1234567890")
    competition: Optional[str] = Field(None, example="Competition Name")
    agreed_to_rules: bool = Field(..., example=True)
    team_signup: bool = Field(..., example=True)
    team_members: Optional[List[str]] = Field(
        None, example=["Alice Smith", "Bob Johnson", "Charlie Lee"]
    )

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="strongpassword")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=8, example="strongpassword")

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    competition: Optional[str]
    agreed_to_rules: bool
    team_signup: bool
    team_members: Optional[List[str]]
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: EmailStr

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

# Permission Schemas
class PermissionBase(BaseModel):
    user_id: int
    competition_access: str = Field(..., example="Competition A")

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        orm_mode = True
