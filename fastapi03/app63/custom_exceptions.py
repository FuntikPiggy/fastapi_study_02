from fastapi import HTTPException, status
from fastapi_babel import _


class UserNotFoundException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=_("User not found")
        )


class InvalidUserDataException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=_("Invalid user data"),
        )
