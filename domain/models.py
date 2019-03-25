from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String, DateTime, Boolean, ForeignKey, Date)
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
    session_expiration_datetime = Column(DateTime)
    last_password_change_datetime = Column(DateTime)
    last_logout_datetime = Column(DateTime)
    password_expire = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    is_enabled = Column(Boolean, nullable=False, default=True)
    token = Column(String(200))


class UsedPassword(Base):
    __tablename__ = 'used_password'
    id = Column(Integer, primary_key=True)
    password = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class AuthSettings(Base):
    __tablename__ = 'auth_settings'
    id = Column(Integer, primary_key=True)
    failed_login_maximum_number = Column(Integer, nullable=False)
    password_expiration_time_days = Column(Integer, nullable=False)
    session_expiration_time_min = Column(Integer, nullable=False)
