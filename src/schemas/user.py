from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, EmailStr, field_validator


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=3, max_length=128)
    email: EmailStr = Field(..., max_length=128)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @field_validator('password', 'confirm_password')
    def validate_password_and_confirm(self):
        if self.password != self.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords must match')


class UserUpdateSchema(UserBaseSchema):
    username: str | None = Field(None, min_length=3, max_length=50)
    name: str | None = Field(None, min_length=3, max_length=128)
    email: EmailStr | None = Field(None, min_length=3, max_length=128)

    @field_validator('username', 'name', 'email')
    def validate_update_fields(self):
        if self.username is None and self.email is None and self.name is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "At least one of username, email or name must be set")

class UserRetrieveSchema(UserBaseSchema):
    id: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
