![](https://demo.identihub.co/assets/Chat'n'Hook_ICONS_5.png)

[![Build Status](https://travis-ci.org/chatnhook/chatnhook.svg?branch=master)](https://travis-ci.org/chatnhook/chatnhook)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/chatnhook/chatnhook/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/chatnhook/chatnhook/?branch=master)
![Python](https://img.shields.io/badge/python-2.7-brightgreen.svg)
[![Documentation Status](https://readthedocs.org/projects/chatnhook/badge/?version=latest)](http://chatnhook.readthedocs.io/en/latest/?badge=latest)   

A web server to receive webhooks from many online services and forward the information
to many different messaging platforms, like Telegram or Slack, using a different
template for each.

A **service** represents any web service that sends a webhook.

An **event** is identified from the given webhook (like a push on Github, for example)

A **comm** is then used to publish information from this hook in messaging services.

## Dependencies

- Python 2.7

`sudo pip install -r requirements.txt`


## Running
Run without deamon:   
`python captain_hook/endpoint.py`

Run with deamon (required for the `/update` telegram command):    
```
./daemon.sh install
/etc/init.d/hook-bot start
```
Acces the WebGui with the following url: https://YOURWEBSERVERADRES:5000/admin/

## Currently supported services and events

- Github
- Bitbucket
- Docker
- Pagerduty
- Patreon
- Scrutinizer
- Codacy
- Slack
- Travis
- CircleCI
- Telegram (can be used as telegram bot)
- Zabbix (In combination with this [script](https://github.com/chatnhook/zabbix-alertscript))

## Currently supported comms to publish event information

- Telegram
- Slack
- Discord
- Mattermost

## Documentation
See our documentation on [Readthedocs](https://chatnhook.readthedocs.io/en/latest/)  

## Contributors
- Brantje
- Maestroi

## Error logging
We use sentry.io for error logging. This enables us to trackdown issues quickly.
If you don't want this you can turn it off by setting `global.enable_sentry` to false in config.yml
