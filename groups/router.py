from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from groups.schemas import GroupCreate, GroupResponse
from groups.controller import create_group

router = APIRouter()

@router.post("/create", response_model=GroupResponse)
def create(group_data: GroupCreate, db: Session = Depends(get_db)):
    return create_group(group_data, db)