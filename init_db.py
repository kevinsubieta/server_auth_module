from configparser import ConfigParser
from datetime import datetime
from importlib import import_module

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.auth import encrypt
from domain.models import AuthSettings, User

settings = ConfigParser()
settings.read('settings.ini')
m = import_module(settings['alembic']['models_location'] + '.models')
base = getattr(m, 'Base')
engine = create_engine(settings['alembic']['sqlalchemy.url'])
base.metadata.create_all(engine, checkfirst=True)
db = sessionmaker(bind=engine, autoflush=False)()
db.add(AuthSettings(
    failed_login_maximum_number=3,
    password_expiration_epoch=100000,
    session_expiration_epoch=100000,
    simultaneous_sessions_nro_allowed=1,
    min_special_letters_number=1,
    min_uppercase_letters_number=1,
    min_password_len=8
))
db.add(User(
    id_number='666666',
    name='Pedro',
    last_name='Yupanqui',
    email_address='pedroyupa@gmail.com',
    birthday=datetime(1985, 6, 17),
    username='pedroy',
    password=encrypt('Admin6543!'),
    password_expire=True,
    is_admin=True,
))
db.commit()
