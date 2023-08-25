from db_work.service.user_service import UserService
from db_work.service.event_service import EventService

from setup_db.sqlite_db import session


user_service = UserService(session)
event_service = EventService(session)
