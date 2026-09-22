from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router("/{session_id}")
def validate_session(session_id: int, db: Session = Depends(get_db)):
    return (session_id, db)