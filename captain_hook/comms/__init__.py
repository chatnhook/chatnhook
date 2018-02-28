import os
import importlib
from os.path import dirname, abspath, isdir, join

PATH = dirname(abspath(__file__))


def find_and_load_comms(config):
    comms = get_base_comm_list()
    comms = load_comms(comms, config)
    return dict(
        (service.__class__.__name__.split("Comm")[0].lower(), service)
        for service in comms
    )


def get_base_comm_list():
    comms = os.listdir(PATH)
    comms.remove("__init__.py")
    comms.remove("__init__.pyc")
    comms.remove("base")
    for comm in comms:
        if not isdir(join(PATH, comm)):
            comms.remove(comm)
    return comms


def load_comms(comms, config):
    loaded_comms = []
    for comm in comms:
        if comm not in config['comms']:
            continue

        comm_config = config["comms"][comm]
        comm = import_service_module(comm)(comm_config)
        comm.setup()
        loaded_comms.append(comm)
    return loaded_comms


def load_comm(comm, config, project_service_config={}):
    comm = import_service_module(comm)(config, project_service_config)
    comm.setup()
    return comm


def import_service_module(comm):
    package = "comms.{}".format(comm)
    module = importlib.import_module(package)
    return getattr(module, "{}Comm".format(comm.title()))
