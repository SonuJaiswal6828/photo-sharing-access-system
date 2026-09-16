from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from sections.schemas import SectionCreate, SectionResponse
from sections.controller import create_section
from utils.dependencies import get_current_admin

router = APIRouter()

@router.post("/create", response_model=SectionResponse)
def create(section_data: SectionCreate, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return create_section(section_data, db, authorized)