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
    'pr_comment_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + comment_api_link,
    'pr_number': str(payload['pull_request']['number']),
    'pr_title': payload['pull_request']['title'],
    'pr_link': payload['pull_request']['html_url'],
}

message = False
if payload['action'] == 'created':
    message = "[🗨]({pr_comment_link}) [{username}]({user_link}) commented on a file in PR [#{pr_number} {pr_title}]({pr_link})"
    # message += '```{body}```'
    message = message.format(**params)

if payload['action'] == 'edited':
    message = "[🗨]({pr_comment_link}) [{username}]({user_link}) edited the comment on a file in PR [#{pr_number} {pr_title}]({pr_link})"
    # message += '```{body}```'
    message = message.format(**params)

if (message):
    bot.send_message(message)
