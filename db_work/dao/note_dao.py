from sqlalchemy.orm import Session
from db_work.dao.models.model import Note


class NoteDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_note(self, data) -> Note:
        new_note = Note(**data)
        self.session.add(new_note)
        self.session.commit()
        return new_note

    def get_notes_by_user_id(self, user_id: int) -> list[Note]:
        return self.session.query(Note).filter_by(user_id=user_id).all()

    def get_note_by_id(self, note_id: int) -> Note:
        return self.session.query(Note).filter_by(id=note_id).first()

    def update_note(self, data) -> Note:
        note = self.get_note_by_id(data["id"])
        if note:
            note.event_id = data["event_id"]
            note.start = data["start"]
            note.end = data["end"]
            note.category = data["category"]
            note.subcategory = data["subcategory"]

            self.session.commit()
            return note

    def delete_note(self, note_id: int) -> None:
        note = self.get_note_by_id(note_id)
        if note:
            self.session.delete(note)
            self.session.commit()
