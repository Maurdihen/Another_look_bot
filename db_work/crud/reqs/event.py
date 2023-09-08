from db_work.crud.implemented import event_service
from db_work.crud.implemented import user_service


class EventRequest:

    def __init__(self, tg_id):
        self.user = user_service.get_user_by_tg_id(tg_id)

    def get_events(self):
        return self.user.events

    def book_event(self, data):
        return event_service.update_event(data)
    def cancel_event(self, data):
        return event_service.update_event(data)
