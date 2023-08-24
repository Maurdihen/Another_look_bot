from sqlalchemy.orm import Session
from db_work.dao.models.model import Note


class NoteDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_note_by_id(self, note_id: int) -> Note:
        return self.session.query(Note).filter_by(id=note_id).first()

    def get_notes_by_user_id(self, user_id: int) -> list[Note]:
        return self.session.query(Note).filter_by(user_id=user_id).all()

    def create_note(self, data) -> Note:
        new_note = Note(**data)

        self.session.add(new_note)
        self.session.commit()

        return new_note

    def delete_note(self, note_id: int) -> None:
        note = self.get_note_by_id(note_id)
        if note:
            self.session.delete(note)
            self.session.commit()
