from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.session import Session as UserSession
from models.access_request import AccessRequest
from models.group import Group
from datetime import datetime

def validate(session_id: int, db: Session):
    existing = db.query(UserSession).filter(UserSession.id == session_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Session not found")

    if existing.revoked_at is not None:
        raise HTTPException(status_code=401, detail="Session has been revoked")

    if existing.expire_time <= datetime.now():
        raise HTTPException(status_code=401, detail="Session has expired")

    request = db.query(AccessRequest).filter(AccessRequest.id == existing.request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Access request not found")

    group = db.query(Group).filter(Group.id == request.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return existing, group