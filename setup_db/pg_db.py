from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_work.dao.models.model import Base

engine = create_engine('postgresql://user:password@pg/db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
