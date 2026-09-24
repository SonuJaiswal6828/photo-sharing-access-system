from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from access_requests.schemas import AccessRequestCreate, AccessRequestResponse, PendingAccessRequestResponse, AccessRequestDetailResponse
from sessions.schemas import SessionResponse
from utils.dependencies import get_current_admin
from access_requests.controller import (
    create_access_request,
    get_pending_requests,
    approve_access_request,
    reject_access_request,
    get_request_detail
)

router = APIRouter()

@router.post("/create", response_model=AccessRequestResponse)
def create_access(request_data: AccessRequestCreate, db: Session = Depends(get_db)):
    return create_access_request(request_data, db)

@router.get("/pending", response_model=list[PendingAccessRequestResponse])
def control_request(db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return get_pending_requests(db, authorized)

@router.patch("/{request_id}/approve", response_model=SessionResponse)
def approve_request(request_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return approve_access_request(db, authorized, request_id)

@router.patch("/{request_id}/reject", response_model=AccessRequestResponse)
def reject_request(request_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return reject_access_request(db, authorized, request_id)

@router.get("/{request_id}", response_model=AccessRequestDetailResponse)
def get_request(request_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return get_request_detail(db, authorized, request_id)