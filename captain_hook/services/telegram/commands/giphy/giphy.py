# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ..base import BaseCommand
import requests



class GiphyCommand(BaseCommand):
    def get_description(self):
        return "Search for a random giphy gif"

    def run(self, messageObj, config):
        apiKey = config.get('plugins').get('giphy').get('apiKey')
        url = 'https://api.giphy.com/v1/gifs/random?api_key={key}&tag={q}&rating=R&lang=en'.format(
            key=apiKey,
            q=' '.join(messageObj.get('args'))
        )
        r = requests.get(url)
        data = r.json()
        data = data.get('data')
        self.send_document(chat_id=messageObj.get('chat').get('id'),
                          document=data.get('image_original_url'))
