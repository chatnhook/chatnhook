![][https://i.imgur.com/UmDqR7T.png]

[![Build Status](https://travis-ci.org/captainhookbot/captain_hook.svg?branch=master)](https://travis-ci.org/captainhookbot/captain_hook)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/captainhookbot/captain_hook/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/captainhookbot/captain_hook/?branch=master)
![Python](https://img.shields.io/badge/python-2.7-brightgreen.svg)
[![Known Vulnerabilities](https://snyk.io/test/github/captainhookbot/captain_hook/badge.svg)](https://snyk.io/test/github/captainhookbot/captain_hook)   

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


## Currently supported comms to publish event information

- Telegram
- Slack
- Discord
- Mattermost


## Adding your own service
See our [wiki](https://github.com/captainhookbot/captain_hook/wiki/Adding-a-service)  

## Adding your own events
See our [wiki](https://github.com/captainhookbot/captain_hook/wiki/Adding-a-event)   

## Adding your comms
See our [wiki](https://github.com/captainhookbot/captain_hook/Adding-a-comm)

## Error logging
We use sentry.io for error logging. This enables us to trackdown issues quickly.
If you don't want this you can turn it off by setting `global.enable_sentry` to false in config.yml
