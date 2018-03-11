import sys
from flask_dance.contrib.github import make_github_blueprint, github
from flask import Flask, redirect, url_for

login_services = {
    'github': github
}


def is_authorized(app_config, service):
    if not login_services[service].authorized:
        return False

    if app_config.get('auth', {}).get(service).get('allowed_users'):
        pass

    return getattr(sys.modules[__name__], "check_%s" % service)(app_config)


def check_github(app_config):
    resp = github.get("/user")
    assert resp.ok
    user_array = app_config.get('auth', {}).get('github').get('allowed_users')
    username = resp.json()["login"]

    if username in user_array:
        return username
    else:
        return False
