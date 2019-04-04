import string

ERROR = 'error'
WRONG_USERNAME_PASSWORD = 'Username or password wrong!'
FAILED_LOGIN = 'Wrong Username or password, %s tries remaining'
MUST_CHANGE_PASSWORD = 'You must change your password'
DISABLED_USER = 'Disabled User'
PASSWORD_USED = 'Password used'
NOT_AUTHORIZED = 'Not authorized'
VALID = 'valid'
PASSWORD_TOO_SHORT = 'Password must have at least %s characters'
FEW_SPECIALS = 'Password must contain at least %s different special characters or numbers'
FEW_UPPERCASE = 'Password must contain at least %s different uppercase letters'
SPECIAL_CHARS = string.printable[:10] + string.printable[52:94]
UPPERCASE_LETTERS = string.printable[36:62]
USER_NOT_FOUND = 'User not found'
