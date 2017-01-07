import telegram
from os.path import abspath, normpath, dirname, join
from json import loads
from pprint import pprint
class Bot(object):
    def __init__(self):
        path = dirname(dirname(abspath(__file__)))

        with open(join(path, 'config.json'), 'r') as cfg:
            config = loads(cfg.read())

        self.bot = telegram.Bot(config['telegram_token'])
        self.config = config

    def send_message(self, message, channel=False, parse_mode=telegram.ParseMode.MARKDOWN):
        if not channel:
            channel = self.config['telegram_channel']
        self.bot.sendMessage(chat_id=channel, text=message, parse_mode=parse_mode)
