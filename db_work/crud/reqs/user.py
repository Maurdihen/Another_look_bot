from db_work.crud.implemented import user_service


class UserRequest:
    def __init__(self, tg_id):
        self._user_service = user_service
        self._tg_id = tg_id
        self._user = self._user_service.get_user_by_tg_id(self._tg_id)

        if self._user is None:
            self._user = self._create_new_user()

    @property
    def tg_id(self):
        return self._tg_id

    def _create_new_user(self):
        user_data = {
            "tg_id": self._tg_id,
            "full_name": None,
            "phone_number": None
        }

        return self._user_service.create_user(user_data)

    def get_user_info(self):
        return {
            "full_name": self._user.full_name,
            "phone_number": self._user.phone_number,
            "events": [x for x in self._user.events]
        }

    def update_user_info(self, update_data):
        user = self._user
        self._user_service.update_user(user, update_data)
