from sqlalchemy.exc import IntegrityError

from database.db import transaction
from repository.user_repo import get_user_by_username_password, change_password, insert_user, password_exists, get_settings
from service.constants import WRONG_USERNAME_PASSWORD, PASSWORD_USED
from service.endpoints import Handler
from service.utils import str_to_user, encrypt_user_password


class UserCreateHandler(Handler):
    def post(self):
        user = encrypt_user_password(str_to_user(self.get_argument('user')))
        try:
            with transaction() as db:
                user_id = insert_user(db, user)
            self.res(dict(user_id=user_id))
        except IntegrityError as e:
            self.error('the username is already in used, choose other')


class UserUpdatePasswordHandler(Handler):
    def post(self):
        username = self.get_argument('username')
        old_password = self.get_argument('old_password')
        new_password = self.get_argument('new_password')

        with transaction() as db:
            user = get_user_by_username_password(db, username, old_password)
            if user is None:
                self.error(WRONG_USERNAME_PASSWORD)
            else:
                if password_exists(db, user.id, new_password):
                    self.error(PASSWORD_USED)
                else:
                    settings = get_settings(db)
                    change_password(db, user, new_password, settings)
                    self.res(dict(success=True))
