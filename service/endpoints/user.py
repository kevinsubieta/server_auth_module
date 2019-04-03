import string
from typing import List

from sqlalchemy.exc import IntegrityError

from database.db import transaction
from domain.models import AuthSettings, User
from repository.user_repo import get_user_by_username_password, change_password, insert_user, password_exists, get_settings, enable_user
from service.constants import WRONG_USERNAME_PASSWORD, PASSWORD_USED, PASSWORD_TOO_SHORT, FEW_SPECIALS, FEW_UPPERCASE
from service.endpoints import Handler
from service.utils import str_to_user, encrypt_user_password, remove


def res(error: str = ''):
    return dict(error=error, success=len(error) <= 0)


class UserCreateHandler(Handler):
    def post(self):
        user = str_to_user(self.get_argument('user'))
        try:
            with transaction() as db:
                response = validate(user, get_settings(db), user.password, db)
                if not response['success']:
                    self.res(response)
                else:
                    user_id = insert_user(db, encrypt_user_password(user))
                    self.res(dict(user_id=user_id))
        except IntegrityError as e:
            self.error('the username is already in used, choose other')


class UserEnableHandler(Handler):
    def post(self):
        username = self.get_argument('username')
        to_enable = self.get_argument('to_enable')
        try:
            with transaction() as db:
                enable_user(db, username, to_enable == '1')
            self.res(res())
        except IntegrityError as e:
            self.error('Internal Error')


class UserUpdatePasswordHandler(Handler):
    def post(self):
        username = self.get_argument('username')
        old_password = self.get_argument('old_password')
        new_password = self.get_argument('new_password')

        with transaction() as db:
            user = get_user_by_username_password(db, username, old_password)
            response = validate(user, get_settings(db), new_password, db)
            settings = get_settings(db)
            if response['success']:
                change_password(db, user, new_password, settings)
            self.res(response)


special_letters = string.printable[:10] + string.printable[52:94]
uppercase_letters = string.printable[36:62]


def has_enough_specials(password: str, min_: int, specials: List[str]) -> bool:
    return min_ <= 0 if len(password) == 0 else has_enough_specials(password[1:], min_ - 1, remove(specials, password[0])) if password[0] in specials else has_enough_specials(password[1:], min_,
                                                                                                                                                                               specials)


def validate(user: User, settings: AuthSettings, password: str, db) -> dict:
    if user is None:
        return res(WRONG_USERNAME_PASSWORD)
    if user.id is not None and password_exists(db, user.id, password):
        return res(PASSWORD_USED)
    if len(password) < settings.min_password_len:
        return res(PASSWORD_TOO_SHORT % settings.min_password_len)
    if not has_enough_specials(password, settings.min_special_letters_number, special_letters):
        return res(FEW_SPECIALS % settings.min_special_letters_number)
    if not has_enough_specials(password, settings.min_uppercase_letters_number, uppercase_letters):
        return res(FEW_UPPERCASE % settings.min_uppercase_letters_number)
    return res()
