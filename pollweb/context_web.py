from pollapi.context_interface import ContextInterface
import os


class ContextWeb(ContextInterface):

    def __init__(self):
        super().__init__()
        self._get_configuration()

    def get_url(self):
        return self._url

    def _set_url(self, url):
        self._url = url

    def _get_configuration(self):
        self._set_url(os.environ.get('NEXTCLOUD_URL'))
