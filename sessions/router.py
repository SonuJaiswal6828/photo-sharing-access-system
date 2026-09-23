from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from sessions.controller import session_status, revoke_session
from sessions.schemas import SessionStatusResponse, SessionResponse
from utils.dependencies import get_current_admin

router = APIRouter()

@router.get("/{session_id}/status", response_model=SessionStatusResponse)
def status(session_id: int, db: Session = Depends(get_db)):
    return session_status(db, session_id)

@router.patch("/{session_id}/revoke", response_model=SessionResponse)
def revoked(session_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return revoke_session(db, authorized, session_id)