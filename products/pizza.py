from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from db import Base, session
from sqlalchemy.exc import SQLAlchemyError
from products.pizzaIngredient import add_pizza_ingredient
from products.ingredient import get_price

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
def add_pizza(name, description, ingredients):
    try:
        price=0.0
        for ingredient_id in ingredients:
            price+=get_price(ingredient_id)
        price

        # Step 1: Add the new pizza
        new_pizza = Pizza(
            Name=name,
            Description=description,
            Price=price,
            IsVegetarian=is_vegetarian,
            IsVegan=is_vegan
        )
        session.add(new_pizza)
        session.commit()

        # Step 2: Get the PizzaID of the newly created pizza
        pizza_id = new_pizza.PizzaID

        # Step 3: Add each ingredient from the ingredients list to the PizzaIngredient table
        for ingredient_id in ingredients:
            add_pizza_ingredient(pizza_id, ingredient_id)


        session.commit()
        print(f"Pizza '{name}' added to the database with ingredients.")
    
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error occurred: {e}")