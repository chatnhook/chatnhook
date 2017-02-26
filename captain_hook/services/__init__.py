import os
import importlib
from os.path import dirname, abspath, isdir, join


PATH = dirname(abspath(__file__))


def find_services(config):
    services = os.listdir(PATH)
    services.remove("__init__.py")
    services.remove("__init__.pyc")
    services.remove("base")
    for service in services:
        if not isdir(join(PATH, service)):
            services.remove(service)
    for service in services:
        if not config["services"][service].get("enabled"):
            services.remove(service)
    services = [import_service_module(service) for service in services]
    return dict(
        (service.__name__.split("Service")[0].lower(), service)
        for service in services
    )


def import_service_module(service):
    package = "services.{}".format(service)
    module = importlib.import_module(package)
    return getattr(module, "{}Service".format(service.title()))
