from ...base.events import BaseEvent


class PatreonEvent(BaseEvent):
    def getDataForTypeAndId(self, type, id, body):
        included_data = body['included']
        for data in included_data:
            if data['type'] == type and data['id'] == id:
                return data
