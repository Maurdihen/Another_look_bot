from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db_work.setup_db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id_tg = Column(Integer)
    name = Column(String)


class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(String)
    time = Column(String)
    category = Column(String)
    sub_category = Column(String)

    user = relationship("Users", back_populates="notes")


Users.notes = relationship("Notes", back_populates="user")
