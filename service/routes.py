from service.endpoints.auth import LoginHandler, LogoutHandler
from service.endpoints.user import UserCreateHandler, UserUpdatePasswordHandler

routes = [
    (r"/user/create", UserCreateHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/user/update/password", UserUpdatePasswordHandler)
]
