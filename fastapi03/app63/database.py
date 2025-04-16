import json

from custom_exceptions import InvalidUserDataException, UserNotFoundException
from models import User

DB_PATH = "users_db.json"


def create_new_user(user: User) -> None:
    try:
        with open(DB_PATH, "r", encoding="U8") as ifl:
            users_db = json.load(ifl)
    except Exception:
        users_db = {}
    if user.username in users_db:
        raise InvalidUserDataException()
    else:
        users_db[user.username] = user.__dict__
    with open(DB_PATH, "w", encoding="U8") as ofl:
        json.dump(users_db, ofl, ensure_ascii=False, indent=4)


def load_user_from_db(username: str) -> dict:
    try:
        with open(DB_PATH, "r", encoding="U8") as ifl:
            users_db = json.load(ifl)
    except Exception:
        users_db = {}
    if username in users_db:
        return users_db[username]
    else:
        raise UserNotFoundException()
