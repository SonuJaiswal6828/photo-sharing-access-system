from pydantic import BaseModel
from datetime import datetime

class AccessRequestCreate(BaseModel):
    group_code : str
    group_password : str


class AccessRequestResponse(BaseModel):
    id : int
    request_code : str
    status : str
    expires_at : datetime
    requested_at : datetime


class PendingAccessRequestResponse(BaseModel):
    id : int
    group_id : int
    group_code : str
    request_code : str
    status : str
    requested_at : datetime
    expires_at : datetime