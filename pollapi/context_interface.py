class ContextInterface:

    def __init__(self):
        self._url = None
        self._password = None
        self._username = None

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_url(self):
        return self._url
