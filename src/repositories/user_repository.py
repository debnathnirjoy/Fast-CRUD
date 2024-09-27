from sqlalchemy.orm import Session
from src.db.models.user import User
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserRetrieveSchema


def create_user(db: Session, user: UserCreateSchema) -> UserRetrieveSchema | None:
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user_schema = None if new_user is None else UserRetrieveSchema.model_validate(new_user, from_attributes=True)
    return user_schema

def get_all_users(db: Session, offset: int, limit: int) -> list[UserRetrieveSchema]:
    users = db.query(User).order_by(User.created_at).offset(offset).limit(limit).all()
    user_schema_list = [UserRetrieveSchema.model_validate(user, from_attributes=True) for user in users]
    return user_schema_list

def get_user_by_id(db: Session, user_id: str) -> UserRetrieveSchema | None:
    user = db.query(User).filter_by(id=user_id).first()
    user_schema = None if user is None else UserRetrieveSchema.model_validate(user, from_attributes=True)
    return user_schema

def update_user_by_id(db: Session, user_id: str, updated_user: UserUpdateSchema) -> int:
    updated_user_dict = updated_user.model_dump(exclude_unset=True)
    update_count = db.query(User).filter_by(id=user_id).update(updated_user_dict)
    db.commit()
    return update_count

def delete_user_by_id(db: Session, user_id: str) -> int:
    delete_count = db.query(User).filter_by(id=user_id).delete()
    db.commit()
    return delete_count
