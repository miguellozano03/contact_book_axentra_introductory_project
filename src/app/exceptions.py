import traceback
from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from modules.V1.ContactManager.controller import ApiResponse

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        content = ApiResponse.error(
            message=exc.detail, 
            code=exc.status_code
        )
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        content = ApiResponse.error(
            message="Validation Error", 
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data={"errors": exc.errors()}
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        tb = traceback.format_exc()
        content = ApiResponse.error(
            message="Internal Server Error", 
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={"traceback": tb}
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content)