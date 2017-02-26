from __future__ import absolute_import
from os.path import abspath
from os.path import dirname
from flask import Flask, request
import yaml
import utils.config
from services import find_services
from comms import find_and_load_comms


CONFIG_FOLDER = dirname(dirname(abspath(__file__)))

application = Flask(__name__)


@application.route('/<service>', methods=['GET', 'POST'])
def receive_webhook(service):
    config = utils.config.load_config(CONFIG_FOLDER)
    services = find_services(config)
    comms = find_and_load_comms(config)

    print services
    print comms

    return services[service](
        request,
        request.get_json(),
        comms,
        config
    ).execute()


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
