import base64
import json
from typing import Optional, Awaitable

from tornado.web import RequestHandler

from service.constants import ERROR, NOT_AUTHORIZED

USER_AUTH = "Vk7iBxhuaYZSCncLIbZazA==Cz8hZS/sv70ZgG7G01DhWQ=="
TOKEN_AUTH = "2a10YEm0utdWochklUhh8zZ78.SghQhV48VDem1voeO9yDihEHI2vA1US"


class Handler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def error(self, msg):
        self.write(json.dumps(dict(success=False, error=msg)))

    def res(self, data: dict):
        if ERROR not in data:
            data['error'] = str()
        self.write(json.dumps(data))

    def is_authenticated(self):
        auth_header = self.request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return False
        username, password = base64.b64decode(auth_header.split(None, 1)[-1]).decode('ascii').split(':', 1)
        is_authenticated = username == USER_AUTH and TOKEN_AUTH == password
        if not is_authenticated:
            self.error(NOT_AUTHORIZED)
        return is_authenticated
