#!/usr/bin/env python3
import time
from datetime import date

import random
from flask import Flask, render_template, request, redirect
from pollapi.pollapi import PollApi
from polldb.polldb import PollDB, Answer
from pollweb.pollweb import PollWeb
from context_webapp import ContextWebapp

app = Flask(__name__)


@app.route("/")
def get_polls():
    context = ContextWebapp()
    api = PollApi(context)

    polls = api.get_poll()
    polls = filter(lambda p: ("Raumbelegung" in p.get('title') or "Anwesenheit" in p.get('title')), polls)
    polls = filter(lambda p: p.get('deleted') == 0, polls)
    polls = list(polls)
    polls.sort(key=lambda p: p.get('id'), reverse=True)

    today = date.today().strftime("%d.%m.%Y")

    return render_template("polls/index.html", polls=polls, today=today)


@app.route("/polls/<int:poll_id>")
def get_votes(poll_id):
    context = ContextWebapp()
    api = PollApi(context)

    votes = api.get_votes(poll_id)
    options = api.get_options(poll_id)

    return render_template("polls/votes.html", votes=votes,
                           options=options['options'], poll_id=poll_id)


@app.route("/health")
def get_health():
    return render_template("health/index.html")


@app.route("/<int:poll_id>/votes/add", methods=['POST'])
def add_vote(poll_id):
    context = ContextWebapp()
    api = PollApi(context)
    web = PollWeb()

    user_id = request.form.get('user_id')
    option_id = request.form.get('option_id')

    share = api.get_share(poll_id, user_id)

    if not share:
        share = api.add_email_share(poll_id=poll_id, user_id=user_id)
        register = True
    else:
        register = False

    token = share.get('token')
    user_id = share.get('userId')

    poll = api.get_poll_by_id(poll_id=poll_id)
    was_expired = poll.get('expire')
    if was_expired:
        api.update_poll_expire(poll_id=poll_id, poll_expire=0)

    login = web.get_login(token=token)
    if register:
        web.add_external_voter(login=login, token=token, user_id=user_id,
                               email_address='')
    web.add_external_vote(login=login, token=token, option_id=option_id, vote_answer='yes')

    if was_expired:
        api.update_poll_expire(poll_id=poll_id, poll_expire=was_expired)

    return redirect(request.referrer)


@app.route("/votes/<int:vote_id>", methods=['POST'])
def delete_votes(vote_id):
    db = PollDB()

    if request.form.get('action') == 'delete':
        db.vote_set_answer(vote_id=vote_id, vote_answer=Answer.NO)
    elif request.form.get('action') == 'recover':
        db.vote_set_answer(vote_id=vote_id, vote_answer=Answer.YES)

    return redirect(request.referrer)


@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response
