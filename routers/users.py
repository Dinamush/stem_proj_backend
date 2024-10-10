from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_password_hash, verify_password, create_access_token
from models import User
from database import get_db
from schemas import UserCreate, UserResponse
from datetime import timedelta
from schemas import UserLogin, Token

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        birth_date=user.birth_date,
        email=user.email,
        hashed_password=hashed_password,
        phone_number=user.phone_number,
        competition=user.competition,
        agreed_to_rules=user.agreed_to_rules
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}
