from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from database import Base

class Section(Base):
    __tablename__ = "sections"

    id =Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    __table_args__  = (UniqueConstraint("group_id", "name"),)
