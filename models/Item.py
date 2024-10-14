from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from database import Base

# Define the Pizza class
class Item(Base):
    __tablename__ = 'items'
    
    ItemID = Column(Integer, primary_key=True, autoincrement=True)
    ItemType = Column(String(255), nullable=False)
    Name = Column(String(255), nullable=False)
    Description = Column(String(255))
    Price = Column(DECIMAL(10, 2), nullable=False)
    IsVegetarian = Column(Boolean, default=False)
    IsVegan = Column(Boolean, default=False)