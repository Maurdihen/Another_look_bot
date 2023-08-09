from db_work.crud.implemented import user_service, note_service


class GetRequest:

    def __init__(self, tg_id):
        self.user = user_service.get_user_by_tg_id(tg_id)

    def get_name(self):
        return self.user["full_name"]

    def get_number(self):
        return self.user["phone_number"]

    def get_notes(self):
        ...


class PostRequest:

    def __init__(self, event_data):
        self.event_data = event_data

    def __feel_dicts(self):
        user_data, note_data = {}, {}

        user_data["user_id_tg"] = self.event_data["user_id"]
        user_data["full_name"] = self.event_data["name"]
        user_data["phone_number"] = self.event_data["phone_number"]

        note_data["user_id"] = self.event_data["user_id"]
        note_data["event_id"] = self.event_data["event_id"]
        note_data["start"] = self.event_data["start"]
        note_data["end"] = self.event_data["end"]
        note_data["category"] = self.event_data["summary"]
        note_data["subcategory"] = self.event_data["subgroup"]

        return user_data, note_data

    def post_to_db(self):
        user_data, note_data = self.__feel_dicts()
        user_service.create_user(user_data)
        note_service.create_note(note_data)


class PatchRequest:

    def __init__(self, tg_id):
        self.data = {"user_id_tg": tg_id}

    def edit_name(self, name):
        self.data["full_name"] = name
        user_service.update_user(self.data)

    def edit_number(self, number):
        self.data["phone_number"] = number
        user_service.update_user(self.data)


class DeleteRequest:

    def __init__(self, event_id):
        self.event_id = event_id
