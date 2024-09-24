from fastapi import FastAPI
from src.db.models.user import User
from src.db.database import engine, Base

app = FastAPI()


Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}