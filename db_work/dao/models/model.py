from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    full_name = Column(String, default=None)
    phone_number = Column(String, default=None)


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    tg_user_id = Column(Integer, ForeignKey('user.tg_id'))
    start = Column(String(25), nullable=False)
    end = Column(String(25), nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, default=None)
    is_free = Column(Boolean, default=True)
#     user = relationship("User", back_populates="event")
#
#
# User.notes = relationship("Event", back_populates="user")
