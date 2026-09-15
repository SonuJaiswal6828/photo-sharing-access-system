from fastapi import FastAPI
from admin.router import router as admin_router

app = FastAPI()

app.include_router(admin_router, prefix="/admin", tags=["Admin"])