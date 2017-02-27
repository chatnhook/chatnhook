from __future__ import absolute_import
from os.path import abspath
from os.path import dirname
from flask import Flask, request
import yaml
import utils.config
from services import find_services
from comms import find_and_load_comms
import json
import pdb

CONFIG_FOLDER = dirname(dirname(abspath(__file__)))

application = Flask(__name__)

config = utils.config.load_config(CONFIG_FOLDER)
services = find_services(config)
comms = find_and_load_comms(config)

@application.route('/<service>', methods=['GET', 'POST'])
def receive_webhook(service):
    try:
        body = json.loads(request.data)
    except ValueError:
        body = request.form

    return services[service](
        request,
        body,
        comms,
        config["services"][service]
    ).execute()

@application.before_first_request
def init_services():
    for service in services:
        s = services[service](
            False,
            False,
            comms,
            config["services"][service]
        )
        if "init_service" in dir(s):
            services[service](
                False,
                False,
                comms,
                config["services"][service]
            ).init_service()

if __name__ == '__main__':


    application.run(debug=True, host='0.0.0.0')
