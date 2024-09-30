from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.ddl import CreateSchema


ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
RetrieveSchemaType = TypeVar('RetrieveSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, RetrieveSchemaType, UpdateSchemaType]):
    def __init__(self,
                 model: Type[ModelType],
                 create_schema: Type[CreateSchemaType],
                 retrieve_schema: Type[RetrieveSchemaType],
                 update_schema: Type[UpdateSchemaType]
                 ) -> None:
        self.model = model
        self.retrieve_schema = retrieve_schema

    def create(self, db: Session, schema: CreateSchemaType) -> RetrieveSchemaType | None:
        new_db_obj = self.model(**schema.model_dump())
        db.add(new_db_obj)
        db.commit()
        db.refresh(new_db_obj)
        new_schema_obj = None if new_db_obj is None else self.retrieve_schema.model_validate(new_db_obj, from_attributes=True)
        return new_schema_obj

    def get_all(self, db: Session, limit: int, offset: int) -> list[RetrieveSchemaType]:
        db_object_list = db.query(self.model).order_by(self.model.created_at).offset(offset).limit(limit).all()
        print(limit, offset)
        print(db_object_list)
        user_schema_list = [self.retrieve_schema.model_validate(user, from_attributes=True) for user in db_object_list]
        return user_schema_list

    def get_by_id(self, db: Session, item_id: str) -> RetrieveSchemaType:
        db_object = db.query(self.model).filter_by(id=item_id).first()
        schema_object = None if db_object is None else self.retrieve_schema.model_validate(db_object, from_attributes=True)
        return schema_object

    def update_by_id(self, db: Session, item_id: str, updated_item: UpdateSchemaType) -> int:
        updated_item_dict = updated_item.model_dump(exclude_unset=True)
        update_count = db.query(self.model).filter_by(id=item_id).update(updated_item_dict)
        db.commit()
        return update_count

    def delete_by_id(self, db: Session, item_id: str) -> int:
        delete_count = db.query(self.model).filter_by(id=item_id).delete()
        db.commit()
        return delete_count
