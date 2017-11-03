# -*- coding: utf-8 -*-
from __future__ import absolute_import
from os.path import abspath
from os.path import dirname
from flask import Flask, request, g, render_template, jsonify, abort
import utils.config
from services import find_and_load_services
from comms import find_and_load_comms
from stats.stats import BotStats
import json

CONFIG_FOLDER = dirname(dirname(abspath(__file__)))
config = utils.config.load_config(CONFIG_FOLDER)

application = Flask(__name__)

bot_stats = BotStats()


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

	if service not in get_services():
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
		return 'Service not found'
	result = get_services()[service].redirect(request, event, path)
	if not result:
		return ""
	bot_stats.count_redirect(service)
	data = {
		'meta_title': result.get('meta_title', '').decode("utf8"),
		'meta_summary': result.get('meta_summary', '').decode("utf8"),
		'meta_link': config['general']['bot_url'] + '/' + request.path,
		'poster_image': result.get('poster_image', '').decode("utf8"),
		'redirect': result.get('redirect', '')
	}

	return render_template('redirect.html', **data), result.get('status_code', 200)


@application.route('/stats', methods=['GET'])
def getstats():
	enabled = False
	if config.get('stats') and config.get('stats').get('enabled') is True:
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
			abort(403)
	else:
		abort(404)


def init_serviceses():
	with application.app_context():
		for service in get_services().itervalues():
			service.setup()


if __name__ == '__main__':
	init_serviceses()
	application.run(debug=True, host='0.0.0.0')
