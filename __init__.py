"""PytSite Google Authentication Driver Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._api import get_client_id, get_authorization_url, get_client_secret, get_user_credentials, create_oauth2_flow


def plugin_load_wsgi():
    from plugins import auth
    from . import _driver

    auth.register_auth_driver(_driver.Auth())
