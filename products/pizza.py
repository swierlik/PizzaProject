# products/pizza.py
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from db import Base, session

# Define the Pizza class
class Pizza(Base):
    __tablename__ = 'Pizza'
    
    PizzaID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Description = Column(String(255))
    Price = Column(DECIMAL(10, 2), nullable=False)
    IsVegetarian = Column(Boolean, default=False)
    IsVegan = Column(Boolean, default=False)

# Function to add pizza items
def add_pizza(name, description, price, is_vegetarian=False, is_vegan=False):
    new_pizza = Pizza(
        Name=name,
        Description=description,
        Price=price,
        IsVegetarian=is_vegetarian,
        IsVegan=is_vegan
    )
    session.add(new_pizza)
    session.commit()
    print(f"Pizza '{name}' added to the database.")
