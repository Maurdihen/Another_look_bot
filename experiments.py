from db_work.crud.implemented import admin_request
from db_work.crud.implemented import user_request

event_data = {
    "tg_user_id": "892189279",
    "start": "2023-09-03T17:00:00+03:00",
    "end": "2023-09-03T18:00:00+03:00",
    "category": "Мини группа",
    "subcategory": None,
    "is_free": True,
}

user_data = {
    "tg_id": "892189279",
    "full_name": "Denis",
    "phone_number": "89278685655",
}

if __name__ == '__main__':
    print(admin_request.get_free_events())
    # admin_request.create_event(event_data)
    # print(user_request.get_user_info())
    print()
    print("Everything is good")
