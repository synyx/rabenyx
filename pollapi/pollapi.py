import pkg_resources
import requests

try:
    version = pkg_resources.require('rabenyx')[0].version
except pkg_resources.DistributionNotFound:
    version = '1.0'


class PollApi:

    API_PATH = '/index.php/apps/polls/api/v1.0'
    HEADERS = {
        "User-Agent": f"Rabenyx/{version}",
        "Accept": "application/json",
    }
    TIMEOUT_SEC = 4.0

    def __init__(self, context):
        self.username = context.get_username()
        self.password = context.get_password()
        self.url = context.get_url()

    def __get(self, endpoint):
        url = self.url + self.API_PATH + endpoint
        auth = (self.username, self.password)
        result = requests.get(url, headers=self.HEADERS, auth=auth, timeout=self.TIMEOUT_SEC)
        result.raise_for_status()
        if result.status_code == 200:
            return result.json()

    def __post(self, endpoint, payload=None):
        url = self.url + self.API_PATH + endpoint
        auth = (self.username, self.password)
        result = requests.post(url, json=payload, headers=self.HEADERS, auth=auth, timeout=self.TIMEOUT_SEC)
        result.raise_for_status()
        if result.status_code == 200 or result.status_code == 201:
            return result.json()

    def __put(self, endpoint, payload):
        url = self.url + self.API_PATH + endpoint
        auth = (self.username, self.password)
        result = requests.put(url, json=payload, headers=self.HEADERS, auth=auth, timeout=self.TIMEOUT_SEC)
        result.raise_for_status()
        if result.status_code == 200:
            return result.json()

    def get_poll(self):
        endpoint = "/polls"
        result = self.__get(endpoint)
        for x in result['polls']:
            print(format(x.get('id')) + ": " + x.get('title'))
        return result['polls']

    def get_poll_by_id(self, poll_id):
        endpoint = f"/poll/{poll_id}"
        result = self.__get(endpoint)
        print(result)
        return result['poll']

    def get_poll_by_title(self, poll_title):
        endpoint = "/polls"
        result = self.__get(endpoint)
        for poll in result['polls']:
            if poll.get('title') == poll_title:
                print(poll.get('id'))

    def get_votes(self, poll_id):
        endpoint = f"/poll/{poll_id}/votes"
        print(endpoint)
        result = self.__get(endpoint)
        for x in result['votes']:
            user = x.get('user')
            print(user.get('userId') + " | " + x.get('optionText'))
        return result['votes']

    def get_votes_by_userid(self, poll_id, vote_userid):
        endpoint = f"/poll/{poll_id}/votes"
        result = self.__get(endpoint)
        for vote in result['votes']:
            user = vote.get('user')
            if user.get('userId') == vote_userid:
                print(vote.get('optionId'))

    def update_vote_answer(self, vote_id, vote_answer):
        endpoint = "/vote"
        payload = {"optionId": vote_id, "setTo": vote_answer}
        result = self.__post(endpoint, payload)
        print("Answered with " + vote_answer + ".")

    def add_poll(self, poll_type, poll_title):
        endpoint = "/poll"
        payload = {"type": poll_type, "title": poll_title}
        result = self.__post(endpoint, payload)
        print(result)

    def get_options(self, poll_id, return_text=False):
        endpoint = f"/poll/{poll_id}/options"
        result = self.__get(endpoint)
        if return_text:
            for option in result['options']:
                print(option.get('text'))
        else:
            print(result)
        return result

    def clone_options(self, from_poll_id, to_poll_id):
        source_options = self.get_options(from_poll_id)
        for x in source_options["options"]:
            self.add_option(to_poll_id, x.get('text'))
        print("All options cloned")

    def clone_poll(self, poll_id, return_id=False):
        endpoint = f"/poll/{poll_id}/clone"
        result = self.__post(endpoint)
        if return_id:
            print(result['poll'].get('id'))
        else:
            print(result)

    def add_option(self, poll_id, option):
        endpoint = f"/poll/{poll_id}/option"
        payload = {"pollOptionText": option}
        result = self.__post(endpoint, payload)
        print(result)

    def update_poll_title(self, poll_id, poll_title):
        endpoint = f"/poll/{poll_id}"
        payload = {"poll": {"title": poll_title}}
        result = self.__put(endpoint, payload)
        print(result)

    def update_poll_expire(self, poll_id, poll_expire):
        endpoint = f"/poll/{poll_id}"
        payload = {"poll": {"expire": poll_expire}}
        result = self.__put(endpoint, payload)
        print(result)

    def update_poll_access(self, poll_id, poll_access):
        endpoint = f"/poll/{poll_id}"
        payload = {"poll": {"access": poll_access}}
        result = self.__put(endpoint, payload)
        print(result)

    def update_poll_deleted(self, poll_id, poll_deleted):
        endpoint = f"/poll/{poll_id}"
        payload = {"poll": {"deleted": poll_deleted}}
        result = self.__put(endpoint, payload)
        print(result)

    def add_email_share(self, poll_id, user_id):
        endpoint = "/share"
        payload = {"pollId": poll_id, "type": "email", "userId": user_id}
        result = self.__post(endpoint, payload)
        print(result)
        return result['share']

    def get_email_shares(self, poll_id):
        endpoint = f"/poll/{poll_id}/shares"
        result = self.__get(endpoint)
        return result

    def get_share(self, poll_id, user_id):
        shares = self.get_email_shares(poll_id)
        for share in shares['shares']:
            if share.get('userId') == user_id:
                return share

        return False
