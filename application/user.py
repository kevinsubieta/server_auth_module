from typing import List

from application.auth import encrypt
from domain.constants import VALID, UserAuthErrors
from domain.models import User, AuthSettings
from functional.utils import remove
from repository.user_repo import password_exists


def validate(user: User, settings: AuthSettings, password: str, db) -> str:
    if user is None:
        return UserAuthErrors.WRONG_USERNAME_PASSWORD
    if user.id is not None and (password_exists(db, user.id, password) or user.password == encrypt(password)):
        return UserAuthErrors.PASSWORD_USED
    if len(password) < settings.min_password_len:
        return UserAuthErrors.PASSWORD_TOO_SHORT % settings.min_password_len
    if not has_enough(password, settings.min_special_letters_number, UserAuthErrors.SPECIAL_CHARS):
        return UserAuthErrors.FEW_SPECIALS % settings.min_special_letters_number
    if not has_enough(password, settings.min_uppercase_letters_number, UserAuthErrors.UPPERCASE_LETTERS):
        return UserAuthErrors.FEW_UPPERCASE % settings.min_uppercase_letters_number
    return VALID


def has_enough(password: str, min_: int, specials: List[str]) -> bool:
    return min_ <= 0 \
        if len(password) == 0 or min_ <= 0 \
        else has_enough(password[1:], min_ - 1, remove(specials, password[0])) \
        if password[0] in specials \
        else has_enough(password[1:], min_, specials)
