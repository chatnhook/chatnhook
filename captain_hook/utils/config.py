import yaml
from os.path import join


def load_config(config_path):
    config_file = open(join(config_path, 'config.yml'), 'rb')
    yaml_config = yaml.load(config_file.read())
    config_file.close()
    return yaml_config
