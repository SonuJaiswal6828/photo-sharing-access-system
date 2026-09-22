from pydantic import BaseModel
from datetime import datetime

class PhotoSave(BaseModel):
    section_id : int
    file_url : str

class PhotoResponse(BaseModel):
    id : int
    section_id : int
    file_url : str
    uploaded_at : datetime

    class Config:
        from_attributes = True