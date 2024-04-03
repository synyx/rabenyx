#!/usr/bin/env python3

import argparse
from argparse import RawTextHelpFormatter
import configparser
from distutils.util import strtobool
import os
import time

from pollapi.pollapi import PollApi
from polldb.polldb import PollDB, Answer
from context_cli import ContextCli


def rabenyx(args):
    try:
        context = ContextCli(args.config)

        api = PollApi(context)

        if args.votes:
            api.get_votes(poll_id=args.votes)
        if args.get_votes_by_user:
            poll_id = int(args.get_votes_by_user[0])
            user_id = args.get_votes_by_user[1]
            api.get_votes_by_userid(poll_id=poll_id, vote_userid=user_id)
        if args.update_vote_answer:
            vote_id = int(args.update_vote_answer[0])
            vote_answer = args.update_vote_answer[1]
            api.update_vote_answer(vote_id=vote_id, vote_answer=vote_answer)
        if args.polls:
            api.get_poll()
        if args.get_poll_by_title:
            api.get_poll_by_title(args.get_poll_by_title)
        if args.new_poll:
            poll_type = args.new_poll[0]
            poll_title = args.new_poll[1]
            api.add_poll(poll_type=poll_type, poll_title=poll_title)
        if args.clone_poll:
            poll_id = int(args.clone_poll[0])
            if len(args.clone_poll) > 1:
                return_id = bool(strtobool(args.clone_poll[1]))
                api.clone_poll(poll_id=poll_id, return_id=return_id)
            else:
                api.clone_poll(poll_id=poll_id)
        if args.add_option:
            poll_id = int(args.add_option[0])
            option = args.add_option[1]
            api.add_option(poll_id=poll_id, option=option)
        if args.get_options:
            poll_id = int(args.get_options[0])
            if len(args.get_options) > 1:
                return_text = bool(strtobool(args.get_options[1]))
                api.get_options(poll_id=poll_id, return_text=return_text)
            else:
                api.get_options(poll_id=poll_id)
        if args.clone_options:
            from_poll_id = args.clone_options[0]
            to_poll_id = args.clone_options[1]
            api.clone_options(from_poll_id=from_poll_id, to_poll_id=to_poll_id)
        if args.update_poll_title:
            poll_id = int(args.update_poll_title[0])
            poll_title = args.update_poll_title[1]
            api.update_poll_title(poll_id=poll_id, poll_title=poll_title)
        if args.update_poll_expire:
            poll_id = int(args.update_poll_expire[0])
            poll_expire = int(args.update_poll_expire[1])
            api.update_poll_expire(poll_id=poll_id, poll_expire=poll_expire)
        if args.update_poll_access:
            poll_id = int(args.update_poll_access[0])
            poll_access = args.update_poll_access[1]
            api.update_poll_access(poll_id=poll_id, poll_access=poll_access)
        if args.update_poll_deleted:
            poll_id = int(args.update_poll_deleted[0])
            poll_deleted = int(args.update_poll_deleted[1])
            api.update_poll_deleted(poll_id=poll_id, poll_deleted=poll_deleted)
        if args.add_email_share:
            poll_id = int(args.add_email_share[0])
            user_id = args.add_email_share[1]
            api.add_email_share(poll_id=poll_id, user_id=user_id)
    except configparser.Error as e:
        print(e.message)
        exit(1)


def rabenyx_votes(args):
    db = PollDB()
    poll_id = args.poll[0]

    if args.delete:
        for vote_id in args.delete:
            db.vote_set_answer(vote_id=vote_id, vote_answer=Answer.NO)


