from pollapi.context_interface import ContextInterface
import os


class ContextWebapp(ContextInterface):

    def __init__(self):
        super().__init__()
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
        self._set_username(os.environ.get('NEXTCLOUD_USERNAME'))
        self._set_password(os.environ.get('NEXTCLOUD_PASSWORD'))
        self._set_url(os.environ.get('NEXTCLOUD_URL'))
