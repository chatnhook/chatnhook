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
issue_type = 'issue'

if 'pull_request' in payload['issue']:
    issue_type = 'pull request'

params = {
    'username': payload['comment']['user']['login'],
    'user_link': payload['comment']['user']['html_url'],
    'issue_number': str(payload['issue']['number']),
    'comment_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + comment_api_link,
    'issue_title': payload['issue']['title'],
    'issue_type': issue_type,
    'body': str(payload['comment']['body']).split("\n")[0] + '...',
}

message = False
if payload['action'] == 'created':
    message = "[🗨]({comment_link}) [{username}]({user_link}) commented on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
    # message += '```{body}```'
    message = message.format(**params)

if payload['action'] == 'edited':
    message = "[🗨]({comment_link}) [{username}]({user_link}) edited the comment on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
    # message += '```{body}```'
    message = message.format(**params)

if (message):
    bot.send_message(message)
