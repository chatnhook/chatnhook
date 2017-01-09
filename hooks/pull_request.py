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

pr_link = str(payload['pull_request']['url']).replace('https://api.github.com/', '')
params = {
    'username': payload['pull_request']['user']['login'],
    'user_link': payload['pull_request']['user']['html_url'],
    'pull_request_number': str(payload['pull_request']['number']),
    'pull_request_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + pr_link,
    'pull_request_title': payload['pull_request']['title'],
    'body': str(payload['pull_request']['body']).strip(),
    'repository_name': payload['repository']['full_name'],
    'repository_link': payload['repository']['html_url'],
}
message = False

if payload['action'] == 'opened':
    message = "[⛓]({pull_request_link}) [{username}]({user_link}) opened new pull request [#{pull_request_number} {pull_request_title}]({pull_request_link}) in [{repository_name}]({repository_link})"

if payload['action'] == 'closed' and payload['pull_request']['merged'] == True:
    message = "[⛓]({pull_request_link}) [{username}]({user_link}) merged pull request [#{pull_request_number} {pull_request_title}]({pull_request_link})"

if payload['action'] == 'closed' and payload['pull_request']['merged'] == False:
    message = "[⛓]({pull_request_link}) [{username}]({user_link}) closed pull request [#{pull_request_number} {pull_request_title}]({pull_request_link}) in [{repository_name}](repository_link)"

message = message.format(**params)

if (message):
    bot.send_message(message)
