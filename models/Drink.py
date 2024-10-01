# products/drink.py
from sqlalchemy import Column, Integer, String, DECIMAL
from database import Base

# Define the Drink class
class Drink(Base):
    __tablename__ = 'drinks'
    
    DrinkID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)


