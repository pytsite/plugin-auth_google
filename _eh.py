"""PytSite Auth Google Plugin Event Handlers.
"""
from pytsite import settings as _settings, auth as _auth, lang as _lang, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    c_user = _auth.get_current_user()
    if not _settings.get('auth_google.client_id') and c_user.has_permission('auth_google.settings.manage'):
        msg = _lang.t('auth_google@plugin_setup_required_warning')
        _router.session().add_warning_message(msg)
