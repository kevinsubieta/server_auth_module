import json

from adapters import str_to_date, create_obj
from domain.models import User


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
