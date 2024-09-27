from sqlalchemy.orm import Session
from src.repositories import user_repository
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserRetrieveSchema
from fastapi import status, HTTPException
from src.utils.logger import logger
from src.utils.password_utils import get_password_hash


def create_user(db: Session, user: UserCreateSchema) -> UserRetrieveSchema:
    user.password = get_password_hash(user.password)
    new_user = user_repository.create_user(db, user)
    if new_user is None:
        logger.error(f"Error occurred while creating user")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while creating user")
    logger.info(f"created user {new_user.id}")
    return new_user

def get_all_users(db: Session, page: int, limit: int) -> list[UserRetrieveSchema]:
    offset = (page - 1) * limit
    return user_repository.get_all_users(db, offset, limit)

def get_user_by_id(db: Session, user_id: str) -> UserRetrieveSchema:
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        logger.error(f"User {user_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

def update_user_by_id(db: Session, user_id: str, updated_user: UserUpdateSchema):
    update_count = user_repository.update_user_by_id(db, user_id, updated_user)
    if update_count > 0:
        logger.info(f"User {user_id} has been updated")
        return updated_user.model_dump(exclude_unset=True)
    else:
        logger.error(f"error occurred while updating user {user_id}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

def delete_user_by_id(db: Session, user_id: str):
    delete_count = user_repository.delete_user_by_id(db, user_id)
    if delete_count > 0:
        logger.info(f"User {user_id} has been deleted")
        return delete_count
    else:
        logger.error(f"error occurred while deleting user {user_id}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")