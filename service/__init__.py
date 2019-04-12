from flask import Flask

from repository import DB
from service.f_endpoints.user import user_api

app = Flask(__name__)

app.register_blueprint(user_api)


def setup(config):
    settings = config['server:main']
    host = settings['listen'].split(':')
    port = int(host[-1])
    address = host[0]
    DB.read(config)
    return address, port
