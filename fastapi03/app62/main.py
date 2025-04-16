from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from pyexpat.errors import messages

from models import User

app = FastAPI()

messages = {
    "username": "Имя пользователя должно быть строкой до 30 символов",
    "age": "Возраст должен быть целым числом в пределах от 18 до 100",
    "email": "Адрес электронной почты некорректен",
    "password": "Пароль должен быть строкой длиной от 8 до 16 символов",
    "phone": 'Номер телефона должен начинаться с \" + \" и содержать от 1 до 12 цифр',
}


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for n, ex in enumerate(exc.errors(), 1):
        errors[f"{n}"] = messages.get(ex["loc"][-1], "Неизвестная ошибка")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=errors)


@app.post("/new_user")
def new_user(user: User):
    return user


if __name__ == "__main__":
    uvicorn.run("app62.main:app", host="0.0.0.0", port=8000, reload=True)
