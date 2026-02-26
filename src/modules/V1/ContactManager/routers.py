from fastapi import APIRouter
from .controller import ContactController
from .schemas import ContactBase

router = APIRouter()

@router.post("/")
async def create_contact(contact: ContactBase):
    return await ContactController.create(contact)

@router.get("/")
async def list_contacts():
    return await ContactController.get_all()

@router.put("/{contact_id}")
async def update_contact(contact_id: int, contact: ContactBase):
    return await ContactController.update(contact_id, contact)

@router.delete("/{contact_id}")
async def delete_contact(contact_id: int):
    return await ContactController.delete(contact_id)