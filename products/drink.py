# products/drink.py
from sqlalchemy import Column, Integer, String, DECIMAL
from db import Base, session

# Define the Drink class
class Drink(Base):
    __tablename__ = 'Drink'
    
    DrinkID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)

# Function to add drink items
def add_drink(name, price):
    new_drink = Drink(
        Name=name,
        Price=price
    )
    session.add(new_drink)
    session.commit()
    print(f"Drink '{name}' added to the database.")
