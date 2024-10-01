# products/dessert.py
from sqlalchemy import Column, Integer, String, DECIMAL
from database import Base

# Define the Dessert class
class Dessert(Base):
    __tablename__ = 'desserts'
    
    DessertID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)