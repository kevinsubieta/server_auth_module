import os

from flask import Flask

from database.db import DB
from endpoints.auth import auth_api
from endpoints.user import user_api

app = Flask(__name__)

app.register_blueprint(auth_api)
app.register_blueprint(user_api)


def setup(config):
    settings = config['server:main']
    host = settings['listen'].split(':')
    port = int(host[-1])
    address = host[0]
    DB.read(config)
    DB.create_tables(config)
    return address, port
