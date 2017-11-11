# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
from . import PatreonEvent


class PledgesCreateEvent(PatreonEvent):
    def process(self, request, body):
        reward_id = body.get('data'), {}.get('relationships', {}).get('reward', {})
        patron_id = body.get('data', {}).get('relationships', {}).get('patron', {})
        creator_id = body.get('data', {}).get('relationships', {}).get('creator', {})

        reward_id = reward_id[0].get('relationships', {}).get('reward', {})

        patron = self.getDataForTypeAndId('user', patron_id.get('data').get('id'), body)
        reward = self.getDataForTypeAndId('reward', reward_id.get('data').get('id'), body)
        creator = self.getDataForTypeAndId('user', creator_id.get('data').get('id'), body)

        cents = body.get('data', {}).get('attributes', {}).get('amount_cents', 0)
        pledge_amount = '${:,.2f}'.format(cents / 100)
        message = '{patron} just pledged *{amount}* / month to {creator}, ' \
                  'gaining the *{reward}* reward. '
        message = message.format(
            patron=patron.get('attributes', {}).get('full_name'),
            amount=pledge_amount,
            creator=creator.get('attributes', {}).get('full_name', ''),
            reward=reward.get('attributes', {}).get('title', '')
        )
        # message = False

        return {"default": message}
