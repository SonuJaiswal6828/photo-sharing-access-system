from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.session import Session as UserSession
from models.access_request import AccessRequest
from models.group import Group
from models.section import Section
from models.photo import Photo
from utils.code_generator import generate_random_code
from datetime import datetime, timezone

def generate_unique_session_token(db: Session) -> str:
    while True:
        token = generate_random_code(32)
        existing = db.query(UserSession).filter(UserSession.session_token == token).first()
        if existing is None:
            return token

def session_status(db: Session, session_id: int):
    existing = db.query(UserSession).filter(UserSession.id == session_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Session not found")

    current = {"status": "active"}
    if existing.revoked_at is not None:
        current["status"] = "revoked"
    elif datetime.now(timezone.utc) > existing.expire_time:
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

    session.revoked_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    return session

def get_session_photos(db: Session, session_token: str):
    session = db.query(UserSession).filter(UserSession.session_token == session_token).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.revoked_at is not None:
        raise HTTPException(status_code=403, detail="Session revoked")

    if datetime.now(timezone.utc) > session.expire_time:
        raise HTTPException(status_code=403, detail="Session expired")

    request = db.query(AccessRequest).filter(AccessRequest.id == session.request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Session not found")

    section_ids = db.query(Section.id).filter(Section.group_id == request.group_id).all()
    section_ids = [s[0] for s in section_ids]

    photos = db.query(Photo).filter(Photo.section_id.in_(section_ids)).all()
    return photos

def update_section(section_id: int, section_data, db: Session, admin_id: int):
    section = db.query(Section).filter(Section.id == section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")

    group = db.query(Group).filter(Group.id == section.group_id, Group.admin_id == admin_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Section not found")

    section.name = section_data.name
    db.commit()
    db.refresh(section)
    return section

def delete_section(section_id: int, db: Session, admin_id: int):
    section = db.query(Section).filter(Section.id == section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")

    group = db.query(Group).filter(Group.id == section.group_id, Group.admin_id == admin_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Section not found")

    db.delete(section)
    db.commit()
    return {"detail": "Section deleted successfully"}

def get_admin_sessions(db: Session, admin_id: int):
    results = (
        db.query(UserSession, AccessRequest, Group)
        .join(AccessRequest, UserSession.request_id == AccessRequest.id)
        .join(Group, AccessRequest.group_id == Group.id)
        .filter(Group.admin_id == admin_id)
        .order_by(UserSession.created_at.desc())
        .all()
    )
    now = datetime.now(timezone.utc)
    sessions = []
    for s, req, grp in results:
        if s.revoked_at is not None:
            status = "revoked"
        elif now > s.expire_time:
            status = "expired"
        else:
            status = "active"
        sessions.append({
            "id": s.id,
            "session_token": s.session_token,
            "request_code": req.request_code,
            "group_code": grp.group_code,
            "group_name": grp.name,
            "created_at": s.created_at,
            "expire_time": s.expire_time,
            "revoked_at": s.revoked_at,
            "status": status,
        })
    return sessions
