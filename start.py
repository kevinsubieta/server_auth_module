from configparser import ConfigParser

from service import setup, app

if __name__ == '__main__':
    config = ConfigParser()
    config.read('settings.ini')
    host, port = setup(config)
    app.run(host=host, port=port)
    app.run()
