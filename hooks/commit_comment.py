#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python Example for Python GitHub Webhooks
# File: push-myrepo-master

import sys
import json
import bot

with open(sys.argv[1], 'r') as jsf:
    payload = json.loads(jsf.read())

with open(sys.argv[3], 'r') as jsf:
    config = json.loads(jsf.read())

bot = bot.Bot()

comment_api_link = str(payload['comment']['url']).replace('https://api.github.com/', '')

params = {
    'username': payload['comment']['user']['login'],
    'user_link': payload['comment']['user']['html_url'],
    'commit_hash': str(payload['comment']['commit_id'])[:7],
    'commit_comment_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + comment_api_link,
    'body': str(payload['comment']['body']).split("\n")[0],
}

message = False
if payload['action'] == 'created':
    message = "[🗨]({commit_comment_link}) [{username}]({user_link}) commented on [{commit_hash}]({commit_comment_link})"
    # message += '```{body}```'
    message = message.format(**params)

if payload['action'] == 'edited':
    message = "[🗨]({commit_comment_link}) [{username}]({user_link}) edited the comment on [{commit_hash}]({commit_comment_link})"
    # message += '```{body}```'
    message = message.format(**params)

if (message):
    bot.send_message(message)
