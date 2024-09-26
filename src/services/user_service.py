from sqlalchemy.orm import Session
from src.repositories import user_repository
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserRetrieveSchema
from fastapi import status, HTTPException
from src.utils.password_utils import get_password_hash


def create_user(db: Session, user: UserCreateSchema):
    user.password = get_password_hash(user.password)
    return user_repository.create_user(db, user)

def get_all_users(db: Session, page: int, limit: int):
    offset = (page - 1) * limit
    return user_repository.get_all_users(db, offset, limit)

def get_user_by_id(db: Session, user_id: str):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

def update_user_by_id(db: Session, user_id: str, updated_user: UserUpdateSchema):
    update_count = user_repository.update_user_by_id(db, user_id, updated_user)
    if update_count > 0:
        return updated_user.model_dump(exclude_unset=True)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

def delete_user_by_id(db: Session, user_id: str):
    delete_count = user_repository.delete_user_by_id(db, user_id)
    if delete_count > 0:
        return delete_count
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")