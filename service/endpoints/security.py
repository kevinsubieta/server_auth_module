from repository import transaction
from repository.user_repo import is_admin
from repository.auth_settings_repo import get_settings
from domain.constants import NOT_AUTHORIZED
from service.endpoints import Handler
from adapters.auth_settings_adapters import str_to_auth_settings


class CreateAuthHandler(Handler):
    def post(self):
        if not self.is_authenticated():
            return
        token = self.get_argument('token')
        auth_settings = str_to_auth_settings(self.get_argument('auth_settings'))
        with transaction() as db:
            if is_admin(db, token):
                db.add(auth_settings)
                db.commit()
                self.res(dict(success=True))
            else:
                self.error(NOT_AUTHORIZED)


class GetAuthHandler(Handler):
    def post(self):
        if not self.is_authenticated():
            return
        token = self.get_argument('token')
        with transaction() as db:
            if is_admin(db, token):
                auth = get_settings(db)
                response = dict(auth.__dict__)
                response.pop('_sa_instance_state', None)
                response.pop('creation_datetime', None)
                response.pop('id', None)
                self.res(response)
            else:
                self.error(NOT_AUTHORIZED)
