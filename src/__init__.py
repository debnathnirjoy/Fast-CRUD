from http.client import HTTPException
from typing import Callable

from fastapi import FastAPI
from src.db.models.user import User
from src.db.database import engine, Base
from src.routes.user import user_router
from src.middlewares.logger import register_logger
from src.utils.custom_response import CustomResponse


from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError
from src.utils.error_handler import register_error_handlers

Base.metadata.create_all(bind=engine)


TITLE = "Fast CRUD"
DESCRIPTION = "Basic CRUD for users using FastAPI"
VERSION = "v1"
VERSION_PREFIX = f"/api/{VERSION}"

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION,
    docs_url=f"{VERSION_PREFIX}/docs",
    default_response_class=CustomResponse,
)


register_logger(app)
register_error_handlers(app)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


app.include_router(user_router, prefix=f"{VERSION_PREFIX}/users", tags=["users"])
