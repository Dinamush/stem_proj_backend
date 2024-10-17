# routers/repositories.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import Repository
from models import User
from schemas import RepositoryCreate, RepositoryUpdate, RepositoryResponse
from database import get_db
from auth import get_current_user

router = APIRouter(
    prefix="/repositories",
    tags=["repositories"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=RepositoryResponse, status_code=status.HTTP_201_CREATED)
def create_repository(
    repository: RepositoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if the repository URL already exists for the user
    existing_repo = db.query(Repository).filter(
        Repository.user_id == current_user.id,
        Repository.repository_url == repository.repository_url
    ).first()
    if existing_repo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Repository already exists."
        )
    db_repository = Repository(
        user_id=current_user.id,
        repository_name=repository.repository_name,
        repository_url=repository.repository_url,
        description=repository.description,
    )
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository

@router.get("/", response_model=List[RepositoryResponse])
def get_user_repositories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repositories = db.query(Repository).filter(Repository.user_id == current_user.id).all()
    return repositories

@router.get("/{repository_id}", response_model=RepositoryResponse)
def get_repository(
    repository_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = db.query(Repository).filter(
        Repository.id == repository_id,
        Repository.user_id == current_user.id
    ).first()
    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found."
        )
    return repository

@router.put("/{repository_id}", response_model=RepositoryResponse)
def update_repository(
    repository_id: int,
    repository_update: RepositoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = db.query(Repository).filter(
        Repository.id == repository_id,
        Repository.user_id == current_user.id
    ).first()
    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found."
        )
    for key, value in repository_update.dict(exclude_unset=True).items():
        setattr(repository, key, value)
    db.commit()
    db.refresh(repository)
    return repository

@router.delete("/{repository_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repository(
    repository_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = db.query(Repository).filter(
        Repository.id == repository_id,
        Repository.user_id == current_user.id
    ).first()
    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found."
        )
    db.delete(repository)
    db.commit()
    return None
