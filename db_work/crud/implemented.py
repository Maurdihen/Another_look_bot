from db_work.service.user_service import UserService
from db_work.service.note_service import NoteService

from setup_db.sqlite_db import session


user_service = UserService(session)
note_service = NoteService(session)
