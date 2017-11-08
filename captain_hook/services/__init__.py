import os
import importlib
from os.path import dirname, abspath, isdir, join

PATH = dirname(abspath(__file__))


def find_and_load_services(config, comms):
    services = get_base_service_list(config)
    services = dict(
        (service, import_service_module(service))
        for service in services
    )
    for name, service in services.items():
        service_config = config["services"].get(name, {})
        service_config['general'] = config['general']
        services[name] = service(service_config, comms)
    return services


def get_base_service_list(config):
    services = os.listdir(PATH)
    services.remove("__init__.py")
    services.remove("__init__.pyc")
    services.remove("base")
    for service in services:
        if not isdir(join(PATH, service)):
            services.remove(service)
    for service in services:
        if not config["services"].get(service, {}).get("enabled"):
            services.remove(service)
    return services


def import_service_module(service):
    package = "services.{}".format(service)
    module = importlib.import_module(package)
    return getattr(module, "{}Service".format(service.title()))
