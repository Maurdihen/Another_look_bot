class UserRequest:
    def __init__(self, tg_id, user_service, event_service):
        self.user_service = user_service
        self.event_service = event_service
        self.tg_id = tg_id
        self.events_list = []
        self._events = self.event_service.get_events_by_tg_id(self.tg_id)
        self._user = self.user_service.get_user_by_tg_id(self.tg_id)

        if self._user is None:
            self._user = self._create_new_user()

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

    def _create_new_user(self):
        user_data = {
            "tg_id": self.tg_id,
            "full_name": None,
            "phone_number": None
        }

        return self.user_service.create_user(user_data)

    def get_user_info(self):
        return {
            "full_name": self._user.full_name,
            "phone_number": self._user.phone_number,
            "events": self._output(self._events)
        }

    def update_user_info(self, update_data):
        user = self._user
        self.user_service.update_user(user, update_data)
