from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy base class
Base = declarative_base()

# Database connection URL
DATABASE_URL = 'mysql+pymysql://root:password@localhost/pizza_project'  # Replace with your credentials

# Create engine
engine = create_engine(DATABASE_URL, echo=True)
