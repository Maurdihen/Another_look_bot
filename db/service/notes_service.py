from sqlalchemy.orm import Session
from db.model import Notes
from db.dao.notes_dao import NotesDAO


class NotesService:
    def __init__(self, session: Session):
        self.notes_dao = NotesDAO(session)

    def create_note(self, user_id: int, date: str, time: str, category: str, sub_category: str) -> Notes:
        return self.notes_dao.create_note(user_id, date, time, category, sub_category)
