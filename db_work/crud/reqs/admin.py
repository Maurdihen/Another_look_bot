class AdminRequest:
    def __init__(self, service):
        self._event_service = service

    # def _output(self, events):
    #     out = []
    #     for event in events:
    #         event_data = {
    #             "id": event.id,
    #             "start": event.start,
    #             "end": event.end,
    #             "category": event.category,
    #             "subcategory": event.subcategory,
    #             "users": []
    #         }
    #         out.append(event_data)
    #     return out

    def get_all_events(self):
        events = self._event_service.get_all_events()
        return events

    def get_free_events(self):
        events = self._event_service.get_free_events()
        return events

    def create_event(self, event_data):
        return self._event_service.create_event(event_data)

    # def update_event(self, event_id, update_data):
    #     event = self._event_service.get_event_by_bid(event_id)
    #     if event:
    #         self._event_service.update_event(event, update_data)

    def delete_event(self, event_id):
        event = self._event_service.get_event_by_bid(event_id)
        if event:
            self._event_service.delete_event(event_id)