def rabenyx_polls(args):
    api = PollApi(ContextCli(args.config))
    poll_id = args.poll[0]

    if args.delete:
        poll_deleted = time.time()
        api.update_poll_deleted(poll_id=poll_id, poll_deleted=poll_deleted)
    elif args.recover:
        api.update_poll_deleted(poll_id=poll_id, poll_deleted=0)
    elif args.votes:
        for x in api.get_votes(poll_id=poll_id):
            print(format(x.get('id')) + ": " + x.get('userId') + " | " + x.get('optionText'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='An ally for the fight against the chaos of Corona organisation.',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-p', '--polls', help='Get all polls.', action="store_true")
    parser.add_argument('--get-poll-by-title', help='Get a poll from a given poll title.', type=str)
    parser.add_argument('-v', '--votes', help='Get votes for a given poll id.', type=int)
    parser.add_argument('--get-votes-by-user',
                        help='Get votes of a user for a given poll id.',
                        nargs=2,
                        metavar=('POLL_ID', 'USER_ID'))
    parser.add_argument('--update-vote-answer',
                        help='Changes the answer for a vote.',
                        nargs=2,
                        metavar=('VOTE_ID', 'VOTE_ANSWER'))
    parser.add_argument('-c', '--config', help='Specify configuration file. (Default: ' +
                                               os.path.expanduser('~/') + '.config/rabenyx.ini)', type=str,
                                               default=(os.path.expanduser('~/') + '.config/rabenyx.ini'))
    parser.add_argument('--new-poll',
                        help='Add new poll. You need to provide a poll type (either "textPoll" or "datePoll") and the '
                             'title of the poll.',
                        nargs=2,
                        metavar=('POLL_TYPE', 'POLL_TITLE'))
    parser.add_argument('--clone-poll',
                        help='Clones a poll. If RETURN_ID is \"True\" the command returns the new poll id instead of '
                             'the poll data.',
                        nargs='+',
                        metavar=('POLL_ID', 'RETURN_ID'))
    parser.add_argument('--add-option',
                        help='Adds an option to an existing poll. You need to provide a poll id and the option text.',
                        nargs=2,
                        metavar=('POLL_ID', 'OPTION'))
    parser.add_argument('--get-options',
                        help='Get options from a given poll. If RETURN_TEXT is \"True\" the command returns the text '
                             'of the options instead of their whole data.',
                        nargs=2,
                        metavar=('POLL_ID', 'RETURN_TEXT'))
    parser.add_argument('--clone-options',
                        help='Clones the options of a given poll to another.',
                        nargs=2,
                        metavar=('FROM_POLL_ID', 'TO_POLL_ID'))
    parser.add_argument('--update-poll-title',
                        help='Updates the title of a given poll.',
                        nargs=2,
                        metavar=('POLL_ID', 'POLL_TITLE'))
    parser.add_argument('--update-poll-expire',
                        help='Updates the expire date of a given poll. Use a Unix timestamp for POLL_EXPIRE.',
                        nargs=2,
                        metavar=('POLL_ID', 'POLL_EXPIRE'))
    parser.add_argument('--update-poll-access',
                        help='Updates the access of a given poll. POLL_ACCESS can either be "public" or "hidden".',
                        nargs=2,
                        metavar=('POLL_ID', 'POLL_ACCESS'))
    parser.add_argument('--update-poll-deleted',
                        help='Archives the poll. Use a Unix timestamp for POLL_DELETED to archive it. Use 0 for '
                             'POLL_DELETED to unarchive it.',
                        nargs=2,
                        metavar=('POLL_ID', 'POLL_DELETED'))
    parser.add_argument('--add-email-share',
                        help='Adds an email share to a given poll.',
                        nargs=2,
                        metavar=('POLL_ID', 'USER_NAME'))
    parser.set_defaults(func=rabenyx)

    subparsers = parser.add_subparsers(dest='subparser', help='sub-command help')

    parser_poll = subparsers.add_parser('poll', help="poll help")
    parser_poll.add_argument('poll', type=int, nargs=1, help='The poll id')
    parser_poll.add_argument('--delete', '-d', action='store_true', help="Delete poll")
    parser_poll.add_argument('--recover', '-r', action='store_true', help="Recover deleted poll")
    parser_poll.add_argument('--votes', '-v', action='store_true', help="List votes from poll")
    parser_poll.set_defaults(func=rabenyx_polls)

    parser_votes = subparsers.add_parser('votes', help="votes help")
    parser_votes.add_argument('poll', type=int, nargs=1, help='The poll id')
    parser_votes.add_argument('--delete', '-d', type=int, help="Delete votes from vote_id", action='append')
    parser_votes.set_defaults(func=rabenyx_votes)

    args = parser.parse_args()
    try:
        args.func(args)
    except configparser.Error as e:
        print(e.message)
        exit(1)
