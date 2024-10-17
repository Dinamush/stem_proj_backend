from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)
from models import User
from database import get_db
from schemas import UserCreate, UserResponse, UserLogin, Token
from datetime import timedelta
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
import logging
from jose import JWTError
from pydantic import EmailStr


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Set up logging
logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency for OAuth2 authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWTError: {e}")
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        birth_date=user.birth_date,
        email=user.email,
        hashed_password=hashed_password,
        phone_number=user.phone_number,
        competition=user.competition,
        agreed_to_rules=user.agreed_to_rules,
        team_signup=user.team_signup,
        team_members=user.team_members,
        team_member_emails=user.team_member_emails,
        is_active=True,
        is_superuser=False
    )
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not save user due to a database error"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return db_user


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "email": db_user.email
    }


@router.get("/retrieve", response_model=List[UserResponse])
def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    logger.debug(f"Retrieved users: {users}")
    return users


@router.get("/retrieve_debug", response_model=List[UserResponse])
def get_all_users_debug(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    # Convert each user object to a dictionary for readable output
    users_dicts = [user.__dict__.copy() for user in users]
    for user_dict in users_dicts:
        user_dict.pop('_sa_instance_state', None)

    logger.debug(f"Retrieved users: {users_dicts}")
    return users

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "email": db_user.email
    }