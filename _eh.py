"""PytSite Google Auth Driver Plugin Event Handlers
"""
from pytsite import metatag as _metatag, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    if _settings.get('google.client_id'):
        _metatag.t_set('google-signin-client_id', _settings.get('google.client_id'))
