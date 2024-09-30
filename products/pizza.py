from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from db import Base, session
from sqlalchemy.exc import SQLAlchemyError
from products.pizzaIngredient import add_pizza_ingredient
from products.ingredient import get_price, is_vegetarian, is_vegan
from .pizzaIngredient import PizzaIngredient
from .ingredient import Ingredient  # Import Ingredient here


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
# products/pizza.py

def add_pizza(name, description, ingredient_ids):
    from db import session  # Import session inside the function
    price = 0.0
    is_vegetarian = True
    is_vegan = True

    # Calculate the total price and determine dietary restrictions
    for ingredient_id in ingredient_ids:
        ingredient = session.query(Ingredient).get(ingredient_id)
        if ingredient is None:
            raise ValueError(f"Ingredient with ID {ingredient_id} not found.")
        price += float(ingredient.Cost)
        if not ingredient.isVegetarian:
            is_vegetarian = False
        if not ingredient.isVegan:
            is_vegan = False

    # Create a new pizza
    new_pizza = Pizza(
        Name=name,
        Description=description,
        Price=price,
        IsVegetarian=is_vegetarian,
        IsVegan=is_vegan
    )
    session.add(new_pizza)
    session.commit()  # Commit to get the PizzaID

    # Associate ingredients with the new pizza
    for ingredient_id in ingredient_ids:
        pizza_ingredient = PizzaIngredient(
            PizzaID=new_pizza.PizzaID,
            IngredientID=ingredient_id
        )
        session.add(pizza_ingredient)
    session.commit()

    print(f"Pizza '{name}' added to the database with price {price:.2f}.")

def get_price(ingredient_id):
    from db import session
    ingredient = session.query(Ingredient).get(ingredient_id)
    if ingredient is None:
        raise ValueError(f"Ingredient with ID {ingredient_id} not found.")
    return float(ingredient.Cost)