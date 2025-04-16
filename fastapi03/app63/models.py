import re
from typing import Annotated, Optional

from annotated_types import Gt, Lt, MaxLen, MinLen
from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    username: Annotated[str, MaxLen(30)]
    age: Annotated[int, Gt(18), Lt(100)]
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(16)]
    phone: Optional[str] = "Unknown"

    @field_validator("phone")
    @classmethod
    def validate_phone_number(cls, phone: str) -> str:
        if phone != "Unknown" and not re.match(r"^\+\d{1,12}$", phone):
            raise ValueError()
        return phone


class ErrorResponseModel(BaseModel):
    status_code: str
    message: str
    error_code: str
