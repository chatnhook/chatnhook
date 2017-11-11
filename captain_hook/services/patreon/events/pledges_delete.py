# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
from . import PatreonEvent


class PledgesDeleteEvent(PatreonEvent):
    def getDataForTypeAndId(self, type, id, body):
        included_data = body['included']
        for data in included_data:
            if data['type'] == type and data['id'] == id:
                return data

    def process(self, request, body):
        patron_id = body.get('data').get('relationships').get('patron').get('data').get('id')
        reward_id = body.get('data').get('relationships').get('reward').get('data').get('id')
        creator_id = body.get('data').get('relationships').get('creator').get('data').get('id')
        campaign_id = body.get('data').get('relationships').get('campaign').get('data').get('id')

        patron = self.getDataForTypeAndId('user', patron_id, body)
        reward = self.getDataForTypeAndId('reward', reward_id, body)
        creator = self.getDataForTypeAndId('user', creator_id, body)
        campaign = self.getDataForTypeAndId('campaign', campaign_id, body)

        cents = body.get('data', {}).get('attributes', {}).get('amount_cents', 0)
        pledge_amount = '${:,.2f}'.format(cents / 100)
        message = '{patron} removed their patreon pledge of *{amount}* ({creator} at {campaign})'
        message = message.format(
            patron=patron.get('attributes', {}).get('full_name'),
            amount=pledge_amount,
            creator=creator.get('attributes', {}).get('full_name', ''),
            campaign=campaign.get('attributes', {}).get('creation_name', ''),
            reward=reward.get('attributes', {}).get('title', '')
        )
        # message = False

        return {"default": message}
