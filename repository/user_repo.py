from datetime import datetime

from sqlalchemy.orm import Session as alchemy

from application.auth import encrypt
from domain.models import User, Session, AuthSettings, UsedPassword
from repository.utils import current_datetime_epoch


def get_user_by_username_password(db: alchemy, username: str, password: str) -> User:
    return db.query(User).filter(User.username == username).filter(User.password == encrypt(password)).first()


def get_user_by_username(db: alchemy, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def insert_user(db: alchemy, user: User) -> int:
    db.add(user)
    db.commit()
    return user.id


def change_password(db: alchemy, user: User, password: str, settings: AuthSettings):
    db.add(UsedPassword(password=user.password, user_id=user.id))
    user.password = encrypt(password)
    user.must_change_password = False
    user.last_password_change_datetime, user.last_password_change_epoch = current_datetime_epoch()
    user.password_expiration_epoch = user.last_password_change_epoch + settings.password_expiration_epoch
    user.password_expiration_datetime = datetime.fromtimestamp(float(user.password_expiration_epoch))
    db.commit()


def password_exists(db: alchemy, user_id, password) -> bool:
    return db.query(UsedPassword).filter(UsedPassword.user_id == user_id).filter(UsedPassword.password == encrypt(password)).first() is not None


def is_admin(db: alchemy, token: str) -> bool:
    session = db.query(Session).filter(Session.token == token).first()
    if session is None:
        return False
    user: User = db.query(User).get(session.user_id)
    return user.is_admin if user is not None else False


def enable_user(db: alchemy, username: str, is_enabled: bool) -> bool:
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return False
    user.failed_login_number = 0
    user.is_enabled = is_enabled
    db.commit()
    return True
