from database import engine, Base
from models.admin import Admin
from models.group import Group
from models.section import Section
from models.photo import Photo
from models.access_request import AccessRequest
from models.session import Session

Base.metadata.create_all(engine)