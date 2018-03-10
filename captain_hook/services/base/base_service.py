from __future__ import absolute_import

import importlib
import json
import logging
import subprocess

import utils.config
from comms import load_comm
from utils import strings

log = logging.getLogger('hookbot')


class BaseService:
    def __init__(self, config, project_service_config):
        self.config = config
        self.project_service_config = project_service_config
        self.global_config = utils.config.load_config('.')
        self.log = log

    def setup(self):
        pass

    def execute(self, request, body, bot_stats, hook_log, service, project):
        event = self.get_event(request, body)
        if not event:
            return "Unable to detect event"

        if self.project_service_config.get('settings', {}).get('notify_events'):
            if event not in self.config.get('notify_events'):
                return 'Event disabled'

        if self.project_service_config.get('settings', {}).get('disabled_events'):
            if event in self.project_service_config.get('settings', {}).get('disabled_events'):
                return 'Event disabled'

        if self.project_service_config.get('settings', {}).get('scripts', {}).get(event, False):
            for script in self.project_service_config.get('settings', {})\
                    .get('scripts', {}).get(event, False):
                command = script.split(' ')
                command.append(event)
                command.append(json.dumps(body))
                subprocess.Popen(command)

        message_dict = self._get_event_processor(event)
        bot_stats.count_webhook(request.path[1:], event)

        to_comms = self.project_service_config.get('send_to', {})

        comm_result = {
            'services': {},
            'total': len(to_comms),
            'success': 0
        }

        if message_dict:
            message_dict = message_dict.process(request, body)

            for name, comm in to_comms.items():
                comm_result['services'][name] = {
                    'result': False,
                    'error': ''
                }
                if self.project_service_config\
                        .get('send_to', {}).get(name, {}).get('enabled', True):
                    comm = load_comm(name,
                                     self.global_config.get('comms', {}).get(name, {}),
                                     self.project_service_config.get('send_to', {}).get(name))
                    default_message = message_dict.get('default', None)
                    message = message_dict.get(name, default_message)
                    if message:
                        bot_stats.count_message(name)
                        try:
                            comm.communicate(message)
                            comm_result['services'][name]['result'] = True
                            comm_result['success'] += 1
                        except Exception as ex:
                            template = "An exception of type {0} occurred."
                            message = template.format(type(ex).__name__)
                            print message
                            comm_result['services'][name]['error'] = message
                else:
                    message = "Service is disabled"
                    comm_result['services'][name]['error'] = message
            hook_log.log_hook(project, service, event, comm_result)
            return "ok"
        else:
            hook_log.log_hook(project, service, event, comm_result)
            return False

    def redirect(self, request, event, params):

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

        event_processor_class_name = "{}Event".format(
            strings.toCamelCase(event),
        )
        if event_module:
            return getattr(event_module, event_processor_class_name)(
                config=self.config,
                project_service_config=self.project_service_config,
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
