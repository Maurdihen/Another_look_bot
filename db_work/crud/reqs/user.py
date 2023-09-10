class UserRequest:
    def __init__(self, tg_id, user_service, event_service):
        self.user_service = user_service
        self.event_service = event_service
        self.tg_id = tg_id
        self._user = self.user_service.get_user_by_tg_id(self.tg_id)

        if self._user is None:
            self._user = self._create_new_user()

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
            "events": [x for x in self._user.events]
        }

    def update_user_info(self, update_data):
        user = self._user
        self.user_service.update_user(user, update_data)
