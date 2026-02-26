from .schemas import ContactBase, ContactRead
from .models import Contact
from .dao import ContactDAO
from typing import Optional, Dict, Any, List

class ContactService:

    @staticmethod
    async def save(contact: ContactBase) -> tuple[Dict[str, Any], int]:
        existing = await ContactDAO.get_by_email_or_phone(contact.email, contact.phone_no)
        contact_model = Contact(**contact.model_dump(exclude_unset=True))

        if existing:
            contact_model.id = existing.id
            id_ = await ContactDAO.update_contact(contact_model)
        else:
            id_ = await ContactDAO.create_contact(contact_model)
        return {"id": id_}, 200

    @staticmethod
    async def filter(filters: Optional[Dict[str, Any]] = None) -> tuple[List[Dict[str, Any]], int]:
        contacts = await ContactDAO.filter(**(filters or {}))

        result = [ContactRead.model_validate(c).model_dump() for c in contacts]
        return result, 200

    @staticmethod
    async def update(contact_id: int, contact: ContactBase) -> tuple[Dict[str, Any], int]:
        data = contact.model_dump(exclude_unset=True)

        data["id"] = contact_id
        
        contact_model = Contact(**data)
        id_ = await ContactDAO.update_contact(contact_model)
        return {"id": id_}, 200

    @staticmethod
    async def delete(contact_id: int) -> tuple[Dict[str, Any], int]:
        await ContactDAO.delete_contact(contact_id)
        return {"id": contact_id}, 200