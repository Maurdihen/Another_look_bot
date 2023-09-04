class AdminRequest:
    def __init__(self, service):
        self.event_service = service
        self.events_list = []

    def _output(self, events):
        for event in events:
            event_data = {
                "id": event.id,
                "tg_user_id": event.tg_user_id,
                "start": event.start,
                "end": event.end,
                "category": event.category,
                "subcategory": event.subcategory,
                "is_free": event.is_free
            }
            self.events_list.append(event_data)
        return self.events_list

    def get_all_events(self):
        events = self.event_service.get_all_events()
        return self._output(events)

    def get_free_events(self):
        events = self.event_service.get_free_events()
        return self._output(events)

    def create_event(self, event_data):
        return self.event_service.create_event(event_data)

    def update_event(self, event_id, update_data):
        event = self.event_service.get_event_by_bid(event_id)
        if event:
            self.event_service.update_event(event, update_data)

    def delete_event(self, event_id):
        event = self.event_service.get_event_by_bid(event_id)
        if event:
            self.event_service.delete_event(event_id)
