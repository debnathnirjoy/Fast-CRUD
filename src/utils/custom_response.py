from typing import Any
from pydantic import BaseModel
from fastapi.responses import JSONResponse


class ResponseStructure(BaseModel):
    status_code: int
    data: Any


class CustomResponse(JSONResponse):
    def __init__(self, content: Any, status_code: int = 200, *args, **kwargs) -> None:
        content = ResponseStructure(status_code=status_code, data=content).model_dump()
        super().__init__(content, status_code, *args, **kwargs)
