"""PytSite Google Authentication Driver Plugin API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union, List
from oauth2client import client as oauth2_client
from pytsite import router, reg
from plugins import auth
from . import _error


def get_client_id():
    """Get client ID from settings
    """
    client_id = reg.get('auth_google.client_id')
    if not client_id:
        raise _error.ClientIdNotDefined()

    return client_id


def get_client_secret():
    """Get client secret from settings
    """
    client_secret = reg.get('auth_google.client_secret')
    if not client_secret:
        raise _error.ClientSecretNotDefined()

    return client_secret


def create_oauth2_flow(scope: Union[str, List[str]] = None, redirect_uri: str = None, client_id: str = None,
                       client_secret: str = None, **kwargs):
    """Create OAuth2 web server flow
    """
    flow = oauth2_client.OAuth2WebServerFlow(client_id or get_client_id(), client_secret or get_client_secret(),
                                             scope or '', redirect_uri or router.current_url(), **kwargs)
    flow.params['access_type'] = 'offline'

    return flow


def get_user_credentials(user: auth.model.AbstractUser) -> oauth2_client.OAuth2Credentials:
    """Get user's Google credentials
    """
    if 'google_oauth2_credentials' not in user.options:
        raise _error.UserCredentialsNotFound(user)

    return oauth2_client.OAuth2Credentials.from_json(user.get_option('google_oauth2_credentials'))


def get_authorization_url(scope: Union[str, List[str]] = None):
    """Get URL of the PytSite's location which start process of requesting user authorization
    """
    rule_args = {}

    if isinstance(scope, list):
        rule_args['scope'] = ','.join(scope)
    elif isinstance(scope, str):
        rule_args['scope'] = scope

    return router.rule_url('auth_google@authorization', rule_args)
