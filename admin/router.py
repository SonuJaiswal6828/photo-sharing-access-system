from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from admin.schemas import AdminCreate, AdminResponse
from admin.controller import create_admin

router = APIRouter()

@router.post("/signup", response_model=AdminResponse)
def signup(admin_data: AdminCreate, db: Session = Depends(get_db)):
    return create_admin(admin_data, db)