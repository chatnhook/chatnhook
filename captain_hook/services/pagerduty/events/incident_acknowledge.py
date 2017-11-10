# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IncidentAcknowledgeEvent(BaseEvent):
    def process(self, request, body):
        payload = body['messages'][0]
        acknowledger = payload['data']['incident'][
            'acknowledgers'][0]['object']
        incident = payload['data']['incident']
        message = '[{name}]({user_link}) has acknowledged incident' \
                  ' [#{incident_number} {incident_title}]({incident_link})'\
            .format(
                name=acknowledger['name'],
                user_link=acknowledger['html_url'],
                incident_number=str(incident['incident_number']),
                incident_title=incident[
                    'trigger_summary_data']['subject'],
                incident_link=incident['html_url'])

        return {'default': message}
