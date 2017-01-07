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
ref = str(payload['ref']).split('/')

if len(payload['commits']) == 0:
    exit()

if ref[2] not in config['notify_branches']:
    exit()

bot = bot.Bot()

push_link = payload['compare'].replace('https://github.com/', '')
user_link = payload['sender']['html_url'].replace('https://github.com/', '')
repo_link = payload['repository']['html_url'].replace('https://github.com/', '')

plural = 'changesets'
if len(payload['commits']) == 1:
    plural = 'changeset'

params = {
    'username': payload['sender']['login'],
    'user_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + user_link,
    'commit_amount': len(payload['commits']),
    'plural': plural,
    'repository_name': payload['repository']['full_name'],
    'repository_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + repo_link,
    'push_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + push_link,
    'ref': ref[2],
}

message = "[🔨]({push_link}) [{username}]({user_link}) pushed {commit_amount} {plural} to {ref} at [{repository_name}]({repository_link}): \n"

# message += '```{body}```'
message = message.format(**params)

for commit in payload['commits']:
    args = {
        'commit_hash': str(commit['id'])[:7],
        'commit_message': commit['message'].replace("\n\n", '\n'),
        'commit_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + commit['url'].replace(
            'https://github.com/', '')
    }
    message += "· [{commit_hash}]({commit_link}): {commit_message} \n".format(**args)

if (message):
    bot.send_message(message)
