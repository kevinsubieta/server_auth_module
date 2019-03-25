MIN_PASSWORD_MSG = 'Password\'s length must greater or equal to %s'
MAX_PASSWORD_MSG = 'Password\'s length must lower or equal to %s'
VALID = 'valid'


def validate_password(password: str, min_len: int, max_len: int):
    if len(password) > max_len:
        return MAX_PASSWORD_MSG % max_len
    return MIN_PASSWORD_MSG % min_len if len(password) < min_len else VALID
