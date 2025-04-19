import json

from custom_exceptions import InvalidUserDataException, UserNotFoundException
from models import User

from app import settings


def read_env() -> str:
    return settings.db_path


async def file_read() -> dict:
    DB_PATH = read_env()
    try:
        with open(DB_PATH, "r", encoding="U8") as ifl:
            users_db = json.load(ifl)
    except Exception:
        users_db = {}
    return users_db


async def create_new_user(user: User) -> None:
    DB_PATH = read_env()
    users_db = await file_read()
    if user.username in users_db:
        raise InvalidUserDataException()
    else:
        users_db[user.username] = user.__dict__
    with open(DB_PATH, "w", encoding="U8") as ofl:
        json.dump(users_db, ofl, ensure_ascii=False, indent=4)


async def load_user_from_db(username: str) -> dict:
    users_db = await file_read()
    if username in users_db:
        return {k: v for k, v in users_db[username].items() if k != "password"}
    else:
        raise UserNotFoundException()


async def delete_user(username: str) -> None:
    DB_PATH = read_env()
    users_db = await file_read()
    if username in users_db:
        del users_db[username]
    else:
        raise InvalidUserDataException()
    with open(DB_PATH, "w", encoding="U8") as ofl:
        json.dump(users_db, ofl, ensure_ascii=False, indent=4)
