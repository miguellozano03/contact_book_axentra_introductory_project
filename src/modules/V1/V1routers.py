from fastapi import APIRouter
from modules.V1.ContactManager.routers import router as contact_router

router = APIRouter()

router.include_router(contact_router, prefix="/contacts", tags=["contact_manager"])