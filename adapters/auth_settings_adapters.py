import json

from adapters import create_obj
from domain.models import AuthSettings


def str_to_auth_settings(auth_settings_str: str) -> AuthSettings:
    return create_obj(
        AuthSettings,
        json.loads(auth_settings_str),
        [
            'failed_login_maximum_number',
            'password_expiration_epoch',
            'session_expiration_epoch',
            'simultaneous_sessions_nro_allowed',
            'min_special_letters_number',
            'min_uppercase_letters_number',
            'min_password_len',
        ]
    )
