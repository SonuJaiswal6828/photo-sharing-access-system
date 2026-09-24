import time
import os
import cloudinary.utils
from utils.cloudinary_config import cloudinary

from fastapi import HTTPException
from sqlalchemy.orm import Session
from photos.schemas import PhotoSave
from models.photo import Photo
from models.section import Section
from models.group import Group


def get_upload_signature():
    timestamp = int(time.time())
    
    signature = cloudinary.utils.api_sign_request(
        {"timestamp": timestamp},
        os.getenv("CLOUDINARY_API_SECRET")
    )
    
    return {
        "signature": signature,
        "timestamp": timestamp,
        "api_key": os.getenv("CLOUDINARY_API_KEY"),
        "cloud_name": os.getenv("CLOUDINARY_CLOUD_NAME")
    }

def save_photo(photo_data: PhotoSave, db: Session, admin_id: int):
    section = db.query(Section).filter(Section.id == photo_data.section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")

    group = db.query(Group).filter(Group.id == section.group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Section not found")

    if group.admin_id != admin_id:
        raise HTTPException(status_code=404, detail="Section not found")

    photo_object= Photo(section_id = photo_data.section_id, file_url = photo_data.file_url)
    db.add(photo_object)
    db.commit()
    db.refresh(photo_object)

    return photo_object

def delete_photo(photo_id: int, db: Session, admin_id: int):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")

    section = db.query(Section).filter(Section.id == photo.section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Photo not found")

    group = db.query(Group).filter(Group.id == section.group_id, Group.admin_id == admin_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Photo not found")

    db.delete(photo)
    db.commit()
    return {"detail": "Photo deleted successfully"}