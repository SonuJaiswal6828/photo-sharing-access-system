from sqlalchemy.orm import Session
from models.admin import Admin
from admin.schemas import AdminCreate, AdminLogin
from utils.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException

def create_admin(admin_data: AdminCreate, db: Session):
    password= admin_data.password
    hash_pass = hash_password(password)

    admin_object = Admin(username = admin_data.username, password_hash = hash_pass)
    db.add(admin_object)
    db.commit()
    db.refresh(admin_object)

    return admin_object

def login_admin(admin_data: AdminLogin, db: Session):
    user = db.query(Admin).filter(Admin.username == admin_data.username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    valid_user = verify_password(admin_data.password, user.password_hash)

    if not valid_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"admin_id": user.id})

    return {"access_token": token, "token_type": "bearer"}