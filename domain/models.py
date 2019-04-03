from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String, DateTime, Boolean, ForeignKey, Date, BigInteger)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    id_number = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email_address = Column(String(200), nullable=False)
    birthday = Column(Date, nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    failed_login_number = Column(Integer, nullable=False, default=0)
    creation_datetime = Column(DateTime, default=datetime.now)
    update_datetime = Column(DateTime, default=datetime.now)
    password_expiration_datetime = Column(DateTime)
    password_expiration_epoch = Column(Integer)
    session_expiration_datetime = Column(DateTime)
    session_expiration_epoch = Column(Integer)
    last_password_change_datetime = Column(DateTime)
    last_password_change_epoch = Column(Integer)
    last_logout_datetime = Column(DateTime)
    last_logout_epoch = Column(DateTime)
    password_expire = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    is_enabled = Column(Boolean, nullable=False, default=True)
    must_change_password = Column(Boolean, nullable=False, default=True)


class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    token = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class UsedPassword(Base):
    __tablename__ = 'used_password'
    id = Column(Integer, primary_key=True)
    password = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class AuthSettings(Base):
    __tablename__ = 'auth_settings'
    id = Column(Integer, primary_key=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    failed_login_maximum_number = Column(Integer, nullable=False)
    password_expiration_epoch = Column(BigInteger, nullable=False)  # epoch
    session_expiration_epoch = Column(BigInteger, nullable=False)  # months days minutes
    simultaneous_sessions_nro_allowed = Column(Integer, nullable=False)
    min_special_letters_number = Column(Integer, nullable=False)
    min_uppercase_letters_number = Column(Integer, nullable=False)
    min_password_len = Column(Integer, nullable=False)
