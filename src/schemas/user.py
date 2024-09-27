from datetime import datetime
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, EmailStr, model_validator


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=3, max_length=128)
    email: EmailStr = Field(..., max_length=128)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., exclude=True)

    @model_validator(mode='after')
    def validate_password_and_confirm(self):
        if self.password != self.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords must match')
        return self


class UserUpdateSchema(UserBaseSchema):
    ...

class UserRetrieveSchema(UserBaseSchema):
    id: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
