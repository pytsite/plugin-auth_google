"""PytSite Google Authentication Driver Plugin Controllers
"""
from oauth2client.client import OAuth2WebServerFlow as _OAuth2WebServerFlow
from pytsite import routing as _routing, router as _router, lang as _lang
from plugins import auth as _auth
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Authorization(_routing.Controller):
    def exec(self):
        # Check for error from Google
        error = self.arg('error')
        if error == 'access_denied':
            raise self.forbidden(_lang.t('auth_google@user_declined_authorization'))

        # Check for code from Google
        code = self.arg('code')
        if code:
            # Restore flow from session
            flow = _router.session().get('google_oauth2_flow')  # type: _OAuth2WebServerFlow
            if not flow:
                raise self.forbidden('Cannot retrieve stored OAuth2 flow')

            # Exchange code to credentials
            credentials = flow.step2_exchange(code)
            user = _auth.get_current_user()
            user.set_option('google_oauth2_credentials', credentials.to_json())
            user.save()

            final_redirect = _router.session().get('google_oauth2_final_redirect', _router.base_url())

            _router.session().pop('google_oauth2_flow')
            _router.session().pop('google_oauth2_final_redirect')

            return self.redirect(final_redirect)

        else:
            # Request new code from Google
            scope = self.args.pop('scope')  # type: str
            if scope and ',' in scope:
                scope = scope.split(',')
            flow = _api.create_oauth2_flow(scope, _router.current_url(True, add_query=dict(self.args)))
            _router.session()['google_oauth2_flow'] = flow
            _router.session()['google_oauth2_final_redirect'] = self.args.pop('__redirect', _router.base_url())

            return self.redirect(flow.step1_get_authorize_url())
