from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from common.exceptions import BaseAppException
from common.dto.response import error_response

def setup_exception_handlers(app: FastAPI):
    """
    Register global exception handlers for the FastAPI application.
    """

    @app.exception_handler(BaseAppException)
    async def custom_app_exception_handler(request: Request, exc: BaseAppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(message=exc.message, error=exc.error_details, status_code=exc.status_code)
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(message=str(exc.detail), status_code=exc.status_code)
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=error_response(message="Internal Server Error", error=str(exc), status_code=500)
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=error_response(message="Validation Error", error=str(exc.errors()), status_code=422)
        )
