"""PytSite Google Authentication Driver Plugin
"""
from ._api import get_user_credentials

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth, lang, assetman, settings, router, permissions
    from . import _driver, _eh, _settings_form, _controllers

    # Language resources
    lang.register_package(__name__, alias='auth_google')
    lang.register_global('auth_google_admin_settings_url', lambda language, args: settings.form_url('auth_google'))

    # Assets
    assetman.register_package(__name__, alias='auth_google')
    assetman.t_less(__name__ + '@css/**', 'css')
    assetman.t_js(__name__ + '@js/**', 'js')
    assetman.js_module('auth-google-widget', __name__ + '@js/auth-google-widget')

    # Permissions
    permissions.define_permission('auth_google.settings.manage', 'auth_google@manage_auth_google_settings', 'app')

    # Settings
    settings.define('auth_google', _settings_form.Form, 'auth_google@auth_google', 'fa fa-google',
                    'auth_google.settings.manage')

    # Event handlers
    router.on_dispatch(_eh.router_dispatch)

    # Auth driver
    client_id = settings.get('auth_google.client_id')
    if client_id:
        auth.register_auth_driver(_driver.Google(client_id))

    # Routes
    router.handle(_controllers.Authorization(), '/auth_google/authorization', 'auth_google@authorization',
                  filters='pytsite.auth_web@authorize')


_init()
