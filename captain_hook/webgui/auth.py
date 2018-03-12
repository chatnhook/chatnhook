import json
import sys
from flask_dance.contrib.github import github
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


class Authorization:
    def __init__(self):
        self.pending_authorizations = []
        pass

    @staticmethod
    def is_authorized(app_config, service):
        if not login_services[service].authorized:
            return False

        if app_config.get('auth', {}).get(service).get('allowed_users'):
            pass

        return getattr(Authorization, "check_%s" % service)(app_config)

    @staticmethod
    def check_github(app_config):
        resp = github.get("/user")
        if not resp.ok:
            return False
        user_array = app_config.get('auth', {}).get('github').get('allowed_users')
        username = resp.json()["login"]

        if username in user_array:
            login_user(User('github', username))
            return True
        else:
            raise UserNotFoundError(User('github', username))

    def add_user_to_pending_authorization(self, user):
        self.pending_authorizations.append(user)

    def get_pending_list(self):
        return self.pending_authorizations

    def has_pending_request(self, user):
        return user in self.pending_authorizations

    def remove_user_from_pending_list(self, service, user_id):
        try:
            self.pending_authorizations.remove(User(service, user_id))
        except ValueError:
            pass
