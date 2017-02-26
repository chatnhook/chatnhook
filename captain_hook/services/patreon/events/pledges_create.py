# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PledgesCreateEvent(BaseEvent):
    def getDataForTypeAndId(self, type, id):
        included_data = self.body['included']
        for data in included_data:
            if data['type'] == type and data['id'] == id:
                return data

    def process(self):

        patron = self.getDataForTypeAndId('user', self.body['data']['relationships']['patron']['data']['id'])
        reward = self.getDataForTypeAndId('reward', self.body['data']['relationships']['reward']['data']['id'])
        creator = self.getDataForTypeAndId('user', self.body['data']['relationships']['creator']['data']['id'])
        campaign = self.getDataForTypeAndId('campaign', reward['relationships']['campaign']['data']['id'])

        pledge_amount = '${:,.2f}'.format(self.body['data']['attributes']['amount_cents'] / 100)
        message = '{patron} just pledged {amount} / month, gaining the {reward} reward. ({creator} at {campaign})'.format(
            patron=patron['attributes']['full_name'],
            amount=pledge_amount,
            creator=creator['attributes']['full_name'],
            campaign=campaign['attributes']['creation_name'],
            reward=reward['attributes']['title']
        )
        # message = False

        return {"telegram": message}
