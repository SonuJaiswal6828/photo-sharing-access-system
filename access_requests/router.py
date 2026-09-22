from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from access_requests.schemas import AccessRequestCreate, AccessRequestResponse, PendingAccessRequestResponse
from utils.dependencies import get_current_admin
from access_requests.controller import create_access_request, get_pending_requests

router = APIRouter()

@router.post("/create", response_model=AccessRequestResponse)
def create_access(request_data: AccessRequestCreate, db: Session = Depends(get_db)):
    return create_access_request(request_data, db)

@router.get("/pending", response_model=list[PendingAccessRequestResponse])
def control_request(db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return get_pending_requests(db, authorized)