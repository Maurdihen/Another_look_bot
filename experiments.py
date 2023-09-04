from db_work.crud.implemented import admin_request
from db_work.crud.implemented import user_request

event_data = {
    "tg_user_id": "892189279",
    "start": "2023-08-31T12:00:00+03:00",
    "end": "2023-08-31T13:00:00+03:00",
    "category": "Мини-группа",
    "subcategory": None,
    "is_free": False,
}

user_data = {
    "tg_id": "892189279",
    "full_name": "тест",
    "phone_number": "43231231231",
}

if __name__ == '__main__':
    # admin_request.create_event(event_data)
    print(admin_request.get_free_events())
    # user_request.update_user_info(update_data=user_data)
    # print(user_request.get_user_info())
    print()
    print("Everything is good")