from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from photos.schemas import PhotoSave, PhotoResponse
from database import get_db
from utils.dependencies import get_current_admin
from photos.controller import save_photo, get_upload_signature, delete_photo

router = APIRouter()

@router.get("/get-upload-signature")
def create_signature(authorized: int = Depends(get_current_admin)):
    return get_upload_signature()

@router.post("/save_photo", response_model=PhotoResponse)
def save(photo_data: PhotoSave, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return save_photo(photo_data, db, authorized)

@router.delete("/{photo_id}")
def remove_photo(photo_id: int, db: Session = Depends(get_db), authorized: int = Depends(get_current_admin)):
    return delete_photo(photo_id, db, authorized)