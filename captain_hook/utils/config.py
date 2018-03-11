import yaml
from os.path import join

def load_config(config_path):
    config_file = open(join(config_path, 'config.yml'), 'rb')
    yaml_config = yaml.load(config_file.read())
    config_file.close()
    test_config(yaml_config)
    return yaml_config


def test_config(config=None):
    if not config:
        config = load_config('.')
    if not config.get('hooks', False):
        raise ValueError('Invalid config detected! Please update your config')
    return True

def save_config(config):
    print yaml.dump(config)