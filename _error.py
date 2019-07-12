"""PytSite Google Authentication Driver Plugin Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import auth


class ClientIdNotDefined(Exception):
    def __str__(self) -> str:
        return "You should set configuration parameter 'auth_google.client_id'. " \
               "See details at https://developers.google.com/identity/sign-in/web/devconsole-project"


class ClientSecretNotDefined(Exception):
    def __str__(self) -> str:
        return "You should set configuration parameter 'auth_google.client_secret'. " \
               "See details at https://developers.google.com/identity/sign-in/web/devconsole-project"


class UserCredentialsNotFound(Exception):
    def __init__(self, user: auth.model.AbstractUser):
        self._user = user
        super().__init__()

    def __str__(self) -> str:
        return 'User {} does not have stored Google credentials'.format(self._user.login)
