from sqlalchemy.orm import Session
from db_work.dao.models.model import Note
from db_work.dao.note_dao import NoteDAO


class NoteService:
    def __init__(self, session: Session):
        self.note_dao = NoteDAO(session)

    def get_note_by_id(self, note_id: int) -> Note:
        return self.note_dao.get_note_by_id(note_id)

    def get_notes_by_user_id(self, user_id: int) -> list[Note]:
        return self.note_dao.get_notes_by_user_id(user_id)

    def create_note(self, data) -> Note:
        return self.note_dao.create_note(data)

    def delete_note(self, note_id: int) -> None:
        return self.note_dao.delete_note(note_id)
