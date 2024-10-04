import json
from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.schemas.audit import AuditSchema
from src.db.models.audit import AuditLog


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

    def _commit(self, db:Session, response:list[RetrieveSchemaType] | RetrieveSchemaType | int, audit_schema: AuditSchema) -> None:
        new_audit_obj = AuditLog(**audit_schema.model_dump())
        new_audit_obj.response = {"Response": str(response)}
        db.add(new_audit_obj)
        db.commit()

    def create(self, db: Session, schema: CreateSchemaType, audit_schema: AuditSchema) -> RetrieveSchemaType | None:
        new_db_obj = self.model(**schema.model_dump())
        db.add(new_db_obj)
        db.flush()
        new_schema_obj = None if new_db_obj is None else self.retrieve_schema.model_validate(new_db_obj, from_attributes=True)
        self._commit(db, new_schema_obj, audit_schema)
        return new_schema_obj

    def get_all(self, db: Session, limit: int, offset: int, audit_schema: AuditSchema) -> list[RetrieveSchemaType]:
        db_object_list = db.query(self.model).order_by(self.model.created_at).offset(offset).limit(limit).all()
        user_schema_list = [self.retrieve_schema.model_validate(user, from_attributes=True) for user in db_object_list]
        self._commit(db, user_schema_list, audit_schema)
        return user_schema_list

    def get_by_id(self, db: Session, audit_schema:AuditSchema, item_id: str) -> RetrieveSchemaType:
        db_object = db.query(self.model).filter_by(id=item_id).first()
        schema_object = None if db_object is None else self.retrieve_schema.model_validate(db_object,from_attributes=True)
        self._commit(db, schema_object, audit_schema)
        return schema_object

    def update_by_id(self, db: Session, item_id: str, updated_item: UpdateSchemaType, audit_schema: AuditSchema) -> int:
        updated_item_dict = updated_item.model_dump(exclude_unset=True)
        update_count = db.query(self.model).filter_by(id=item_id).update(updated_item_dict)
        self._commit(db, update_count, audit_schema)
        return update_count

    def delete_by_id(self, db: Session, item_id: str, audit_schema: AuditSchema) -> int:
        delete_count = db.query(self.model).filter_by(id=item_id).delete()
        self._commit(db, delete_count, audit_schema)
        return delete_count
