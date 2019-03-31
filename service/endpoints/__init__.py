import json
from typing import Optional, Awaitable

from tornado.web import RequestHandler

from service.constants import ERROR


class Handler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def error(self, msg):
        self.write(json.dumps({'response': '', 'error': msg}))

    def respond(self, obj):
        self.write(json.dumps({'response': obj, 'error': ''}))

    def res(self, data: dict):
        if ERROR not in data:
            data['error'] = str()
        self.write(json.dumps(data))
