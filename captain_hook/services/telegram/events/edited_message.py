# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class EditedMessageEvent(BaseEvent):

    def process(self, request, body):
        print('Telegram webhook')

        return {"telegram": str('')}
