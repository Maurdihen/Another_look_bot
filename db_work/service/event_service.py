from typing import Type

from sqlalchemy.orm import Session
from db_work.dao.models.model import Event
from db_work.dao.event_dao import EventDAO


class EventService:
    def __init__(self, session: Session):
        self.event_dao = EventDAO(session)

    def get_event_by_bid(self, base_id: int) -> Type[Event] | None:
        return self.event_dao.get_event_by_bid(base_id)

    def get_events_by_tg_id(self, tg_user_id: int) -> list[Type[Event]]:
        return self.event_dao.get_events_by_tg_id(tg_user_id)

    def get_free_events(self) -> list[Type[Event]]:
        return self.event_dao.get_free_events()

    def get_all_events(self) -> list[Type[Event]]:
        return self.event_dao.get_all_events()

    def create_event(self, data: dict) -> Event:
        return self.event_dao.create_event(data)

    def update_event(self, event, data: dict) -> None:
        if "tg_user_id" in data:
            event.tg_user_id = data.get("tg_user_id")
        if "start" in data:
            event.start = data.get("start")
        if "end" in data:
            event.end = data.get("end")
        if "category" in data:
            event.category = data.get("category")
        if "subcategory" in data:
            event.subcategory = data.get("subcategory")
        if "is_free" in data:
            event.is_free = data.get("is_free")

        return self.event_dao.update_event(event)

    def delete_event(self, base_id: int) -> None:
        return self.event_dao.delete_event(base_id)
