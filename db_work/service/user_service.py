from typing import Type

from sqlalchemy.orm import Session
from db_work.dao.models.model import User
from db_work.dao.user_dao import UserDAO


class UserService:
    def __init__(self, session: Session):
        self.user_dao = UserDAO(session)

    def get_user_by_bid(self, base_id: int) -> User:
        return self.user_dao.get_user_by_bid(base_id)

    def get_user_by_tg_id(self, tg_id: int) -> Type[User] | None:
        return self.user_dao.get_user_by_tg_id(tg_id)

    def create_user(self, data) -> User:
        return self.user_dao.create_user(data)

    def update_user(self, user, data) -> None:
        if data.get("full_name"):
            user.full_name = data["full_name"]
        if data.get("phone_number"):
            user.phone_number = data["phone_number"]

        self.user_dao.update_user(user)
