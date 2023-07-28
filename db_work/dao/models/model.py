from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
    subcategory = Column(String)

    user = relationship("Users", back_populates="notes")


Users.notes = relationship("Notes", back_populates="user")
