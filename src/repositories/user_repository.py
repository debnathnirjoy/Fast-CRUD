from sqlalchemy.orm import Session
from src.db.models.user import User
from src.schemas.user import UserCreateSchema, UserUpdateSchema

def create_user(db: Session, user: UserCreateSchema):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    users = db.query(User).all()
    return users

def get_user_by_id(db: Session, user_id: str):
    user = db.query(User).filter_by(id=user_id).first()
    return user

def update_user_by_id(db: Session, user_id: str, updated_user: UserUpdateSchema):
    updated_user_dict = updated_user.model_dump(exclude_unset=True)
    update_count = db.query(User).filter_by(id=user_id).update(updated_user_dict)
    db.commit()
    return update_count

def delete_user_by_id(db: Session, user_id: str):
    delete_count = db.query(User).filter_by(id=user_id).delete()
    db.commit()
    return delete_count
