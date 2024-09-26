from fastapi import FastAPI
from src.db.models.user import User
from src.db.database import engine, Base
from src.routes.user import user_router
from src.middlewares.logger import register_logger


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
)


register_logger(app)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


app.include_router(user_router, prefix=f"{VERSION_PREFIX}/users", tags=["users"])
