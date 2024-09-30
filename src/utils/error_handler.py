from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from starlette.requests import Request
from src.core.constants import DatabaseError
from src.utils.logger import logger
import logging

def create_sqlalchemy_error_responses(exception):
    message: str
    status_code: int
    if exception.orig.args[0] == DatabaseError.DuplicateEntry.value:
        status_code = 409
        if 'email' in str(exception.orig.args):
            message = "Email already exists"
        else:
            message = "Username already exists"
    else:
        message = "Unexpected error"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return [message], status_code

def create_validation_error_responses(exception):
    messages: list[str] = []

    for exc in exception.args[0]:
        messages.append(f"{exc.get('type')}: {exc.get('loc')[1]} {exc.get('msg')} in {exc.get('loc')[0]}")

    return messages


async def handle_all_exceptions(request:Request, exception:any) -> JSONResponse:
    messages:list = []
    status_code:int

    if isinstance(exception, StarletteHTTPException):
        messages.append(exception.detail)
        status_code = exception.status_code
    elif isinstance(exception, IntegrityError):
        messages, status_code = create_sqlalchemy_error_responses(exception)
    elif isinstance(exception, RequestValidationError):
        messages = create_validation_error_responses(exception)
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    else:
        messages = ["Unexpected error"]
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        log_message = f"{logging.getLevelName(logger.level)} - {request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {status_code} - error details: {exception}"
        logger.error(log_message)
    else:
        log_message = f"{logging.getLevelName(logger.level)} - {request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {status_code} - error details: {messages}"
        logger.error(log_message)

    error_data: dict = {'error': {'code': status_code, 'messages': messages}}
    return JSONResponse(content=error_data, status_code=status_code)


def register_error_handlers(app:FastAPI):
    app.add_exception_handler(StarletteHTTPException, handle_all_exceptions)
    app.add_exception_handler(SQLAlchemyError, handle_all_exceptions)
    app.add_exception_handler(RequestValidationError, handle_all_exceptions)
    app.add_exception_handler(NotImplementedError, handle_all_exceptions)
    app.add_exception_handler(Exception, handle_all_exceptions)