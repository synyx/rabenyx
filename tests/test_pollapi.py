import responses

from rvalidator import validate_request
from pollapi.pollapi import PollApi
from pollapi.context_interface import ContextInterface


class _TestContext(ContextInterface):
    def __init__(self, username: str, password: str, url: str):
        super().__init__()
        self._username = username
        self._password = password
        self._url = url


config = _TestContext('test', 'test', 'https://example.com')


@responses.activate
@validate_request
def test_get_poll(capsys):
    responses.add(responses.GET, config.get_url() + PollApi.API_PATH + '/polls',
                  json={'polls': [{'id': 1, 'title': 'test', 'type': 'datePoll'}]}, status=200)

    api = PollApi(config)
    api.get_poll()
    assert "1: test" in capsys.readouterr().out


@responses.activate
@validate_request
def test_get_poll_by_title(capsys):
    responses.add(responses.GET, config.get_url() + PollApi.API_PATH + '/polls',
                  json={'polls': [{'id': 1, 'type': 'textPoll', 'title': 'How are you on 20.09.2021?'}]}, status=200)

    api = PollApi(config)
    api.get_poll_by_title('How are you on 20.09.2021?')
    assert "1" in capsys.readouterr().out


@responses.activate
@validate_request
def test_get_poll_by_id(capsys):
    responses.add(responses.GET, config.get_url() + PollApi.API_PATH + '/poll/1',
                  json={'poll': {'id': 1, 'type': 'textPoll', 'title': 'How are you on 24.01.2022?'}}, status=200)

    api = PollApi(config)
    api.get_poll_by_id(1)
    assert "24.01.2022" in capsys.readouterr().out


@responses.activate
@validate_request
def test_get_votes(capsys):
    responses.add(responses.GET, config.get_url() + PollApi.API_PATH + '/poll/1/votes',
                  json={'votes': [{'id': 1, 'user': {'userId': 'uid'}, 'optionId': 2, 'optionText': 'eggplant'}]},
                  status=200)

    api = PollApi(config)
    api.get_votes(1)
    assert "uid | eggplant" in capsys.readouterr().out

    api.get_votes_by_userid(1, 'uid')
    assert "2" in capsys.readouterr().out


@responses.activate
@validate_request
def test_update_vote(capsys):
    responses.add(responses.POST, config.get_url() + PollApi.API_PATH + '/vote',
                  json={'votes': [{'id': 1, 'user': {'userId': 'someone'}, 'optionText': 'Will you?', 'voteAnswer': 'no'}]},
                  status=200)

    api = PollApi(config)
    api.update_vote_answer(1, 'no')
    assert "Answered with no." in capsys.readouterr().out


@responses.activate
@validate_request
def test_add_poll(capsys):
    responses.add(responses.POST, config.get_url() + PollApi.API_PATH + '/poll',
                  json={'poll': {'type': 'textPoll', 'title': 'How are you?'}}, status=201)

    api = PollApi(config)
    api.add_poll("textPoll", "How are you?")
    assert "How are you?" in capsys.readouterr().out


@responses.activate
@validate_request
def test_clone_poll(capsys):
    responses.add(responses.POST, config.get_url() + PollApi.API_PATH + '/poll/1/clone',
                  json={'poll': {'id': 1, 'type': 'textPoll', 'title': 'Clone of How are you?'}}, status=201)

    api = PollApi(config)
    api.clone_poll(1)
    assert "Clone of How are you?" in capsys.readouterr().out

    api.clone_poll(1, True)
    assert "1" in capsys.readouterr().out


@responses.activate
@validate_request
def test_add_option(capsys):
    responses.add(responses.POST, config.get_url() + PollApi.API_PATH + '/poll/1/option',
                  json={"option": {"id": 1, "pollId": 1, "text": "I'm fine!"}}, status=201)

    api = PollApi(config)
    api.add_option(1, "I'm fine!")
    assert "I'm fine!" in capsys.readouterr().out


@responses.activate
@validate_request
def test_get_options(capsys):
    responses.add(responses.GET, config.get_url() + PollApi.API_PATH + '/poll/1/options',
                  json={"options": [{"id": 1, "pollId": 2, "text": "I'm fine!"},
                                    {"id": 2, "pollId": 2, "text": "I'm still fine!"}]}, status=200)

    api = PollApi(config)
    api.get_options(1)
    stdout = capsys.readouterr().out
    assert "2" in stdout
    assert "I'm fine!" in stdout
    assert "I'm still fine!" in stdout

    api.get_options(1, True)
    stdout = capsys.readouterr().out
    assert "I'm fine!" in stdout
    assert "I'm still fine!" in stdout


@responses.activate
@validate_request
def test_clone_options(capsys):
    responses.add(responses.POST, config.get_url() + PollApi.API_PATH + '/poll/1/clone',
                  json={'poll': {'id': 2, 'type': 'textPoll', 'title': 'Clone of How are you?'}}, status=201)
    responses.add(responses.GET, config.get_url() + PollApi.API_PATH + '/poll/1/options',
                  json={"options": [{"id": 1, "pollId": 2, "text": "I'm fine!"},
                                    {"id": 2, "pollId": 2, "text": "I'm still fine!"}]}, status=200)
    responses.add(responses.POST, config.get_url() + PollApi.API_PATH + '/poll/2/option',
                  json={"pollId": 2, "text": "I'm fine!"}, status=201)
    responses.add(responses.POST, config.get_url() + PollApi.API_PATH + '/poll/2/option',
                  json={"pollId": 2, "text": "I'm still fine!"}, status=201)

    api = PollApi(config)
    api.clone_poll(1, True)
    api.clone_options(from_poll_id=1, to_poll_id=2)
    assert "All options cloned" in capsys.readouterr().out
    assert len(responses.calls) == 4
    assert responses.calls[2].response.json()['text'] == "I'm fine!"
    assert responses.calls[3].response.json()['text'] == "I'm still fine!"


@responses.activate
@validate_request
def test_update_poll(capsys):
    responses.add(responses.PUT, config.get_url() + PollApi.API_PATH + '/poll/1',
                  json={'poll': {'id': 1, 'type': 'textPoll', 'title': 'How are you now?', 'expire': 1631549334,
                                 'access': 'public', 'deleted': 1631549335}},
                  status=200)

    api = PollApi(config)
    api.update_poll_title(1, "How are you now?")
    assert "How are you now?" in capsys.readouterr().out

    api.update_poll_expire(1, 1631549334)
    assert "1631549334" in capsys.readouterr().out

    api.update_poll_access(1, "public")
    assert "public" in capsys.readouterr().out

    api.update_poll_deleted(1, 1631549335)
    assert "deleted" in capsys.readouterr().out


@responses.activate
@validate_request
def test_add_email_share(capsys):
    responses.add(responses.POST, config.get_url() + PollApi.API_PATH + '/share',
                  json={"share": {"pollId": 1, "type": "email", "userId": "someone"}}, status=201)

    api = PollApi(config)
    api.add_email_share(1, "someone")
    assert "someone" in capsys.readouterr().out
