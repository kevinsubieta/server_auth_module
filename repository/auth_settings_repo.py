from sqlalchemy.orm import Session as alchemy

from domain.models import AuthSettings


def get_settings(db: alchemy) -> AuthSettings:
    return db.query(AuthSettings).order_by(AuthSettings.creation_datetime.desc()).first()