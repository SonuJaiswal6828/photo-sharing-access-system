from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    file_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.now)