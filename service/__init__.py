import tornado.web

from database.db import DB
from service.routes import routes


class AppMaker:
    port = int()
    address = str()

    @classmethod
    def create(cls, config):
        settings = config['server:main']
        host = settings['listen'].split(':')
        cls.port = int(host[-1])
        cls.address = host[0]
        DB.read(config)
        app = tornado.web.Application(routes, **settings)
        app.listen(cls.port, cls.address)
