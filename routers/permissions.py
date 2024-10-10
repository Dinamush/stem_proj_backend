from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Permission

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"]
)

@router.post("/assign")
def assign_permission(user_id: int, competition_access: str, db: Session = Depends(get_db)):
    permission = Permission(user_id=user_id, competition_access=competition_access)
    db.add(permission)
    db.commit()
    return {"message": "Permission assigned successfully"}
