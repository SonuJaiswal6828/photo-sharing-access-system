from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from sessions.controller import session_status, revoke_session, get_session_photos, get_admin_sessions
from sessions.schemas import SessionStatusResponse, SessionResponse, SessionDetailResponse
from photos.schemas import PhotoResponse
from utils.dependencies import get_current_admin

router = APIRouter()

@router.get("/all", response_model=list[SessionDetailResponse])
def all_sessions(db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return get_admin_sessions(db, authorized)

@router.get("/{session_id}/status", response_model=SessionStatusResponse)
def status(session_id: int, db: Session = Depends(get_db)):
    return session_status(db, session_id)

@router.patch("/{session_id}/revoke", response_model=SessionResponse)
def revoked(session_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return revoke_session(db, authorized, session_id)

@router.get("/{session_token}/photos", response_model=list[PhotoResponse])
def session_photos(session_token: str, db: Session = Depends(get_db)):
    return get_session_photos(db, session_token)
