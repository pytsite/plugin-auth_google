"""PytSite Google Authentication Driver.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth, lang, assetman, settings, events, permissions
    from . import _driver, _settings_form, _eh

    # Resources
    lang.register_package(__name__, alias='auth_google')
    lang.register_global('auth_google_admin_settings_url', lambda: settings.form_url('auth_google'))
    assetman.register_package(__name__, alias='auth_google')

    # Permissions
    permissions.define_permission('auth_google.settings.manage', 'auth_google@manage_auth_google_settings', 'app')

    # Settings
    settings.define('auth_google', _settings_form.Form, 'auth_google@google_authentication', 'fa fa-google',
                    'auth_google.settings.manage')

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)

    # Authentication driver
    client_id = settings.get('auth_google.client_id')
    if client_id:
        auth.register_auth_driver(_driver.Google(client_id))


_init()
