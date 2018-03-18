# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import SocketServer
import json
from os.path import abspath, dirname
from werkzeug.contrib.fixers import ProxyFix
from flask import abort, g, jsonify
from raven.contrib.flask import Sentry

from flask import Flask, render_template, request

import flask_admin as admin
import flask_login as login

from webgui.views import AdminIndexView
from webgui.user import User

from comms import find_and_load_comms
from logger import setup_logger
from services import find_and_load_services
from stats import BotStats
from utils.config import load_config
from utils.forward_request import forward_request
from inspections import WebhookInspector
from hooklog import Hooklog
from webgui.auth import Authorization

CONFIG_FOLDER = dirname(dirname(abspath(__file__)))

config = load_config(CONFIG_FOLDER)
application = Flask(__name__)
application.wsgi_app = ProxyFix(application.wsgi_app)

application.config['SECRET_KEY'] = '123456790'

bot_stats = BotStats()
log = setup_logger()
hook_log = Hooklog()
inspector = WebhookInspector()
application.auth = Authorization()
dsn = 'https://a3aa56ba615c4085ae8855ab78e4c021:a0f50be103034d9eb71331378e8f1da2@sentry.io/245538'
isDev = config.get('global', {}).get('debug', False)
if config.get('global', {}).get('enable_sentry', True) and not isDev:
    log.info('Crash reporting is enabled.')
    log.info('You can disable this by setting global.enable_sentry to false in your config')

    sentry = Sentry(application, dsn=dsn)


def get_services(project_service_config=None):
    services = getattr(g, "_services", None)
    if services is None:
        services = g._services = find_and_load_services(config, project_service_config)
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
                           ), 500


@application.route('/<service>', methods=['GET', 'POST'])
@application.route('/<project>/<service>', methods=['GET', 'POST'])
def receive_webhook(service='', project=''):
    try:
        body = json.loads(request.data)
    except ValueError:
        body = request.form

    project_service_config = config.get('hooks', {}).get(project, {}).get(service, {})
    if service not in get_services(project_service_config):
        log.error('Service {} not found'.format(service))
        return 'Service not found'

    if config.get('inspector', {}).get('inspect_hooks', False):
        path = '/' + project + '/' + service
        inspector.inspect(path, request)

    result = get_services(project_service_config)[service].execute(request,
                                                                   body,
                                                                   bot_stats,
                                                                   hook_log,
                                                                   service,
                                                                   project)
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
        'redirect': result.get('redirect', ''),
        'service': service[0].upper() + service[1:]
    }
    return render_template('redirect.html', **data), result.get('status_code', 200)


@application.route('/inspect', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@application.route('/inspect/<path:path>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def inspect(path=''):
    if not config.get('inspector', {}).get('enabled', True):
        abort(404)

    key = config.get('inspector', {}).get('verification_key', False)
    if key:
        if key != request.args.get('verification_key', False):
            abort(403)
            return ''

    path = '/' + path
    inspector.inspect(path, request)
    forward_url = config.get('inspector', {}).get('forward_url', False)
    if forward_url:
        response = forward_request(forward_url, request)
        return response


@application.route('/favicon.ico', methods=['GET'])
def favIcon():
    return ''


@application.route('/', methods=['GET'])
def index():
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


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(application)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)


def init_services():
    with application.app_context():
        for service in get_services({}).itervalues():
            service.setup()


# Initialize flask-login
init_login()

# Create admin
admin = admin.Admin(application,
                    'Chat \'n\' Hook',
                    index_view=AdminIndexView(config=config,
                                              inspector=inspector,
                                              hook_log=hook_log,
                                              app=application
                                              ))
# admin.add_view(BlankView(name='Blank', url='blank', endpoint='blank'))

if __name__ == '__main__':
    init_services()
    try:
        application.run(debug=False, host='0.0.0.0', threaded=True)
    except SocketServer.socket.error as ex:
        if ex.args[0] != 98:
            raise
        else:
            print('Port already in use')
