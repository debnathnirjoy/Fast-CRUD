from sqlalchemy.orm import Session
from src.repositories import user_repository
from src.schemas.user import UserCreateSchema, UserUpdateSchema
from fastapi import status, HTTPException


def create_user(db: Session, user: UserCreateSchema):
    return user_repository.create_user(db, user)

def get_all_users(db: Session):
    return user_repository.get_all_users(db)

def get_user_by_id(db: Session, user_id: str):
    return user_repository.get_user_by_id(db, user_id)

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