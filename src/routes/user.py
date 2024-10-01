import time

from fastapi import Depends, status, HTTPException, APIRouter, Query, Request
from typing import Annotated
from src.schemas.user import UserRetrieveSchema, UserUpdateSchema, UserCreateSchema
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.services import user_service


user_router = APIRouter()


@user_router.get('/', response_model=list[UserRetrieveSchema], status_code=status.HTTP_200_OK)
def get_all_users(request: Request,
                  page: Annotated[int, Query(description="page number", ge=1)] = 1,
                  limit: Annotated[int, Query(description="number of items to skip", ge=1, le=100)] = 3,
                  db_session: Session = Depends(get_db)) -> list[UserRetrieveSchema]:
    users = user_service.get_all_users(db_session, page, limit, request)
    return users


@user_router.get('/{user_id}', response_model=UserRetrieveSchema, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: str, request: Request, db_session: Session = Depends(get_db)) -> UserRetrieveSchema:
    user = user_service.get_user_by_id(db_session, user_id, request)
    return user


@user_router.put('/{user_id}', response_model=UserUpdateSchema, status_code=status.HTTP_200_OK)
def update_user_by_id(user_id: str, updated_fields: UserUpdateSchema, request: Request, db_session: Session = Depends(get_db)) -> UserUpdateSchema:
    user = user_service.update_user_by_id(db_session, user_id, updated_fields, request)
    return user


@user_router.delete('/{user_id}', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(user_id: str, request: Request, db_session: Session = Depends(get_db)) -> None:
    user_service.delete_user_by_id(db_session, user_id, request)


@user_router.post('/', response_model=UserRetrieveSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateSchema, request: Request, db_session: Session = Depends(get_db)) -> UserRetrieveSchema:
    user = user_service.create_user(db_session, user, request)
    return user
