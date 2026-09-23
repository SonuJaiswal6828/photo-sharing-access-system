from fastapi import FastAPI
from admin.router import router as admin_router
from groups.router import router as group_router
from sections.router import router as section_router
from photos.router import router as photo_router
from access_requests.router import router as access_requests_router
from sessions.router import router as session_router

app = FastAPI()

app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(group_router, prefix="/group", tags=["Group"])
app.include_router(section_router, prefix="/section", tags=["Section"])
app.include_router(photo_router, prefix="/photo", tags=["Photo"])
app.include_router(access_requests_router, prefix="/access-request", tags=["Access Request"])
app.include_router(session_router, prefix="/session", tags=["Session"])