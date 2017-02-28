from __future__ import absolute_import
import importlib
from utils import strings


class BaseService:
    def __init__(self, config, comms):
        self.comms = comms
        self.config = config

    def setup(self):
        pass

    def execute(self, request, body):
        message_dict = self._get_event_processor(
            self.get_event(request, body)
        ).process(request, body)
        for name, comm in self.comms.items():
            default_message = message_dict.get('default', None)
            comm.communicate(message_dict.get(name, default_message))
        return "ok"

    def redirect(self, request, event, params):

        redirect_params = self._get_event_processor(
            event=event
        ).get_redirect(request, event, params)

        return redirect_params

    def _get_event_processor(self, event):
        try:
            event_module = self._import_event_module(event)
        except ImportError:
            print("Doesn't know how to handle {}".format(event))

        event_processor_class_name = "{}Event".format(
            strings.toCamelCase(event),
        )
        return getattr(event_module, event_processor_class_name)(
            config=self.config,
            event=event
        )

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
