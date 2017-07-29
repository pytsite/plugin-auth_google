"""PytSite Google Authentication Driver Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth, lang, assetman, settings, router
    from . import _driver, _eh

    # Resources
    lang.register_package(__name__, alias='auth_google')

    assetman.register_package(__name__, alias='auth_google')
    assetman.t_less(__name__ + '@css/**', 'css')
    assetman.t_js(__name__ + '@js/**', 'js')
    assetman.js_module('auth-google-widget', __name__ + '@js/auth-google-widget')

    client_id = settings.get('google.client_id')
    if client_id:
        auth.register_auth_driver(_driver.Google(client_id))
        router.on_dispatch(_eh.router_dispatch)


_init()
