# db_setup.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "mysql+mysqlconnector://root:password@localhost/pizza_project"

def setup_database():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    setup_database()
