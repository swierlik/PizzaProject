from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLAlchemy base class
Base = declarative_base()

# Database connection URL
DATABASE_URL = 'mysql+pymysql://root:password@localhost/pizza_project'

# Create engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session object
session = Session()

# Function to create all tables
def create_all_tables():
    Base.metadata.create_all(engine)
