from pydantic import BaseModel, EmailStr, Field, HttpUrl
from datetime import datetime, date
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
    team_member_emails: Optional[List[EmailStr]] = Field(
        None, example=["alice@example.com", "bob@example.com", "charlie@example.com"]
    )
    
# Repository Schemas
class RepositoryBase(BaseModel):
    repository_name: str = Field(..., example="my-awesome-repo")
    repository_url: HttpUrl = Field(..., example="https://github.com/username/my-awesome-repo")
    description: Optional[str] = Field(None, example="A description of the repository.")

class RepositoryCreate(RepositoryBase):
    pass

class RepositoryUpdate(BaseModel):
    repository_name: Optional[str] = Field(None, example="my-updated-repo")
    repository_url: Optional[HttpUrl] = Field(None, example="https://github.com/username/my-updated-repo")
    description: Optional[str] = Field(None, example="An updated description.")

class RepositoryResponse(RepositoryBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

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
    team_member_emails: Optional[List[EmailStr]]
    is_active: bool
    is_superuser: bool
    repositories: List[RepositoryResponse] = []

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
