from typing import List

from sqlalchemy.exc import IntegrityError

from application.auth import encrypt
from database.db import transaction
from domain.models import AuthSettings, User
from repository.user_repo import get_user_by_username_password, change_password, insert_user, password_exists, get_settings, enable_user, is_admin, get_user_by_username
from service.constants import WRONG_USERNAME_PASSWORD, PASSWORD_USED, PASSWORD_TOO_SHORT, FEW_SPECIALS, FEW_UPPERCASE, SPECIAL_CHARS, UPPERCASE_LETTERS, NOT_AUTHORIZED, USER_NOT_FOUND
from service.endpoints import Handler
from service.utils import str_to_user, encrypt_user_password, remove


def res(error: str = ''):
    return dict(error=error, success=len(error) <= 0)


class UserCreateHandler(Handler):
    def post(self):
        if not self.is_authenticated():
            return
        user = str_to_user(self.get_argument('user'))
        token = self.get_argument('token')
        try:
            with transaction() as db:
                if is_admin(db, token):
                    response = validate(user, get_settings(db), user.password, db)
                    if not response['success']:
                        self.res(response)
                    else:
                        user_id = insert_user(db, encrypt_user_password(user))
                        self.res(dict(user_id=user_id))
                else:
                    self.error(NOT_AUTHORIZED)
        except IntegrityError as e:
            self.error('the username is already in used, choose other')


class UserEnableHandler(Handler):
    def post(self):
        if not self.is_authenticated():
            return
        username = self.get_argument('username')
        to_enable = self.get_argument('to_enable')
        token = self.get_argument('token')
        try:
            with transaction() as db:
                if is_admin(db, token):
                    success = enable_user(db, username, to_enable == '1')
                    if not success:
                        self.error(USER_NOT_FOUND)
                    else:
                        self.res(res())
                else:
                    self.error(NOT_AUTHORIZED)
        except IntegrityError as e:
            self.error('Internal Error')


class UserResetPasswordHandler(Handler):
    def post(self):
        if not self.is_authenticated():
            return
        username = self.get_argument('username')
        new_password = self.get_argument('new_password')
        token = self.get_argument('token')
        try:
            with transaction() as db:
                if is_admin(db, token):
                    user = get_user_by_username(db, username)
                    response = validate(user, get_settings(db), new_password, db)
                    if response['success']:
                        change_password(db, user, new_password, get_settings(db))
                    self.res(response)
                else:
                    self.error(NOT_AUTHORIZED)
        except IntegrityError as e:
            self.error('Internal Error')


class UserUpdatePasswordHandler(Handler):
    def post(self):
        if not self.is_authenticated():
            return
        username = self.get_argument('username')
        old_password = self.get_argument('old_password')
        new_password = self.get_argument('new_password')

        with transaction() as db:
            user = get_user_by_username_password(db, username, old_password)
            response = validate(user, get_settings(db), new_password, db)
            if response['success']:
                change_password(db, user, new_password, get_settings(db))
            self.res(response)


def has_enough(password: str, min_: int, specials: List[str]) -> bool:
    return min_ <= 0 \
        if len(password) == 0 or min_ <= 0 \
        else has_enough(password[1:], min_ - 1, remove(specials, password[0])) \
        if password[0] in specials \
        else has_enough(password[1:], min_, specials)


def validate(user: User, settings: AuthSettings, password: str, db) -> dict:
    if user is None:
        return res(WRONG_USERNAME_PASSWORD)
    if user.id is not None and (password_exists(db, user.id, password) or user.password == encrypt(password)):
        return res(PASSWORD_USED)
    if len(password) < settings.min_password_len:
        return res(PASSWORD_TOO_SHORT % settings.min_password_len)
    if not has_enough(password, settings.min_special_letters_number, SPECIAL_CHARS):
        return res(FEW_SPECIALS % settings.min_special_letters_number)
    if not has_enough(password, settings.min_uppercase_letters_number, UPPERCASE_LETTERS):
        return res(FEW_UPPERCASE % settings.min_uppercase_letters_number)
    return res()
