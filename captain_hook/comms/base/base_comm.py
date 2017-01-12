import yaml
from os.path import dirname, abspath, join
from utils import strings


class BaseComm:

    CONFIG_FOLDER = dirname(dirname(dirname(dirname(abspath(__file__)))))

    def __init__(self):
        self.config = self._load_config()

    def setup(self):
        raise NotImplementedError

    def communicate(self):
        raise NotImplementedError

    def _load_config(self):
        config_file = open(join(self.CONFIG_FOLDER, 'comms.yml'), 'rb')
        yaml_config = yaml.load(config_file.read())
        config_file.close()
        return yaml_config
