from pydantic import BaseModel, validator, Field
from typing import Optional


class ErrorDTO(BaseModel):
    details: str
    error: str = "Bad request"
    code: int = 400