from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.session import Session as UserSession
from models.access_request import AccessRequest
from models.group import Group
from models.section import Section
from models.photo import Photo
from datetime import datetime

def session_status(db: Session, session_id: int):
    existing = db.query(UserSession).filter(UserSession.id == session_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Session not found")

    current = {"status" : "active"}

    if existing.revoked_at is not None:
        current["status"] = "revoked" 
    elif datetime.now()>existing.expire_time:
        current["status"] = "expired" 
 
    return current


def revoke_session(db: Session, admin_id: int, session_id: int):
    session = db.query(UserSession).filter(UserSession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    request = db.query(AccessRequest).filter(AccessRequest.id == session.request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Session not found")

    group = db.query(Group).filter(Group.id == request.group_id, Group.admin_id == admin_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session.revoked_at = datetime.now()
    db.commit()
    db.refresh(session)
    return session


def get_session_photos(db: Session, session_id: int):
    session = db.query(UserSession).filter(UserSession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.revoked_at is not None:
        raise HTTPException(status_code=403, detail="Session revoked")

    if datetime.now() > session.expire_time:
        raise HTTPException(status_code=403, detail="Session expired")

    request = db.query(AccessRequest).filter(AccessRequest.id == session.request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Session not found")

    section_ids = db.query(Section.id).filter(Section.group_id == request.group_id).all()
    section_ids = [s[0] for s in section_ids]

    photos = db.query(Photo).filter(Photo.section_id.in_(section_ids)).all()
    return photos
    
