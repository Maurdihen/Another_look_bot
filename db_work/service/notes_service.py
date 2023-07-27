from sqlalchemy.orm import Session
from db_work.dao.models.model import Notes
from db_work.dao.notes_dao import NotesDAO


class NotesService:
    def __init__(self, session: Session):
        self.notes_dao = NotesDAO(session)

    def create_note(self, user_id: int, date: str, time: str, category: str, sub_category: str) -> Notes:
        return self.notes_dao.create_note(user_id, date, time, category, sub_category)

    def get_notes_by_user_id(self, user_id: int) -> list[Notes]:
        return self.notes_dao.get_notes_by_user_id(user_id)

    def get_note_by_id(self, note_id: int) -> Notes:
        return self.notes_dao.get_note_by_id(note_id)

    def update_note(self, note_id: int, date: str, time: str, category: str, sub_category: str) -> Notes:
        return self.notes_dao.update_note(note_id, date, time, category, sub_category)

    def delete_note(self, note_id: int) -> None:
        return self.notes_dao.delete_note(note_id)
