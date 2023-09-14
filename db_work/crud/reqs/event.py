from db_work.crud.implemented import event_service


class EventRequest:

    def __init__(self, base_id):
        self._base_id = base_id
        self.event_service = event_service

    def get_event_info(self):
        event = self.event_service.get_event_by_bid(self._base_id)
        info = {
            "id": event.id,
            "start": event.start,
            "end": event.end,
            "category": event.category,
            "subcategory": event.subcategory,
            "is_free": event.is_free,
            "users": [x for x in event.users]
        }
        return info

    def book_event(self, update_data):
        self.event_service.book_event(update_data)

    def cancel_event(self, update_data):
        self.event_service.cancel_event(update_data)
