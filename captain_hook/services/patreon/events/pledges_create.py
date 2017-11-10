# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
from . import PatreonEvent


class PledgesCreateEvent(PatreonEvent):
    def process(self, request, body):
        patron = self.getDataForTypeAndId('user', body['data']['relationships'][
            'patron']['data']['id'], body)
        reward = self.getDataForTypeAndId('reward', body['data']['relationships'][
            'reward']['data']['id'], body)
        creator = self.getDataForTypeAndId('user', body['data']['relationships'][
            'creator']['data']['id'], body)
        campaign = self.getDataForTypeAndId('campaign', reward['relationships'][
            'campaign']['data']['id'], body)

        pledge_amount = '${:,.2f}'.format(
            body['data']['attributes']['amount_cents'] / 100)
        message = '{patron} just pledged *{amount}* / month, gaining the *{reward}* reward. ' \
                  '({creator} at {campaign}) on patreon'
        message = message.format(
            patron=patron['attributes']['full_name'],
            amount=pledge_amount,
            creator=creator['attributes']['full_name'],
            campaign=campaign['attributes']['creation_name'],
            reward=reward['attributes']['title']
        )
        # message = False

        return {"default": message}
