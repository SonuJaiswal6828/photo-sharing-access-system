from fastapi import FastAPI
from admin.router import router as admin_router
from groups.router import router as group_router

app = FastAPI()

app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(group_router, prefix="/group", tags=["Group"])