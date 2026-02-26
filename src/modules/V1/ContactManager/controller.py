from typing import Any, Dict, Optional
from .services import ContactService
from .schemas import ContactBase

class ApiResponse:
    @staticmethod
    def success(data: Any = None, message: str = "OK", code: int = 200):
        return {
            "status": "success",
            "code": code,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message: str = "Error", code: int = 400, data: Any = None):
        return {
            "status": "error",
            "code": code,
            "message": message,
            "data": data
        }
    
class ContactController:
    @staticmethod
    async def get_all():
        result, code = await ContactService.filter({})
        return ApiResponse.success(result, "Fetched successfully", code)

    @staticmethod
    async def create(contact_data: ContactBase):
        result, code = await ContactService.save(contact_data)
        return ApiResponse.success(result, "Created successfully", code)

    @staticmethod
    async def update(contact_id: int, contact_data: ContactBase):
        result, code = await ContactService.update(contact_id, contact_data)
        
        return ApiResponse.success(result, "Updated successfully", code)

    @staticmethod
    async def delete(contact_id: int):
        result, code = await ContactService.delete(contact_id)
        return ApiResponse.success(result, "Deleted successfully", code)