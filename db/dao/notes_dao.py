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
