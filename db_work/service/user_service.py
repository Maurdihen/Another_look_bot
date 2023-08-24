from sqlalchemy.orm import Session
from db_work.dao.models.model import User
from db_work.dao.user_dao import UserDAO


class UserService:
    def __init__(self, session: Session):
        self.user_dao = UserDAO(session)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_dao.get_user_by_id(user_id)

    def get_user_by_tg_id(self, user_id_tg: int) -> User:
        return self.user_dao.get_user_by_tg_id(user_id_tg)

    def create_user(self, data) -> User:
        return self.user_dao.create_user(data)

    def update_user(self, data) -> None:
        user = self.get_user_by_tg_id(data["user_id_tg"])

        if data.get("full_name"):
            user.full_name = data["full_name"]
        if data.get("phone_number"):
            user.phone_number = data["phone_number"]

        self.user_dao.update_user(user)

    def delete_user(self, user_id_tg: int) -> None:
        # Аналогично, нужна ли функиця?
        self.user_dao.delete_user(user_id_tg)
