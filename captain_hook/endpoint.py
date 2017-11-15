# -*- coding: utf-8 -*-
from __future__ import absolute_import
from os.path import abspath
from os.path import dirname
from flask import Flask, request, g, render_template, jsonify, abort
import utils.config
from services import find_and_load_services
from comms import find_and_load_comms
from stats.stats import BotStats
import logging
import json
from raven.contrib.flask import Sentry

CONFIG_FOLDER = dirname(dirname(abspath(__file__)))
config = utils.config.load_config(CONFIG_FOLDER)

application = Flask(__name__)

bot_stats = BotStats()

formatter = logging.Formatter('%(created)s - %(name)s - %(levelname)s - %(message)s')
dsn = 'https://a3aa56ba615c4085ae8855ab78e4c021:a0f50be103034d9eb71331378e8f1da2@sentry.io/245538'

if config.get('enable_sentry', True):
    sentry = Sentry(application, dsn=dsn)

wz = logging.getLogger('werkzeug')
wz.setLevel(logging.INFO)

wd = logging.getLogger('watchdog')
wd.setLevel(logging.INFO)

log = logging.getLogger('hookbot')
logging.getLogger().setLevel(logging.DEBUG)

fh = logging.FileHandler('hookbot.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

wz.addHandler(fh)
wz.addHandler(ch)

ch.setFormatter(formatter)
fh.setFormatter(formatter)
log.addHandler(ch)
log.addHandler(fh)


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


@application.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html',
                           event_id=g.sentry_event_id,
                           public_dsn=sentry.client.get_public_dsn('https')
                           )


@application.route('/<service>', methods=['GET', 'POST'])
def receive_webhook(service):
    try:
        body = json.loads(request.data)
    except ValueError:
        body = request.form

    if service not in get_services():
        log.error('Service {} not found'.format(service))
        return 'Service not found'
    result = get_services()[service].execute(request, body, bot_stats)
    if result:
        return result
    else:
        return 'Error during processing. See log for more info'


@application.route('/redirect/<service>/<event>', methods=['GET'], defaults={'params': None})
@application.route('/redirect/<service>/<event>/<path:path>', methods=['GET'])
def redirect(service, event, path):
    if service not in get_services():
        log.error('Service {} not found'.format(service))
        return 'Service not found'
    result = get_services()[service].redirect(request, event, path)
    if not result:
        return ""
    bot_stats.count_redirect(service)
    data = {
        'meta_title': result.get('meta_title', '').decode("utf8"),
        'meta_summary': result.get('meta_summary', '').decode("utf8"),
        'meta_link': config['global']['bot_url'] + '/' + request.path,
        'poster_image': result.get('poster_image', '').decode("utf8"),
        'redirect': result.get('redirect', '')
    }

    return render_template('redirect.html', **data), result.get('status_code', 200)


@application.route('/favicon.ico', methods=['GET'])
def favIcon():
    return ''


@application.route('/stats', methods=['GET'])
def getstats():
    enabled = False
    if config.get('stats', {}).get('enabled') is True:
        if config.get('stats').get('api_key'):
            key = config.get('stats').get('api_key')
            submitted_key = request.args.get('api_key')
            if key == submitted_key:
                enabled = True
        else:
            enabled = True

        if enabled:
            return jsonify(bot_stats.get_stats())
        else:
            abort(404)
    else:
        abort(404)


def init_serviceses():
    with application.app_context():
        for service in get_services().itervalues():
            service.setup()


if __name__ == '__main__':
    init_serviceses()
    application.run(debug=False, host='0.0.0.0')
