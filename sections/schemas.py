from pydantic import BaseModel
from datetime import datetime

class SectionCreate(BaseModel):
    group_id : int
    name : str

class SectionResponse(BaseModel):
    id : int
    group_id : int
    name : str
    created_at : datetime

    class Config:
        from_attributes = True