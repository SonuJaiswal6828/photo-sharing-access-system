from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from access_requests.schemas import AccessRequestCreate
from models.access_request import AccessRequest
from models.group import Group
from models.session import Session as UserSession
from utils.security import verify_password
from utils.code_generator import generate_random_code
from sessions.controller import generate_unique_session_token
from datetime import datetime, timedelta

def generate_unique_request_code(db: Session) -> str:
    while True:
        code = generate_random_code(4, False)
        existing = db.query(AccessRequest).filter(AccessRequest.request_code == code, AccessRequest.status == "pending").first()
        if existing is None:
            return code

def create_access_request(request_data: AccessRequestCreate, db: Session):
    existing = db.query(Group).filter(Group.group_code == request_data.group_code).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Invalid Group code or Password")

    isValid_user = verify_password(request_data.group_password, existing.password_hash)
    if not isValid_user:
        raise HTTPException(status_code=404, detail="Invalid Group code or Password")

    request_code = generate_unique_request_code(db)
    expires_at = datetime.utcnow() + timedelta(minutes=60)

    request_object = AccessRequest(group_id=existing.id, request_code=request_code, expires_at=expires_at)
    db.add(request_object)
    db.commit()
    db.refresh(request_object)
    return request_object

def get_pending_requests(db: Session, admin_id):
    requests = (db.query(AccessRequest, Group)
                .join(Group, AccessRequest.group_id == Group.id)
                .filter(Group.admin_id == admin_id, AccessRequest.status == "pending")
                .all())
    result = []
    for request, group in requests:
        result.append({
            "id": request.id, "group_id": request.group_id, "group_code": group.group_code,
            "request_code": request.request_code, "status": request.status,
            "requested_at": request.requested_at, "expires_at": request.expires_at
        })
    return result

def approve_access_request(db: Session, admin_id: int, request_id: int):
    existing = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Request not found")

    group = db.query(Group).filter(Group.id == existing.group_id, Group.admin_id == admin_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Request not found")

    if existing.status != "pending":
        raise HTTPException(status_code=400, detail="Request is not pending")

    if existing.expires_at <= datetime.now():
        raise HTTPException(status_code=400, detail="Access request has expired")

    existing.status = "approved"
    session_token = generate_unique_session_token(db)
    session = UserSession(request_id=existing.id, session_token=session_token, expire_time=datetime.now() + timedelta(hours=1))

    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_request_status(db: Session, request_code: str):
    request = (db.query(AccessRequest)
               .filter(AccessRequest.request_code == request_code)
               .order_by(AccessRequest.requested_at.desc())
               .first())
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.status == "approved":
        session = db.query(UserSession).filter(UserSession.request_id == request.id).first()
        return {"status": "approved", "session_token": session.session_token if session else None}

    return {"status": request.status}

def cleanup_expired_requests(db: Session):
    expired = db.query(AccessRequest).filter(
        AccessRequest.status == "pending",
        AccessRequest.expires_at <= datetime.now()
    ).all()
    for req in expired:
        req.status = "expired"
    if expired:
        db.commit()

def get_pending_requests(db: Session, admin_id):
    cleanup_expired_requests(db)
    requests = (db.query(AccessRequest, Group)
               .join(Group, AccessRequest.group_id == Group.id)
               .filter(
                   Group.admin_id == admin_id,
                   AccessRequest.status == "pending"
               ).all())
    result = []
    for request, group in requests:
        result.append({
            "id": request.id, "group_id": request.group_id, "group_code": group.group_code,
            "request_code": request.request_code, "status": request.status,
            "requested_at": request.requested_at, "expires_at": request.expires_at
        })
    return result
