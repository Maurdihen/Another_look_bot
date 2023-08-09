from sqlalchemy.orm import Session
from db_work.dao.models.model import User


class UserDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_tg_id(self, user_id_tg: int) -> User:
        return self.session.query(User).filter_by(user_id_tg=user_id_tg).first()

    def create_user(self, data) -> User:
        new_user = User(**data)

        self.session.add(new_user)
        self.session.commit()

        return new_user

    def update_user(self, data) -> User:
        user = self.get_user_by_tg_id(data["user_id_tg"])
        if user:
            if data.get("full_name"):
                user.full_name = data["full_name"]
            if data.get("phone_number"):
                user.phone_number = data["phone_number"]

            self.session.commit()
            return user

    def delete_user(self, user_id_tg: int) -> None:
        user = self.get_user_by_tg_id(user_id_tg)
        if user:
            self.session.delete(user)
            self.session.commit()
