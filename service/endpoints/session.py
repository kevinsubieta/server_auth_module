from datetime import datetime

from application.auth import encrypt
from database.db import transaction
from domain.models import User
from repository.user_repo import get_user_by_username, login as login_db, fail_login
from repository.user_repo import logout
from service.constants import WRONG_USERNAME_PASSWORD, MUST_CHANGE_PASSWORD, DISABLED_USER, FAILED_LOGIN
from service.endpoints import Handler


def res(must_change_password: bool = None, is_failed_login: bool = None, is_user_enabled: bool = None, token: str = None, error: str = None, is_admin: bool = None) -> dict:
    return dict(must_change_password=must_change_password, failed_login=is_failed_login, user_enabled=is_user_enabled, token=token, error=error, is_admin=is_admin)


def login(db, user: User, password: str) -> dict:
    if user is None:
        return res(is_failed_login=True, error=WRONG_USERNAME_PASSWORD)
    if not user.is_enabled:
        return res(is_user_enabled=False, error=DISABLED_USER)
    if user.password != encrypt(password):
        return res(is_failed_login=True, is_user_enabled=True, error=FAILED_LOGIN % fail_login(db, user))
    if user.must_change_password or user.password_expiration_datetime < datetime.now():
        return res(is_failed_login=False, is_user_enabled=True, must_change_password=True, error=MUST_CHANGE_PASSWORD)
    return res(is_failed_login=False, must_change_password=False, is_user_enabled=True, token=login_db(db, user), is_admin=user.is_admin)


class LoginHandler(Handler):
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        with transaction() as db:
            self.res(login(db, get_user_by_username(db, username), password))


class LogoutHandler(Handler):
    def post(self):
        token = self.get_argument('token')
        with transaction() as db:
            logout(db, token)
        self.res(dict(success=True))
