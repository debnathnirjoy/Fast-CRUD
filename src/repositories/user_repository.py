from src.db.models.user import User
from src.repositories.base_repository import BaseRepository
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserRetrieveSchema


class UserRepository(BaseRepository[User, UserCreateSchema, UserRetrieveSchema, UserUpdateSchema]):
    def __init__(self):
        super().__init__(User, UserCreateSchema, UserRetrieveSchema, UserUpdateSchema)
