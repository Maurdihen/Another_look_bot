from sqlalchemy.orm import Session
from db_work.dao.models.model import Event


class EventDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_event_by_bid(self, base_id: int) -> Event:
        return self.session.query(Event).filter_by(id=base_id).first()

    def get_events_by_user_id(self, user_id: int) -> list[Event]:
        return self.session.query(Event).filter_by(user_id=user_id).all()

    def create_event(self, data) -> Event:
        new_event = Event(**data)

        self.session.add(new_event)
        self.session.commit()

        return new_event

    def delete_event(self, base_id: int) -> None:
        event = self.get_event_by_bid(base_id)

        self.session.delete(event)
        self.session.commit()
