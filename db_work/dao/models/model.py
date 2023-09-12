from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

users_events = Table(
    "users_events",
    Base.metadata,
    Column("user_id", Integer(), ForeignKey("user.id")),
    Column("event_id", Integer(), ForeignKey("event.id"))
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    full_name = Column(String, default=None)
    phone_number = Column(String, default=None)

    events = relationship('Event', secondary=users_events, backref='users')

    def __repr__(self):
        info = f"User(id={self.id}, tg_id={self.tg_id}, full_name="

        if self.full_name:
            info += f"'{self.full_name}', phone_number="
        else:
            info += f"{self.full_name}, phone_number="

        if self.phone_number:
            info += f"'{self.phone_number}'"
        else:
            info += f"{self.phone_number}"

        return info


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    start = Column(String(25))
    end = Column(String(25))
    category = Column(String)
    subcategory = Column(String)
    # is_free = Column(Boolean, default=True)

    def __repr__(self):
        info = f"Event(id={self.id}, start='{self.start}', end='{self.end}', category='{self.category}', subcategory="

        if self.subcategory:
            info += f"'{self.subcategory}')"
        else:
            info += f"{self.subcategory})"

        return info
