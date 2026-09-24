from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionResponse(BaseModel):
    id: int
    request_id: int
    session_token: str
    created_at: datetime
    expire_time: datetime
    revoked_at: Optional[datetime]

    class Config:
        from_attributes = True

class SessionStatusResponse(BaseModel):
    status: str

class SessionDetailResponse(BaseModel):
    id: int
    session_token: str
    request_code: str
    group_code: str
    group_name: str
    created_at: datetime
    expire_time: datetime
    revoked_at: Optional[datetime]
    status: str

    class Config:
        from_attributes = True