# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import PatreonEvent


class PledgesCreateEvent(PatreonEvent):
    def process(self, request, body):
        reward_id = body.get('data'), {}.get('relationships', {}).get('reward', {})
        patron_id = body.get('data', {}).get('relationships', {}).get('patron', {})
        campaign_id = body.get('data', {}).get('relationships', {}).get('campaign', {})

        reward_id = reward_id[0].get('relationships', {}).get('reward', {})

        patron = self.getDataForTypeAndId('user', patron_id.get('data').get('id'), body)
        reward = self.getDataForTypeAndId('reward', reward_id.get('data').get('id'), body)
        campaign = self.getDataForTypeAndId('campaign', campaign_id.get('data').get('id'), body)
        creator = self.getDataForTypeAndId('user',
                                           campaign.get('relationships', {}).get('creator').get(
                                               'data', {}).get('id'),
                                           body
                                          )
        cents = body.get('data', {}).get('attributes', {}).get('amount_cents', 0)
        pledge_amount = '${:,.2f}'.format(cents / 100)
        message = '{patron} just pledged *{amount}* / month to {campaign} from {creator_name}, ' \
                  'gaining the *{reward}* reward. '
        message = message.format(
            patron=patron.get('attributes', {}).get('full_name'),
            amount=pledge_amount,
            creator_name=creator.get('attributes', {}).get('full_name'),
            campaign=campaign.get('attributes', {}).get('creation_name', ''),
            reward=reward.get('attributes', {}).get('title', '')
        )
        # message = False

        return {"default": message}
