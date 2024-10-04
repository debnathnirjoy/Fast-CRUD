from sqlalchemy.orm import Session
from src.repositories.user_repository import UserRepository
from src.schemas.audit import AuditSchema
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserRetrieveSchema
from fastapi import status, HTTPException, Request
from src.utils.logger import logger
from src.utils.password_utils import get_password_hash
from src.utils.audit_utils import create_audit_schema


user_repository = UserRepository()
table_name = user_repository.model.__tablename__
service_name = "UserService"


def create_user(db: Session, user: UserCreateSchema, request: Request) -> UserRetrieveSchema:
    user.password = get_password_hash(user.password)
    audit_schema = create_audit_schema(request, table_name, service_name, action_name="Create_user")
    new_user = user_repository.create(db, user, audit_schema)
    if new_user is None:
        logger.error(f"Error occurred while creating user")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while creating user")
    logger.info(f"created user {new_user.id}")
    return new_user

def get_all_users(db: Session, page: int, limit: int, request: Request) -> list[UserRetrieveSchema]:
    audit_schema = create_audit_schema(request, table_name, service_name, action_name="Get_all_users")
    offset = (page - 1) * limit
    return user_repository.get_all(db, offset=offset, limit=limit, audit_schema=audit_schema)

def get_user_by_id(db: Session, user_id: str, request: Request) -> UserRetrieveSchema:
    audit_schema = create_audit_schema(request, table_name, service_name, action_name="Get_user_by_id")
    user = user_repository.get_by_id(db, audit_schema, user_id)
    if not user:
        logger.error(f"User {user_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

def update_user_by_id(db: Session, user_id: str, updated_user: UserUpdateSchema, request: Request):
    audit_schema = create_audit_schema(request, table_name, service_name, action_name="Update_user_by_id")
    update_count = user_repository.update_by_id(db, user_id, updated_user, audit_schema)
    if update_count > 0:
        logger.info(f"User {user_id} has been updated")
        return updated_user.model_dump(exclude_unset=True)
    else:
        logger.error(f"error occurred while updating user {user_id}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

def delete_user_by_id(db: Session, user_id: str, request: Request):
    audit_schema = create_audit_schema(request, table_name, service_name, action_name="Delete_user_by_id")
    delete_count = user_repository.delete_by_id(db, user_id, audit_schema)
    if delete_count > 0:
        logger.info(f"User {user_id} has been deleted")
        return delete_count
    else:
        logger.error(f"error occurred while deleting user {user_id}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")