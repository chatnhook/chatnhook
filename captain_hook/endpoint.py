from __future__ import absolute_import
from flask import Flask, request
import utils
from services.github import GithubService
from comms.telegram.bot import TelegramComm

SERVICES = {
    "github": GithubService
}

application = Flask(__name__)

@application.route('/<service>', methods=['GET', 'POST'])
def receive_webhook(service):
    return SERVICES[service](request, request.get_json(), setup_comms()).execute()


def setup_comms():
    telegram = TelegramComm()
    telegram.setup()
    return [telegram]


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
