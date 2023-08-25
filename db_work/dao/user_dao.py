from sqlalchemy.orm import Session
from db_work.dao.models.model import User


class UserDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def get_user_by_tg_id(self, user_id_tg: int) -> User:
        return self.session.query(User).filter_by(user_id_tg=user_id_tg).first()

    def create_user(self, data) -> User:
        new_user = User(**data)

        self.session.add(new_user)
        self.session.commit()

        return new_user

    def update_user(self, user) -> None:
        self.session.add(user)
        self.session.commit()
