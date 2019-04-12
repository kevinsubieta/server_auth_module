from typing import List

from sqlalchemy.exc import IntegrityError

from adapters.user_adapters import str_to_user
from application.auth import encrypt
from domain.constants import WRONG_USERNAME_PASSWORD, PASSWORD_USED, PASSWORD_TOO_SHORT, FEW_SPECIALS, FEW_UPPERCASE, SPECIAL_CHARS, UPPERCASE_LETTERS, NOT_AUTHORIZED, USER_NOT_FOUND, VALID
from domain.models import AuthSettings, User
from functional.utils import remove
from repository import transaction
from repository.user_repo import get_user_by_username_password, change_password, password_exists, enable_user, is_admin, get_user_by_username
from repository.auth_settings_repo import get_settings
from service.endpoints import Handler
from service.utils import verify_basic_auth, respond


def res(error: str = ''):
    return dict(error=error, success=len(error) <= 0)


def respond_user(user_id=None, error: str = None) -> dict:
    return dict(user_id=user_id, error=error)


def is_valid(msg: str, function: callable, *args, **kwargs) -> dict:
    return respond_user(error=msg) if msg is not VALID else respond_user(function(*args, **kwargs))


class UserCreateHandler(Handler):
    def post(self):
        user = str_to_user(self.get_argument('user'))
        token = self.get_argument('token')
        try:
            with transaction() as db:
                if not verify_basic_auth(self) or not is_admin(db, token):
                    return respond(NOT_AUTHORIZED)

                # self.res(verify_basic_auth(self, create_user_service, db, token, user))
        except IntegrityError:
            self.error('the username is already in used, choose other')


class UserEnableHandler(Handler):
    def post(self):
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


def validate(user: User, settings: AuthSettings, password: str, db) -> str:
    if user is None:
        return WRONG_USERNAME_PASSWORD
    if user.id is not None and (password_exists(db, user.id, password) or user.password == encrypt(password)):
        return PASSWORD_USED
    if len(password) < settings.min_password_len:
        return PASSWORD_TOO_SHORT % settings.min_password_len
    if not has_enough(password, settings.min_special_letters_number, SPECIAL_CHARS):
        return FEW_SPECIALS % settings.min_special_letters_number
    if not has_enough(password, settings.min_uppercase_letters_number, UPPERCASE_LETTERS):
        return FEW_UPPERCASE % settings.min_uppercase_letters_number
    return VALID
