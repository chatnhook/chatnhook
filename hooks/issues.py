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

issue_link = str(payload['issue']['url']).replace('https://api.github.com/', '')
params = {
    'username': payload['sender']['login'],
    'user_link': payload['sender']['html_url'],
    'issue_number': str(payload['issue']['number']),
    'issue_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + issue_link,
    'issue_title': payload['issue']['title'],
    'body': payload['issue']['body'],
    'repository_name': payload['repository']['full_name'],
    'repository_link': payload['repository']['html_url'],
}
pprint(params)
message = False
if payload['action'] == 'opened':
    message = "[❓]({issue_link}) [{username}]({user_link}) opened new issue [#{issue_number} {issue_title}]({issue_link}) in [{repository_name}]({repository_link})"

if payload['action'] == 'closed':
    message = "[❓]({issue_link}) [{username}]({user_link}) closed issue [#{issue_number} {issue_title}]({issue_link}) in [{repository_name}]({repository_link})"

message = message.format(**params)

if (message):
    bot.send_message(message)
