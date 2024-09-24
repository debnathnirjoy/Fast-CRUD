from sqlalchemy.orm import Session
from src.db.models.user import User
from src.schemas.user import UserCreateSchema, UserUpdateSchema


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreateSchema):
        new_user = User(username=user.name, email=user.email, password=user.password, name = user.name)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)



    def get_all_user(self):
        users = self.db.query(User).all()
        return users

    def get_user_by_id(self, user_id):
        user = self.db.query(User).filter_by(id=user_id).first()
        return user

    def update_user_by_id(self, user_id, updated_user: UserUpdateSchema):
        updated_user_dict = updated_user.model_dump(exclude_unset=True)
        update_count = self.db.query(User).filter_by(id=user_id).update(updated_user_dict)
        self.db.commit()
        return update_count

    def delete_user_by_id(self, user_id):
        delete_count = self.db.query(User).filter_by(id=user_id).delete()
        self.db.commit()
        return delete_count


