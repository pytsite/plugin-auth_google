"""PytSite Auth Google Driver
"""
import requests as _requests
from pytsite import auth as _auth, form as _form, widget as _widget, html as _html, lang as _lang, \
    metatag as _metatag, file as _file, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _SignInWidget(_widget.Abstract):
    """Google Sign In Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-google-sign-in'
        self._data['client_id'] = kwargs.get('client_id', '')
        self._js_module = 'auth-google-widget'

    def _get_element(self, **kwargs) -> _html.Element:
        return _html.Div(uid=self.uid, css='button-container')


class _SignInForm(_form.Form):
    """Google Sign In Form
    """

    def __init__(self, **kwargs):
        """Init.
        """
        self._client_id = kwargs.get('client_id')
        super().__init__(**kwargs)
        self._nocache = True

    def _on_setup_widgets(self):
        self.add_widget(_widget.input.Hidden(self.uid + '-id-token', form_area='hidden'))
        self.add_widget(_SignInWidget(self.uid + '-google-button', client_id=self._client_id))

        # Submit button is not necessary, form submit performs by JS code
        self.remove_widget('action-submit')


class Google(_auth.driver.Authentication):
    def __init__(self, client_id: str):
        """Init.
        """
        self._client_id = client_id
        if not self._client_id:
            raise RuntimeError("You should set configuration parameter 'auth.google.client_id'. " +
                               "See details at https://developers.google.com/identity/sign-in/web/devconsole-project")

    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'google'

    def get_sign_up_form(self, **kwargs) -> _form.Form:
        """Get sign in form.
        """
        return self.get_sign_in_form(**kwargs)

    def get_sign_in_form(self, **kwargs) -> _form.Form:
        """Get sign in form.
        """
        _metatag.t_set('google-signin-client_id', self._client_id)

        return _SignInForm(client_id=self._client_id, **kwargs)

    def sign_in(self, data: dict) -> _auth.model.AbstractUser:
        """Authenticate user.
        """
        token = data.get('id_token')

        if not token:
            for k, v in data.items():
                if k.endswith('token'):
                    token = v
                    break

        if not token:
            raise ValueError("No ID token received")

        response = _requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo', params={
            'id_token': token,
        })

        # Parse response from Google
        google_data = response.json()

        # Check response status
        if response.status_code != 200:
            raise _auth.error.AuthenticationError('Google response: ' + google_data.get('error_description'))

        # Check email validness
        if google_data['email_verified'] != 'true':
            raise _auth.error.AuthenticationError("Email '{}' is not verified by Google".format(google_data['email']))

        # Try to load user
        try:
            user = _auth.get_user(google_data.get('email'))
            is_new_user = False

        except _auth.error.UserNotExist:
            # Try to create new user
            if not _settings.get('auth.signup_enabled'):
                raise _auth.error.AuthenticationError(_lang.t('auth_google@signup_is_disabled'))
            else:
                # New users can be created only by system user
                _auth.switch_user_to_system()

                # Create new user
                user = _auth.create_user(google_data.get('email'))
                is_new_user = True

        # As soon as user created or loaded, set it as current
        _auth.switch_user(user)

        # Picture
        if is_new_user and 'picture' in google_data and google_data['picture']:
            current_pic = user.picture
            user.picture = _file.create(google_data['picture'])
            current_pic.delete()

        # Name
        if not user.first_name:
            user.first_name = google_data.get('given_name')
        if not user.last_name:
            user.last_name = google_data.get('family_name')

        # Alter nickname
        if is_new_user:
            user.nickname = user.full_name

        user.save()

        return user

    def sign_up(self, data: dict) -> _auth.model.AbstractUser:
        """Register new user.
        """
        return self.sign_in(data)
