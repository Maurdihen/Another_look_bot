from db_work.service.user_service import UserService
from db_work.service.event_service import EventService
from db_work.crud.reqs.admin import AdminRequest
from db_work.crud.reqs.user import UserRequest

from setup_db.sqlite_db import session

user_service = UserService(session)
event_service = EventService(session)

admin_request = AdminRequest(event_service)
user_request = UserRequest(user_service=user_service, event_service=event_service, tg_id=32423423)
