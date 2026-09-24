from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from datetime import datetime
from database import Base

class AccessRequest(Base):
    __tablename__ = "access_requests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    request_code = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    requested_at = Column(DateTime, nullable=False, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)

    __table_args__ = (
    Index(
        "uq_pending_request_code",
        "request_code",
        unique=True,
        postgresql_where=(status == "pending")
    ),
)