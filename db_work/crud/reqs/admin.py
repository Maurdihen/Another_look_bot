class AdminRequest:
    def __init__(self, service):
        self._event_service = service
        self._events_list = []

    def _output(self, events):
        for event in events:
            event_data = {
                "id": event.id,
                "start": event.start,
                "end": event.end,
                "category": event.category,
                "subcategory": event.subcategory,
                "users": []
            }
            self._events_list.append(event_data)

    def get_all_events(self):
        events = self._event_service.get_all_events()
        self._output(events)
        return self._events_list

    # def get_free_events(self):
    #     events = self._event_service.get_free_events()
    #     self._output(events)
    #     return self.events_list

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
