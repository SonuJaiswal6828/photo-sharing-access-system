from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from groups.schemas import GroupCreate, GroupResponse, GroupUpdate
from sections.schemas import SectionResponse
from groups.controller import create_group, get_admin_groups, get_group_sections, update_group, delete_group
from utils.dependencies import get_current_admin


router = APIRouter()

@router.post("/create", response_model=GroupResponse)
def create(group_data: GroupCreate, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin) ):
    return create_group(group_data, db, authorized)

@router.get("/", response_model=list[GroupResponse])
def list_groups(db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return get_admin_groups(authorized, db)

@router.get("/{group_id}/sections", response_model=list[SectionResponse])
def list_group_sections(group_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return get_group_sections(group_id, authorized, db)

@router.patch("/{group_id}", response_model=GroupResponse)
def edit_group(group_id: int, group_data: GroupUpdate, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return update_group(group_id, group_data, db, authorized)

@router.delete("/{group_id}")
def remove_group(group_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return delete_group(group_id, db, authorized)