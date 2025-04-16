from typing import Optional, Annotated
from annotated_types import MinLen, MaxLen, Gt, Lt

from pydantic import BaseModel, EmailStr, field_validator
import re


class User(BaseModel):
    username: Annotated[str, MaxLen(30)]
    age: Annotated[int, Gt(18), Lt(100)]
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(16)]
    phone: Optional[str] = "Unknown"

    @field_validator("phone")
    @classmethod
    def validate_phone_number(cls, phone_num: str) -> str:
        if phone_num != "Unknown" and not re.match(r"^\+\d{1,12}$", phone_num):
            raise ValueError()
        return phone_num
