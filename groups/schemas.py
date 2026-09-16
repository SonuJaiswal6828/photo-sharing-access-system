from pydantic import BaseModel
from datetime import datetime

class GroupCreate(BaseModel):
    admin_id : int
    name : str
    password : str

class GroupResponse(BaseModel):
    id: int
    group_code: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True