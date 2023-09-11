class EventRequest:

    def __init__(self, tg_id, event_service):
        self.event_service = event_service

    def get_events(self):
        return self.user.events

    def book_event(self, data):
        return self.event_service.update_event(data)

    def cancel_event(self, data):
        return self.event_service.update_event(data)
