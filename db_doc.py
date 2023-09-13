from db_work.crud.implemented import admin_request
from db_work.crud.reqs.user import UserRequest
from db_work.crud.reqs.event import EventRequest

from db_work.dao.models.model import Event, User

from db_work.service.user_service import UserService
from db_work.service.event_service import EventService

from setup_db.sqlite_db import session


def db_add_all():
    """
    Функция добавления новых пользователей и записей.
    Используется только для тестовых данных единожды.
    """
    session.add_all([user1, user2, user3])

    session.add_all([event1, event2])

    session.commit()


"""
Тестовые данные ниже.
"""

event1 = Event(
    id=1,
    start="2023-09-15T12:00:00+03:00",
    end="2023-09-15T14:00:00+03:00",
    category="Мини-группа",
    subcategory=None,
    is_free=True
)

event2 = Event(
    id=2,
    start="2023-11-12T12:00:00+03:00",
    end="2023-11-12T14:00:00+03:00",
    category="Тематическая группа",
    subcategory="Про отношения",
    is_free=True
)

user1 = User(
    id=1,
    tg_id=777,
    full_name="Владимиров Вадим",
    phone_number="+79111111111"
)
user2 = User(
    id=2,
    tg_id=888,
    full_name="Денис Степанов",
    phone_number="+79555555555"
)
user3 = User(
    id=3,
    tg_id=999,
    full_name="MEGA KRUTOI OMEGA",
    phone_number="+79222222222"
)

"""
Далее идут примеры данных. 
Именно в таком формате сервисы будут ожидать их.
"""

"""
Данные об ивенте, чтобы создать его в базе.
Функция create_event(data). 
Создаёт ивенты админ.
"""

admin_create_data = {
    "start": "2023-10-23T12:00:00+03:00",
    "end": "2023-10-23T14:00:00+03:00",
    "category": "Индивидуальная встреча",
    "subcategory": None  # None или строка
}

"""
Для удаления ивента нужно знать его айди в базе данных. 
Функция delete_event(event_id).
"""

admin_delete_data_id = 2

"""
Методы просмотра ивентов. 
Функции get_all_events() и get_free_events().
"""

"""
Ниже инициализируются user_request'ы с помощью класса UserRequest(tg_id). 
Для инициализации нужен телеграм айди юзера.
"""

"""
Если необходимо посмотреть телеграм айди юзера, просто вызови это поле:
user_request.tg_id.
"""

"""
Ниже идёт пример данных для обновления информации о пользователе.
Функция update_user_info(data).
"""

user_update_data = {
    "full_name": "Вася Пупкин",  # необязательное поле
    "phone_number": "+79123456789",  # необязательное поле
    "event": event1  # Объект класса Event, необязательное поле
}

"""
Достать список со всеми ивентами у юзера можно через метод get_user_info().get("events").
Достать список со всеми юзерами у ивента можно через events.users.
"""


user_request_123 = UserRequest(123)
user_request_999 = UserRequest(999)

event_request_1 = EventRequest(1)

eid = event_request_1.get_event_info().get("id")
user999 = UserService(session).get_user_by_tg_id(user_request_999.tg_id)
new_event = EventService(session).get_event_by_bid(eid)

if __name__ == '__main__':
    # db_add_all()  # вызывается единожды!

    # admin_request.create_event(admin_create_data)
    # admin_request.delete_event(admin_delete_data_id)
    # print(admin_request.get_all_events())

    # print(user_request_123.tg_id)
    # print(user_request_123.get_user_info())
    # print(user_request_999.get_user_info())
    # user_request_123.update_user_info(user_update_data)
    # print(user_request_123.get_user_info())
    # events = user_request_123.get_user_info().get("events")

    # print([x.id for x in events])
    # event = events[0]
    # print(event.users)
    # event_request_1 = EventRequest(event.id)
    # print(event_request_1.get_event_info())
    # event_request_1.book_event({"event": new_event, "user": user999})
    # print(event_request_1.get_event_info())
    # event_request_1.cancel_event({"event": new_event, "user": user999})
    # print(event_request_1.get_event_info())

    print()
    print("Everything is good")
