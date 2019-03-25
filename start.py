from configparser import ConfigParser

from endpoints.web import setup, app

if __name__ == '__main__':
    config = ConfigParser()
    config.read('settings.ini')
    host, port = setup(config)
    # context = ('cert.crt', 'key.key')
    # app.run(host=host, port=port, ssl_context=context)
    app.run(host=host, port=port)
    app.run()
