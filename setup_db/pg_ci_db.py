from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_work.dao.models.model import Base

engine = create_engine('postgresql://$DB_USER:$DB_PASSWORD@pg/$DB_NAME')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
