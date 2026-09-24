from sqlalchemy.orm import Session
from fastapi import HTTPException
from groups.schemas import GroupCreate
from models.group import Group
from models.section import Section
from utils.security import hash_password
from utils.code_generator import generate_random_code

def generate_unique_group_code(db : Session)-> str:
    while True:
        code = generate_random_code(6)
        existing = db.query(Group.group_code).filter(Group.group_code == code).first()
        if existing is None:
            return code

def create_group(group_data: GroupCreate, db: Session, admin_id):
    password = group_data.password
    password_hash = hash_password(password)

    group_code = generate_unique_group_code(db)

    group_object = Group(admin_id = admin_id, group_code = group_code, name = group_data.name, password_hash = password_hash)
    db.add(group_object)
    db.commit()
    db.refresh(group_object)

    return group_object

def get_admin_groups(admin_id: int, db: Session):
    groups = db.query(Group).filter(Group.admin_id == admin_id).all()
    return groups

def get_group_sections(group_id: int, admin_id: int, db: Session):
    group = db.query(Group).filter(Group.id == group_id).first()

    if group is None or group.admin_id != admin_id:
        raise HTTPException(status_code=404, detail="Group not found")

    sections = db.query(Section).filter(Section.group_id == group_id).all()
    return sections