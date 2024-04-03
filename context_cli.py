import configparser
from pollapi.context_interface import ContextInterface
import os


class ContextCli(ContextInterface):

    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
        self._get_configuration()

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_url(self):
        return self._url

    def _set_username(self, username):
        self._username = username

    def _set_password(self, password):
        self._password = password

    def _set_url(self, url):
        self._url = url

    def _get_configuration(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)

        if not config.has_option('DEFAULT', 'username'):
            if not (os.environ.get('NEXTCLOUD_USERNAME') and os.environ.get('NEXTCLOUD_PASSWORD')
                    and os.environ.get('NEXTCLOUD_URL')):
                raise configparser.Error('Configuration error, please check your ini file or environment variables.')
            else:
                self._set_username(os.environ.get('NEXTCLOUD_USERNAME'))
                self._set_password(os.environ.get('NEXTCLOUD_PASSWORD'))
                self._set_url(os.environ.get('NEXTCLOUD_URL'))
        else:
            self._set_username(config.get('DEFAULT', 'username'))
            self._set_password(config.get('DEFAULT', 'password'))
            self._set_url(config.get('DEFAULT', 'url'))
