from __future__ import absolute_import
import importlib
from utils import strings
import logging

log = logging.getLogger('hookbot')


class BaseService:
	def __init__(self, config, comms):
		self.comms = comms
		self.config = config
		self.log = log

	def setup(self):
		pass

	def execute(self, request, body, bot_stats):
		event = self.get_event(request, body)
		if self.config.get('notify_events'):
			if event not in self.config.get('notify_events'):
				return 'Event disabled'
		if self.config.get('disabled_events'):
			if event in self.config.get('disabled_events'):
				return 'Event disabled'
		message_dict = self._get_event_processor(event)
		bot_stats.count_webhook(request.path[1:], event)
		if message_dict:
			message_dict = message_dict.process(request, body)
			for name, comm in self.comms.items():
				default_message = message_dict.get('default', None)
				bot_stats.count_message(name)
				message = message_dict.get(name, default_message)
				if message:
					comm.communicate(message)
			return "ok"
		else:
			return False

	def redirect(self, request, event, params):

		if not self.config.get('redirect', False):
			return False

		redirect_params = self._get_event_processor(
			event=event
		).get_redirect(request, event, params)

		return redirect_params

	def _get_event_processor(self, event):
		event_module = False
		if not event:
			return False
		try:
			event_module = self._import_event_module(event)
		except ImportError:
			self.log.warn('Don\'t know how to handle {}'.format(event))
			print("Doesn't know how to handle {}".format(event))

		event_processor_class_name = "{}Event".format(
			strings.toCamelCase(event),
		)
		if event_module:
			return getattr(event_module, event_processor_class_name)(
				config=self.config,
				event=event
			)
		return False

	def _import_event_module(self, event):
		package = "services.{}.events".format(
			strings.toSnakeCase(
				self.__class__.__name__.split('Service')[0]
			)
		)
		importlib.import_module(package)

		return importlib.import_module(
			".{}".format(event),
			package=package
		)
