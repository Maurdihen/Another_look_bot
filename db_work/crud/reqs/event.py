class EventRequest:

    def __init__(self, tg_id, event_service, user_service):
        self.event_service = event_service
        self._user = user_service.get_user_by_tg_id(tg_id)

    def get_events(self):
        return self._user.events

    def book_event(self, data):
        return self.event_service.update_event(data)

    def cancel_event(self, data):
        return self.event_service.update_event(data)
