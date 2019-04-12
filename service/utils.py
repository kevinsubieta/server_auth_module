import base64

from flask import request as flask_request

from domain.constants import UserAuthErrors

USER_AUTH = "Vk7iBxhuaYZSCncLIbZazA==Cz8hZS/sv70ZgG7G01DhWQ=="
TOKEN_AUTH = "2a10YEm0utdWochklUhh8zZ78.SghQhV48VDem1voeO9yDihEHI2vA1US"


def respond(error: str = None) -> dict:
    return dict(success=error is None or len(error) == 0, error=error)


def is_valid_basic_auth(auth_header: str) -> bool:
    username, password = base64.b64decode(auth_header.split(None, 1)[-1]).decode('ascii').split(':', 1)
    return username == USER_AUTH and TOKEN_AUTH == password


def verify_basic_auth_header(auth_header: str) -> bool:
    return auth_header and auth_header.startswith('Basic ') and is_valid_basic_auth(auth_header)


def verify_basic_auth(request) -> bool:
    return verify_basic_auth_header(request.headers.get('Authorization'))


from functools import wraps


def basic_auth(function, *args, **kwargs):
    @wraps(function)
    def super_function(*args, **kwargs):
        if not verify_basic_auth(flask_request):
            return respond(UserAuthErrors.NOT_AUTHORIZED)
        return function(*args, **kwargs)

    return super_function
