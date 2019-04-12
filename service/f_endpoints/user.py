import json

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from adapters.user_adapters import str_to_user
from application.user import validate
from domain.constants import VALID, UserAuthErrors, USER_NOT_FOUND
from domain.models import User
from repository import transaction
from repository.auth_settings_repo import get_settings
from repository.user_repo import is_admin, insert_user, enable_user
from service.utils import verify_basic_auth, basic_auth

user_api = Blueprint('user_api', __name__, url_prefix='/user')


def create_respond(user_id=None, error: str = None) -> dict:
    return json.dumps(dict(user_id=user_id, error=error))


@basic_auth
@user_api.route("/create", methods=['POST'])
def create():
    user: User = str_to_user(request.args.get('user'))
    token = request.args.get('token')
    try:
        with transaction() as db:
            if not verify_basic_auth(request) or not is_admin(db, token):
                return create_respond(error=UserAuthErrors.NOT_AUTHORIZED)
            msg = validate(user, get_settings(db), user.password, db)
            return create_respond(insert_user(db, user)) if msg == VALID else create_respond(error=msg)
    except IntegrityError:
        return create_respond(error='the username is already in used, choose other')


def update_respond(error: str = None) -> dict:
    return json.dumps(dict(success=error is None or len(error) == 0, error=error))


@user_api.route("/update/enable", methods=['POST'])
def enable():
    username = request.args.get('username')
    to_enable = request.args.get('to_enable')
    token = request.args.get('token')
    try:
        with transaction() as db:
            if not verify_basic_auth(request) or not is_admin(db, token):
                return create_respond(error=UserAuthErrors.NOT_AUTHORIZED)
            return update_respond(USER_NOT_FOUND) if not enable_user(db, username, to_enable == '1') else update_respond()
    except IntegrityError as e:
        return update_respond('Internal Error')


@user_api.route("/reset/password", methods=['POST'])
def reset():
    if not self.is_authenticated():
        return
    username = self.get_argument('username')
    new_password = self.get_argument('new_password')
    token = self.get_argument('token')
    try:
        with transaction() as db:
            if is_admin(db, token):
                user = get_user_by_username(db, username)
                response = validate(user, get_settings(db), new_password, db)
                if response['success']:
                    change_password(db, user, new_password, get_settings(db))
                self.res(response)
            else:
                self.error(NOT_AUTHORIZED)
    except IntegrityError as e:
        self.error('Internal Error')
