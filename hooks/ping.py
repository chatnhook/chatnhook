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
repo_link = payload['repository']['html_url'].replace('https://github.com/', '')

params = {
    'repo': payload['repository']['full_name']
}

message = "Webhook works for: {repo}".format(**params)

if (message):
    bot.send_message(message)