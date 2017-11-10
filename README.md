# Captain Hook

[![Build Status](https://travis-ci.org/brantje/captain_hook.svg?branch=master)](https://travis-ci.org/brantje/captain_hook)
![Python](https://img.shields.io/badge/python-2.7-brightgreen.svg)

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

`python captain_hook/endpoint.py`

## Currently supported services and events

- Github
- Docker
- Pagerduty
- Patreon
- Scrutinizer
- Slack
- Travis
- Telegram (can be used as telegram bot)


## Currently supported comms to publish event information

- Telegram
- Slack
- Discord
- Mattermost


## Adding your own service
See our [wiki](https://github.com/brantje/captain_hook/wiki/Adding-a-service)  

## Adding your own events
See our [wiki](https://github.com/brantje/captain_hook/wiki/Adding-a-event)   

## Adding your comms
See our [wiki](https://github.com/brantje/captain_hook/wiki/Adding-a-comm)