from __future__ import absolute_import
from os.path import abspath
from os.path import dirname
from flask import Flask, request
import yaml
import utils.config
from services import find_and_load_services
from comms import find_and_load_comms
import json
import pdb

CONFIG_FOLDER = dirname(dirname(abspath(__file__)))

application = Flask(__name__)

config = utils.config.load_config(CONFIG_FOLDER)
comms = find_and_load_comms(config)
services = find_and_load_services(config, comms)


@application.route('/<service>', methods=['GET', 'POST'])
def receive_webhook(service):
    try:
        body = json.loads(request.data)
    except ValueError:
        body = request.form
    return services[service].execute(request, body)


@application.before_first_request
def setup_services():
    for service in services.itervalues():
        service.setup()


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
