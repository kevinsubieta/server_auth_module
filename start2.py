from configparser import ConfigParser

from tornado.ioloop import IOLoop

from database.db import DB
from service import AppMaker as Maker


def main():
    config = ConfigParser()
    config.read('settings2.ini')
    Maker.create(config)
    t = 'running ... \nhttp://%s:%s/'
    DB.read(config)
    DB.create_tables(config)
    print(t % (Maker.address, Maker.port))
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        IOLoop.current().stop()


if __name__ == '__main__':
    main()
