from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date) #(YYYY-MM-DD)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)
    hashed_password = Column(String)
    competition = Column(String)
    agreed_to_rules = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class Permission(Base):
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    competition_access = Column(String)
