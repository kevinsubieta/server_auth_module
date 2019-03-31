from database.db import transaction
from service.endpoints import Handler
from service.utils import str_to_auth_settings


class CreateAuthHandler(Handler):
    def post(self):
        auth_settings = str_to_auth_settings(self.get_argument('auth_settings'))
        with transaction() as db:
            db.add(auth_settings)
            db.commit()
        self.res(dict(success=True))
