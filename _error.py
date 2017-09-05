"""PytSite Auth Google Plugin Errors
"""
from pytsite import auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ClientIdNotDefined(Exception):
    def __str__(self) -> str:
        return 'Client ID is not defined'


class ClientSecretNotDefined(Exception):
    def __str__(self) -> str:
        return 'Client secret is not defined'


class UserCredentialsNotFound(Exception):
    def __init__(self, user: _auth.model.AbstractUser):
        self._user = user
        super().__init__()

    def __str__(self) -> str:
        return 'User {} does not have stored Google credentials'.format(self._user.login)
