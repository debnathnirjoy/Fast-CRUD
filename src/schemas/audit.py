from datetime import datetime
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, EmailStr, model_validator

class AuditSchema(BaseModel):
    id: str | None = Field(default=None)
    ip_address: str = Field(..., min_length=3, max_length=255)
    table_name: str = Field(..., min_length=3, max_length=255)
    service_name: str = Field(..., min_length=3, max_length=255)
    action_name: str = Field(..., min_length=3, max_length=255)
    request_url: str = Field(..., min_length=3, max_length=255)
    request_method: str = Field(..., min_length=3, max_length=255)
    response: dict | None = Field(default=None)



# id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     ip_address: Mapped[str] = mapped_column(String(255), nullable=False)
#     table_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     service_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     action_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     request_url: Mapped[str] = mapped_column(String(255), nullable=False)
#     request_method: Mapped[str] = mapped_column(String(255), nullable=False)
#     request_params: Mapped[str] = mapped_column(String(255), nullable=False)
#     response: Mapped[dict] = mapped_column(JSON, nullable=False)
#     created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())