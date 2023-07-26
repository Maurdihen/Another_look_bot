from sqlalchemy.orm import Session
from db.model import Notes

class NotesDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_note(self, user_id: int, date: str, time: str, category: str, sub_category: str) -> Notes:
        new_note = Notes(
            user_id=user_id,
            date=date,
            time=time,
            category=category,
            sub_category=sub_category
        )
        self.session.add(new_note)
        self.session.commit()
        return new_note

    def get_notes_by_user_id(self, user_id: int) -> list[Notes]:
        return self.session.query(Notes).filter_by(user_id=user_id).all()

    def get_note_by_id(self, note_id: int) -> Notes:
        return self.session.query(Notes).filter_by(id=note_id).first()

    def update_note(self, note_id: int, date: str, time: str, category: str, sub_category: str) -> Notes:
        note = self.get_note_by_id(note_id)
        if note:
            note.date = date
            note.time = time
            note.category = category
            note.sub_category = sub_category
            self.session.commit()
            return note

    def delete_note(self, note_id: int) -> None:
        note = self.get_note_by_id(note_id)
        if note:
            self.session.delete(note)
            self.session.commit()
