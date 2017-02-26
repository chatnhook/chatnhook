from __future__ import absolute_import

import hug
import utils
from services.github import GithubService
from comms.telegram.bot import TelegramComm

SERVICES = {
    "github": GithubService
}

@hug.get('/{service}')
@hug.post('/{service}')
def receive_webhook(request, body, service: hug.types.text):
    return SERVICES[service](request, body, setup_comms()).execute()

def setup_comms():
    telegram = TelegramComm()
    telegram.setup()
    return [telegram]
