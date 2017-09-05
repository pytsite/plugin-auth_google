"""PytSite Google Auth Driver Plugin Event Handlers
"""
from pytsite import metatag as _metatag, settings as _settings, auth as _auth, router as _router, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    if _settings.get('auth_google.client_id'):
        _metatag.t_set('google-signin-client_id', _settings.get('auth_google.client_id'))

    c_user = _auth.get_current_user()
    if not (_settings.get('auth_google.client_id') and _settings.get('auth_google.client_secret')) \
            and c_user.has_permission('auth_google.settings.manage'):
        _router.session().add_warning_message(_lang.t('auth_google@plugin_setup_required_warning'))

    if _settings.get('auth_google.client_id'):
        _metatag.t_set('pytsite-auth-google-client-id', _settings.get('auth_google.client_id'))
