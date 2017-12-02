"""PytSite Google Authentication Driver Plugin
"""
from . import _error as error
from ._api import get_client_id, get_authorization_url, get_client_secret, get_user_credentials, create_oauth2_flow

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang
    from plugins import auth
    from . import _driver

    try:
        auth.register_auth_driver(_driver.Auth(get_client_id()))
        lang.register_package(__name__)
    except error.ClientIdNotDefined:
        pass


_init()
