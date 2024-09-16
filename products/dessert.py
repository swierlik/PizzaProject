# products/dessert.py
from sqlalchemy import Column, Integer, String, DECIMAL
from db import Base, session

# Define the Dessert class
class Dessert(Base):
    __tablename__ = 'Dessert'
    
    DessertID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)

# Function to add dessert items
def add_dessert(name, price):
    new_dessert = Dessert(
        Name=name,
        Price=price
    )
    session.add(new_dessert)
    session.commit()
    print(f"Dessert '{name}' added to the database.")
