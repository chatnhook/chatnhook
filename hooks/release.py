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

user_link = payload['sender']['html_url'].replace('https://github.com/', '')
tag_link = payload['release']['html_url'].replace('https://github.com/', '')
repo_link = payload['repository']['html_url'].replace('https://github.com/', '')

params = {
    'username': payload['sender']['login'],
    'user_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + user_link,
    'tag': payload['release']['tag_name'],
    'tag_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + tag_link,
    'repository_name': payload['repository']['full_name'],
    'repository_link': config['server_url'] + '/redirect/' + sys.argv[2] + '/' + repo_link,
}
message = False
if payload['action'] == 'published':
    message = "🚀 [{username}]({user_link}) added tag [{tag}]({tag_link}) to [{repository_name}]({repository_link})"
    message = message.format(**params)


if (message):
    bot.send_message(message)
