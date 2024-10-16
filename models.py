from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey,
    UniqueConstraint,
    JSON,
    Text,
    DateTime,
    TypeDecorator,
)
from sqlalchemy.orm import relationship
from base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)  # (YYYY-MM-DD)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    competition = Column(String(255), nullable=True)  # Assuming this can be optional
    agreed_to_rules = Column(Boolean, default=False, nullable=False)
    team_signup = Column(Boolean, default=False)
    team_members = Column(JSON, nullable=True)
    team_member_emails = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    permissions = relationship(
        "Permission",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    repositories = relationship(
        'Repository',
        back_populates='user',
        cascade='all, delete-orphan'
    )

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    competition_access = Column(String(255), nullable=False)

    user = relationship("User", back_populates="permissions")

    __table_args__ = (
        UniqueConstraint('user_id', 'competition_access', name='uq_user_competition_access'),
    )


from datetime import datetime

class Repository(Base):
    __tablename__ = 'repositories'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    repository_name = Column(String(255), nullable=False)
    repository_url = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to the User model
    user = relationship('User', back_populates='repositories')

class JSONEncodedList(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
