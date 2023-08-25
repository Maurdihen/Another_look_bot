from db_work.crud.implemented import user_service, event_service


class GetURQ:

    def __init__(self, tg_id):
        self._user = user_service.get_user_by_tg_id(tg_id)
        self._events = event_service.get_events_by_user_id(tg_id)

    def get_user_name(self):
        return self._user.get("full_name")

    def get_user_number(self):
        return self._user.get("phone_number")

    def get_user_events(self):
        return self._events


class PostURQ:

    def __init__(self, event_data):
        self.event_data = event_data

    def __take_data(self):
        # need update method
        user_data = {
            "user_id_tg": self.event_data["user_id"],
            "full_name": self.event_data["name"],
            "phone_number": self.event_data["phone_number"]
        }

        return user_data

    def post_to_db(self):
        user_data, event_data = self.__take_data()
        user_service.create_user(user_data)
        event_service.create_event(event_data)


class PatchRequest:

    def __init__(self, tg_id):
        self._user_data = {"user_id_tg": tg_id}

    def edit_name(self, name):
        self._user_data["full_name"] = name
        user_service.update_user(self._user_data)

    def edit_number(self, number):
        self._user_data["phone_number"] = number
        user_service.update_user(self._user_data)


class DeleteRequest:

    def __init__(self, event_id):
        self.event_id = event_id

    def close_event(self):
        event_service.delete_event(self.event_id)
