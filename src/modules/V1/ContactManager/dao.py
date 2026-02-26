from sqlalchemy import select
from .models import Contact
from app.database import create, update, fetch_one, fetch_all, delete_by_id

class ContactDAO:

    @staticmethod
    async def create_contact(contact: Contact) -> int:
        return await create(contact)

    @staticmethod
    async def update_contact(contact: Contact) -> int:
        return await update(contact)

    @staticmethod
    async def delete_contact(contact_id: int) -> None:
        await delete_by_id(Contact, contact_id)

    @staticmethod
    async def get_by_email_or_phone(email: str = None, phone_no: str = None):
        query = select(Contact)
        if email and phone_no:
            query = query.where((Contact.email == email) | (Contact.phone_no == phone_no))
        elif email:
            query = query.where(Contact.email == email)
        elif phone_no:
            query = query.where(Contact.phone_no == phone_no)
        else:
            return None
        return await fetch_one(query)

    @staticmethod
    async def filter(**filters):
        query = select(Contact)
        for key, value in filters.items():
            column = getattr(Contact, key, None)
            if column is not None:
                query = query.where(column == value)
        return await fetch_all(query)