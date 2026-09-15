from pydantic import BaseModel
from datetime import datetime

class AdminCreate(BaseModel):
    username : str
    password : str

class AdminResponse(BaseModel):
    id : int
    username : str
    created_at : datetime
    
    class Config:
        from_attributes = True