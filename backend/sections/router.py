from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from sections.schemas import SectionCreate, SectionResponse, SectionUpdate
from photos.schemas import PhotoResponse
from sections.controller import create_section, update_section, delete_section, get_section_photos
from utils.dependencies import get_current_admin

router = APIRouter()

@router.post("/create", response_model=SectionResponse)
def create(section_data: SectionCreate, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return create_section(section_data, db, authorized)

@router.patch("/{section_id}", response_model=SectionResponse)
def edit_section(section_id: int, section_data: SectionUpdate, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return update_section(section_id, section_data, db, authorized)

@router.delete("/{section_id}")
def remove_section(section_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return delete_section(section_id, db, authorized)

@router.get("/{section_id}/photos", response_model=list[PhotoResponse])
def list_section_photos(section_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return get_section_photos(section_id, db, authorized)