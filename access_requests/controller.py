from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from access_requests.schemas import AccessRequestCreate
from models.access_request import AccessRequest
from models.group import Group
from utils.security import verify_password
from utils.code_generator import generate_random_code
from datetime import datetime , timedelta
from models.session import Session as UserSession

def generate_unique_request_code(db : Session)-> str:
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
        raise HTTPException(status_code=401, detail="Invalid Group code or Password")

    request_code = generate_unique_request_code(db)

    expires_at = datetime.now() + timedelta(minutes=60)

    request_object = AccessRequest(group_id = existing.id, request_code = request_code, expires_at = expires_at)
    db.add(request_object)
    db.commit()
    db.refresh(request_object)

    return request_object

def get_pending_requests(db: Session, admin_id):
    requests =( db.query(AccessRequest, Group)
               .join(Group, AccessRequest.group_id == Group.id)
               .filter(
                   Group.admin_id == admin_id,
                   AccessRequest.status == "pending"
               ).all())
    result = []
    for request, group in requests:
        result.append({
            "id": request.id,
            "group_id": request.group_id,
            "group_code": group.group_code,
            "request_code": request.request_code,
            "status": request.status,
            "requested_at": request.requested_at,
            "expires_at": request.expires_at
        })

    return result

def approve_access_request(db: Session, admin_id: int, request_id: int):
    existing = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Request not exist")

    if existing.status != "pending":
        raise HTTPException(status_code=400, detail="Request is not pending")

    group = db.query(Group).filter(Group.id == existing.group_id, Group.admin_id == admin_id).first()
    if not group:
        raise HTTPException(status_code=403, detail="You are not authorized to approve this request")

    if existing.expires_at <= datetime.now():
        raise HTTPException(status_code=400, detail="Access request has expire")

    existing.status = "approved"

    session = UserSession(request_id = existing.id, expire_time = existing.expires_at)

    db.add(session)
    db.commit()
    db.refresh(session)

    return session