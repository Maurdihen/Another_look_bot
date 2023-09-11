from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

users_events = Table(
    "users_events",
    Column("user_id", Integer(), ForeignKey("user.id")),
    Column("event_id", Integer(), ForeignKey("event.id"))
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    full_name = Column(String, default=None)
    phone_number = Column(String, default=None)

    events = relationship('Event', secondary=users_events, backref=backref('user', lazy='dynamic'))


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    start = Column(String(8))
    end = Column(String(8))
    category = Column(String)
    subcategory = Column(String)
    is_free = Column(Boolean, default=True)

    users = relationship('User', secondary=users_events, backref=backref('event', lazy='dynamic'))
