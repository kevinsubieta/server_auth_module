from datetime import datetime

from application.auth import encrypt
from database.db import transaction
from domain.models import User
from repository.user_repo import get_user_by_username, login, fail_login

from repository.user_repo import logout
from service.constants import WRONG_USERNAME_PASSWORD
from service.endpoints import Handler


class LoginHandler(Handler):
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        with transaction() as db:
            self.res(self.login(db, get_user_by_username(db, username), password))

    def login(self, db, user: User, password: str) -> dict:
        if user is None:
            return dict(ERROR=WRONG_USERNAME_PASSWORD)
        if user.password != encrypt(password):
            fail_login(db, user)
            return dict(ERROR=WRONG_USERNAME_PASSWORD)
        if user.is_first_login or user.password_expiration_datetime > datetime.now():
            return dict(is_first_login=True)
        return dict(is_first_login=False, token=login(db, user))


class LogoutHandler(Handler):
    def post(self):
        token = self.get_argument('token')
        with transaction() as db:
            logout(db, token)
        self.res(dict(success=True))
