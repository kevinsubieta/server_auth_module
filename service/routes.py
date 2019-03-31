from service.endpoints.security import CreateAuthHandler, GetAuthHandler
from service.endpoints.session import LoginHandler, LogoutHandler
from service.endpoints.user import UserCreateHandler, UserUpdatePasswordHandler

routes = [
    (r"/user/create", UserCreateHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/user/update/password", UserUpdatePasswordHandler),
    (r"/auth_settings/update", CreateAuthHandler),
    (r"/auth_settings/get", GetAuthHandler),
]
