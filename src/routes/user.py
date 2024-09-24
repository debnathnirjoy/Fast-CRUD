from fastapi import Depends, status, HTTPException, APIRouter
from src.schemas.user import UserRetrieveSchema, UserUpdateSchema, UserCreateSchema
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.services import user_service


user_router = APIRouter()


@user_router.get('/', response_model=list[UserRetrieveSchema])
def get_all_users(db_session: Session = Depends(get_db)) -> list[UserRetrieveSchema]:
    users = user_service.get_all_users(db_session)
    return users


@user_router.get('/{user_id}', response_model=UserRetrieveSchema)
def get_user_by_id(user_id: str, db_session: Session = Depends(get_db)) -> UserRetrieveSchema:
    user = user_service.get_user_by_id(db_session, user_id)
    return user


@user_router.patch('/{user_id}', response_model=UserUpdateSchema)
def update_user_by_id(user_id: str, updated_fields: UserUpdateSchema, db_session: Session = Depends(get_db)) -> UserUpdateSchema:
    user = user_service.update_user_by_id(db_session, user_id, updated_fields)
    return user


@user_router.delete('/{user_id}', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(user_id: str, db_session: Session = Depends(get_db)) -> None:
    user_service.delete_user_by_id(db_session, user_id)


@user_router.post('/', response_model=UserRetrieveSchema)
def create_user(user: UserCreateSchema, db_session: Session = Depends(get_db)) -> UserRetrieveSchema:
    user = user_service.create_user(db_session, user)
    return user
