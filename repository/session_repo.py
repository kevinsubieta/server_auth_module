from sqlalchemy.orm import Session as alchemy

from application.auth import create_token
from domain.models import Session, User
from repository.auth_settings_repo import get_settings
from repository.utils import current_datetime_epoch


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
