from flask import Blueprint, render_template

auth_api = Blueprint('auth_api', __name__, )


@auth_api.route("/login", methods=['POST'])
def login():

    return 'hello world!'
    # return render_template('encrypt_decrypt.html')


@auth_api.route("/logout", methods=['POST'])
def logout():
    return render_template('encrypt_decrypt.html')
