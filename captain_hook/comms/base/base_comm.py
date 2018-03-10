from __future__ import absolute_import


class BaseComm:
    def __init__(self, config, project_service_config):
        self.config = config
        self.project_service_config = project_service_config

    def setup(self):
        raise NotImplementedError

    def communicate(self, message):
        raise NotImplementedError

    def get_config_template(self):
        return 'No config options!'
