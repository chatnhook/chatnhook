from __future__ import absolute_import
from os.path import abspath
from os.path import dirname
from flask import Flask, request, g
import yaml
import utils.config
from services import find_and_load_services
from comms import find_and_load_comms
import json
import pdb

CONFIG_FOLDER = dirname(dirname(abspath(__file__)))
config = utils.config.load_config(CONFIG_FOLDER)

application = Flask(__name__)


def get_services():
    services = getattr(g, "_services", None)
    if services is None:
        services = g._services = find_and_load_services(config, get_comms())
    return services


def get_comms():
    comms = getattr(g, "_comms", None)
    if comms is None:
        comms = g._comms = find_and_load_comms(config)
    return comms


@application.route('/<service>', methods=['GET', 'POST'])
def receive_webhook(service):
    try:
        body = json.loads(request.data)
    except ValueError:
        body = request.form
    return get_services()[service].execute(request, body)


@application.before_first_request
def setup_services():
    for service in get_services().itervalues():
        service.setup()


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
