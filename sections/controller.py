from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.group import Group
from models.section import Section
from sections.schemas import SectionCreate

def create_section(section_data: SectionCreate, db: Session, admin_id: int):
    group = db.query(Group).filter(Group.id == section_data.group_id).first()

    if group is None or group.admin_id != admin_id:
        raise HTTPException(status_code=404, detail="Group  not found")

    section_object = Section(group_id = section_data.group_id, name = section_data.name)
    db.add(section_object)
    db.commit()
    db.refresh(section_object)

    return section_object