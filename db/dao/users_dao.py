from sqlalchemy.orm import Session
from db.model import Users


class UsersDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_tg_id(self, user_id_tg: int) -> Users:
        return self.session.query(Users).filter_by(user_id_tg=user_id_tg).first()
