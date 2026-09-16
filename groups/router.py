from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from groups.schemas import GroupCreate, GroupResponse
from groups.controller import create_group
from utils.dependencies import get_current_admin

router = APIRouter()

@router.post("/create", response_model=GroupResponse)
def create(group_data: GroupCreate, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin) ):
    return create_group(group_data, db, authorized)