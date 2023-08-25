from db_work.crud.implemented import user_service, event_service


class UserRequest:
    def __init__(self, tg_id):
        try:
            self._user = user_service.get_user_by_tg_id(tg_id)
        except:
            self._user = self._create_new_user(tg_id)
        self._events = event_service.get_events_by_user_id(tg_id)

    @staticmethod
    def _create_new_user(tg_id):
        user_data = {
            "tg_id": tg_id,
            "full_name": None,
            "phone_number": None
        }

        return user_service.create_user(user_data)

    def get_user_info(self):
        return {
            "full_name": self._user.get("full_name"),
            "phone_number": self._user.get("phone_number"),
            "events": self._events
        }

    def update_user_info(self, update_data):
        user = self._user
        user_service.update_user(user, update_data)
