"""PytSite Google Authentication Driver Plugin Settings Form
"""
from pytsite import lang as _lang, reload as _reload
from plugins import widget as _widget, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    def _on_setup_widgets(self):
        """Hook
        """
        self.add_widget(_widget.input.Text(
            uid='setting_client_id',
            weight=10,
            label=_lang.t('auth_google@client_id'),
            required=True,
            help=_lang.t('auth_google@client_id_setup_help'),
        ))

        self.add_widget(_widget.input.Text(
            uid='setting_client_secret',
            weight=20,
            label=_lang.t('auth_google@client_secret'),
            required=True,
            help=_lang.t('auth_google@client_secret_setup_help'),
        ))

        super()._on_setup_widgets()

    def _on_submit(self):
        _reload.set_flag()

        return super()._on_submit()
