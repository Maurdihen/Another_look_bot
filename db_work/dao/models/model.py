from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id_tg = Column(Integer)
    full_name = Column(String, default=None)
    phone_number = Column(String, default=None)


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id_tg'))
    event_id = Column(String)
    start = Column(String(8))
    end = Column(String(8))
    category = Column(String)
    subcategory = Column(String)

    user = relationship("User", back_populates="note")


User.notes = relationship("Note", back_populates="user")
