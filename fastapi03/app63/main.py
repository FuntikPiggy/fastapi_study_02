import time

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_babel import Babel, BabelConfigs, BabelMiddleware, _

from custom_exceptions import InvalidUserDataException, UserNotFoundException
from database import create_new_user, load_user_from_db
from models import User

app = FastAPI()

babel_configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",  # Язык по умолчанию
    BABEL_TRANSLATION_DIRECTORY="locales",  # Папка с переводами
)

babel = Babel(configs=babel_configs)

app.add_middleware(BabelMiddleware, babel_configs=babel_configs)


def get_custom_message():
    messages = {
        "username": _("The username must be a string of up to 30 characters."),
        "age": _("The age must be an integer between 18 and 100."),
        "email": _("The email address is incorrect."),
        "password": _(
            "The password must be a string "
            "between 8 and 16 characters long."
        ),
        "phone": _(
            'The phone number must start with a " + " '
            "and contain from 1 to 12 digits."
        ),
    }
    return messages


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request,
                                 exc: RequestValidationError):
    messages = get_custom_message()
    start = time.perf_counter()
    errors = {}
    for n, ex in enumerate(exc.errors(), 1):
        errors[f"{n}"] = messages.get(ex["loc"][-1], _("Unknown error"))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=errors,
        headers={
            "X-ErrorHandleTime": _(
                f"Time - " f"{round(time.perf_counter() - start, 4)} " f"sec."
            )
        },
    )


@app.exception_handler(InvalidUserDataException)
def InvalidUserDataException_handler(request: Request,
                                     exc: InvalidUserDataException):
    start = time.perf_counter()
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers={
            "X-ErrorHandleTime": _(
                f"Time - " f"{round(time.perf_counter() - start, 4)} " f"sec."
            )
        },
    )


@app.exception_handler(UserNotFoundException)
def UserNotFoundException_handler(request: Request, exc):
    start = time.perf_counter()
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers={
            "X-ErrorHandleTime": _(
                f"Time - " f"{round(time.perf_counter() - start, 4)} " f"sec."
            )
        },
    )


@app.post("/new_user")
def new_user(user: User):
    create_new_user(user)
    return user


@app.get("/load_user/{username}")
def load_user(username: str):
    user = User(**load_user_from_db(username))
    return user


if __name__ == "__main__":
    uvicorn.run("app63.main:app", host="0.0.0.0", port=8000, reload=True)
