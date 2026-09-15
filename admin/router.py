from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from admin.schemas import AdminCreate, AdminResponse, AdminLogin
from admin.controller import create_admin, login_admin

router = APIRouter()

@router.post("/signup", response_model=AdminResponse)
def signup(admin_data: AdminCreate, db: Session = Depends(get_db)):
    return create_admin(admin_data, db)

@router.post("/login", response_model=AdminResponse)
def login(admin_data: AdminLogin, db: Session = Depends(get_db)):
    return login_admin(admin_data, db)