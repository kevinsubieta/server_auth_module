import json
from hashlib import sha512

from flask import request, Blueprint

from database.db import transaction
from endpoints.utils import str_to_user

user_api = Blueprint('user_api', __name__, url_prefix='/user')


@user_api.route('/', methods=['PUT'])
def create_user():
    user = str_to_user(request.args['user'])
    user.password = sha512(user.password.encode()).hexdigest()
    with transaction() as db:
        db.add(user)
        db.commit()
        user_id = user.id
    return json.dumps({'user_id': user_id})
