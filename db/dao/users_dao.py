from sqlalchemy.orm import Session
from db.dao.model.model import Users

class UsersDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_tg_id(self, user_id_tg: int) -> Users:
        return self.session.query(Users).filter_by(user_id_tg=user_id_tg).first()

    def create_user(self, user_id_tg: int, name: str) -> Users:
        new_user = Users(user_id_tg=user_id_tg, name=name)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def delete_user(self, user_id_tg: int) -> None:
        user = self.get_user_by_tg_id(user_id_tg)
        if user:
            self.session.delete(user)
            self.session.commit()

    def update_user_name(self, user_id_tg: int, new_name: str) -> Users:
        user = self.get_user_by_tg_id(user_id_tg)
        if user:
            user.name = new_name
            self.session.commit()
            return user
