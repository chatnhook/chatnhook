from __future__ import absolute_import
import yaml
from os.path import join


class BaseComm:
    def __init__(self, config, project_service_config):
        self.config = config
        self.project_service_config = project_service_config

    def setup(self):
        raise NotImplementedError

    def communicate(self):
        raise NotImplementedError

    def _load_config(self):
        config_file = open(join(self.CONFIG_FOLDER, 'comms.yml'), 'rb')
        yaml_config = yaml.load(config_file.read())
        config_file.close()
        return yaml_config
