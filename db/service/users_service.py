from sqlalchemy.orm import Session
from db.model import Users
from db.dao.users_dao import UsersDAO


class UsersService:
    def __init__(self, session: Session):
        self.users_dao = UsersDAO(session)

    def get_user_by_tg_id(self, user_id_tg: int) -> Users:
        return self.users_dao.get_user_by_tg_id(user_id_tg)
