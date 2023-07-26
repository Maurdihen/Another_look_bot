from sqlalchemy.orm import Session
from db.dao.model.model import Users
from db.dao.users_dao import UsersDAO

class UsersService:
    def __init__(self, session: Session):
        self.users_dao = UsersDAO(session)

    def get_user_by_tg_id(self, user_id_tg: int) -> Users:
        return self.users_dao.get_user_by_tg_id(user_id_tg)

    def create_user(self, user_id_tg: int, name: str) -> Users:
        return self.users_dao.create_user(user_id_tg, name)

    def delete_user(self, user_id_tg: int) -> None:
        return self.users_dao.delete_user(user_id_tg)

    def update_user_name(self, user_id_tg: int, new_name: str) -> Users:
        return self.users_dao.update_user_name(user_id_tg, new_name)
