import json
from datetime import date, datetime
from typing import List

from application.auth import encrypt
from domain.models import User


def str_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def create_obj(class_, values: dict, keys: List[str]):
    obj = class_()
    for key in values:
        if key in keys:
            setattr(obj, key, values[key])
    return obj


def str_to_user(user_str: str) -> User:
    data = json.loads(user_str)
    user = create_obj(
        User,
        data,
        [
            'id_number',
            'name',
            'last_name',
            'email_address',
            'birthday',
            'username',
            'password',
            'password_expire',
            'is_admin'
        ]
    )
    user.birthday = str_to_date(data['birthday'])
    return user


def encrypt_user_password(user: User) -> User:
    user.password = encrypt(user.password)
    return user
