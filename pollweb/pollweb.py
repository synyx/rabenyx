import re

import pkg_resources
import requests
from pollweb.context_web import ContextWeb

try:
    version = pkg_resources.require('rabenyx')[0].version
except pkg_resources.DistributionNotFound:
    version = '1.0'


class PollWeb:
    REQUEST_PATH = '/apps/polls'
    HEADERS = {
        "User-Agent": f"Rabenyx/{version}",
        "Accept": "application/json",
    }
    TIMEOUT_SEC = 4.0

    def __init__(self):
        context = ContextWeb()
        self.url = context.get_url()

    def get_headers(self, content):
        headers = self.HEADERS
        pattern = r'data-requesttoken=\"([^\"]+)\"'
        headers['requesttoken'] = re.search(pattern, content).group(1)

        return headers

    def get_login(self, token):
        url = self.url + self.REQUEST_PATH + '/s/' + token
        session = requests.Session()
        response = session.get(url, timeout=self.TIMEOUT_SEC)
        headers = self.get_headers(bytes.decode(response.content))

        login = {"session": session, "headers": headers}

        return login

    def add_external_voter(self, login, token, user_id, email_address):
        url = self.url + self.REQUEST_PATH + '/s/' + token + '/register'
        payload = {"userName": user_id, "emailAddress": email_address}
        result = login['session'].post(url, json=payload, headers=login['headers'], timeout=self.TIMEOUT_SEC)
        result.raise_for_status()
        if result.status_code == 201:
            return result.json()

    def add_external_vote(self, login, token, option_id, vote_answer):
        url = self.url + self.REQUEST_PATH + '/s/' + token + '/vote'
        payload = {"optionId": option_id, "setTo": vote_answer}
        result = login['session'].put(url, json=payload, headers=login['headers'], timeout=self.TIMEOUT_SEC)
        result.raise_for_status()
        if result.status_code == 200:
            return result.json()
