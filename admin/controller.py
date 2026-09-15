from sqlalchemy.orm import Session
from models.admin import Admin
from admin.schemas import AdminCreate, AdminResponse
from utils.security import hash_password, verify_password

def create_admin(admin_data: AdminCreate, db: Session):
    password= admin_data.password
    hash_pass = hash_password(password)

    admin_object = Admin(username = admin_data.username, password_hash = hash_pass)
    db.add(admin_object)
    db.commit()
    db.refresh(admin_object)

    return admin_object