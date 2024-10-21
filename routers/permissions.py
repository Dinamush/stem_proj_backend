from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import Permission, User
from auth import get_current_user
from schemas import PermissionCreate, PermissionResponse
from typing import List

# Ensure that get_current_user is imported from auth.py and uses the updated oauth2_scheme


router = APIRouter(
    prefix="/permissions",
    tags=["permissions"]
)

@router.post("/assign", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def assign_permission(
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if current user is a superuser
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Check if the user exists
    user = db.query(User).filter(User.id == permission_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if the permission already exists
    existing_permission = db.query(Permission).filter(
        Permission.user_id == permission_data.user_id,
        Permission.competition_access == permission_data.competition_access
    ).first()
    if existing_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission already assigned"
        )

    # Create new permission
    permission = Permission(
        user_id=permission_data.user_id,
        competition_access=permission_data.competition_access
    )
    db.add(permission)
    try:
        db.commit()
        db.refresh(permission)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not assign permission due to database error"
        )

    return permission

@router.get("/", response_model=List[PermissionResponse])
def get_permissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only superusers can view all permissions
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    permissions = db.query(Permission).offset(skip).limit(limit).all()
    return permissions

@router.get("/user/{user_id}", response_model=List[PermissionResponse])
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # A user can view their own permissions, or superuser can view any
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    permissions = db.query(Permission).filter(Permission.user_id == user_id).all()
    return permissions

@router.delete("/revoke", response_model=PermissionResponse)
def revoke_permission(
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only superusers can revoke permissions
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    permission = db.query(Permission).filter(
        Permission.user_id == permission_data.user_id,
        Permission.competition_access == permission_data.competition_access
    ).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    db.delete(permission)
    db.commit()
    return permission
