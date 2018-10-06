"""PytSite Google Authentication Driver Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import requests as _requests
from pytsite import lang as _lang
from plugins import auth as _auth, file as _file
from . import _api, _error


class Auth(_auth.driver.Authentication):
    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'google'

    def get_description(self) -> str:
        """Get description of the driver
        """
        return 'Google'

    def sign_in(self, data: dict) -> _auth.model.AbstractUser:
        """Authenticate user
        """
        try:
            _api.get_client_id()
        except _error.ClientIdNotDefined as e:
            raise _auth.error.AuthenticationError(str(e))

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

        except _auth.error.UserNotFound:
            # Try to create new user
            if not _auth.is_sign_up_enabled():
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
            user.nickname = user.first_last_name

        user.save()

        return user

    def sign_up(self, data: dict) -> _auth.model.AbstractUser:
        """Register new user.
        """
        return self.sign_in(data)

    def sign_out(self, user: _auth.model.AbstractUser):
        """Sign out user
        """
        pass
