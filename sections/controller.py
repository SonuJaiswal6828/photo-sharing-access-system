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

def update_section(section_id: int, section_data, db: Session, admin_id: int):
    section = db.query(Section).filter(Section.id == section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")

    group = db.query(Group).filter(Group.id == section.group_id, Group.admin_id == admin_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Section not found")

    section.name = section_data.name
    db.commit()
    db.refresh(section)
    return section

def delete_section(section_id: int, db: Session, admin_id: int):
    section = db.query(Section).filter(Section.id == section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")

    group = db.query(Group).filter(Group.id == section.group_id, Group.admin_id == admin_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Section not found")

    db.delete(section)
    db.commit()
    return {"detail": "Section deleted successfully"}