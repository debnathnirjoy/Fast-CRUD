from src.db.models.user import User
from src.db.database import engine, Base
from src.routes.user import user_router
from src.middlewares.logger import register_logger
from src.utils.custom_response import CustomResponse
from fastapi import FastAPI, Request
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

register_error_handlers(app)
register_logger(app)


@app.get("/")
async def read_root(request: Request):
    print("Request from read root: ", request.client.host)
    return {"message": "Hello, World!"}


app.include_router(user_router, prefix=f"{VERSION_PREFIX}/users", tags=["users"])
