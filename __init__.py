"""PytSite Google Authentication Driver Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._api import get_client_id, get_authorization_url, get_client_secret, get_user_credentials, create_oauth2_flow


def plugin_load_wsgi():
    from pytsite import lang
    from plugins import auth
    from . import _driver

    lang.register_package(__name__)
    auth.register_auth_driver(_driver.Auth())
