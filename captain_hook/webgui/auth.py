import json
import sys
from flask_dance.contrib.github import make_github_blueprint, github
from flask import Flask, redirect, url_for
from flask_login import login_user, UserMixin

login_services = {
    'github': github
}


class UserNotFoundError(Exception):
    def __init__(self, user):
        self.user = user

class User(UserMixin):
    def __init__(self, provider, id):
        self.id = id
        self.auth_provider = provider

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

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
        login_user(User('github', username))
        return True
    else:
        raise UserNotFoundError(User('github', username))
