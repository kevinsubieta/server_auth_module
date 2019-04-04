from datetime import datetime

from sqlalchemy.orm import Session as alchemy

from application.auth import encrypt, create_token
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


def create_session(db: alchemy, token: str, user_id):
    db.add(Session(token=token, user_id=user_id))
    db.commit()


def change_password(db: alchemy, user: User, password: str, settings: AuthSettings):
    db.add(UsedPassword(password=user.password, user_id=user.id))
    user.password = encrypt(password)
    user.must_change_password = False
    user.last_password_change_datetime, user.last_password_change_epoch = current_datetime_epoch()
    user.password_expiration_epoch = user.last_password_change_epoch + settings.password_expiration_epoch
    user.password_expiration_datetime = datetime.fromtimestamp(float(user.password_expiration_epoch))
    db.commit()


def logout(db: alchemy, token: str):
    session: Session = db.query(Session).filter(Session.token == token)
    db.add(Session(token=token, user_id=session.user_id))
    user: User = db.query(User).get(session.user_id)
    user.last_logout_datetime, user.last_logout_epoch = current_datetime_epoch()
    session.delete()
    db.commit()


def fail_login(db: alchemy, user: User) -> int:
    settings = get_settings(db)
    user.failed_login_number += 1
    user.is_enabled = user.failed_login_number + 1 < settings.failed_login_maximum_number
    db.commit()
    return settings.failed_login_maximum_number - user.failed_login_number


def login(db: alchemy, user: User) -> str:
    token = create_token()
    db.add(Session(token=token, user_id=user.id))
    user.failed_login_number = 0
    db.commit()
    return token


def get_settings(db: alchemy) -> AuthSettings:
    return db.query(AuthSettings).order_by(AuthSettings.creation_datetime.desc()).first()


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
