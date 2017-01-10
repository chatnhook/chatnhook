import importlib
import os
from utils import strings

class BaseAdapter:

    def __init__(self, request, body):
        self.request = request
        self.body = body

    def execute(self):
        return self.get_processor_for_event(self.event).process()

    def get_processor_for_event(self, event):
        event_module = self._import_event_module(event)
        event_processor_class_name = "{}{}".format(
            strings.toCamelCase(event),
            "Processor"
        )
        return getattr(event_module, event_processor_class_name)(event)

    def _import_event_module(self, event):
        package = "adapters.{}.processors".format(
            strings.toSnakeCase(
                self.__class__.__name__.split('Adapter')[0]
            )
        )
        importlib.import_module(package)

        return importlib.import_module(
            ".{}".format(event),
            package=package
        )
