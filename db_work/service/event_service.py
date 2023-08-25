from sqlalchemy.orm import Session
from db_work.dao.models.model import Event
from db_work.dao.event_dao import EventDAO


class EventService:
    def __init__(self, session: Session):
        self.event_dao = EventDAO(session)

    def get_event_by_bid(self, base_id: int) -> Event:
        return self.event_dao.get_event_by_bid(base_id)

    def get_events_by_user_id(self, user_id: int) -> list[Event]:
        return self.event_dao.get_events_by_user_id(user_id)

    def create_event(self, data) -> Event:
        return self.event_dao.create_event(data)

    def delete_event(self, base_id: int) -> None:
        return self.event_dao.delete_event(base_id)
