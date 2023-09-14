from db_work.service.user_service import UserService
from db_work.service.event_service import EventService
from db_work.crud.reqs.admin import AdminRequest

from setup_db.sqlite_db import session

event_service = EventService(session)
user_service = UserService(session)

admin_request = AdminRequest(event_service)
