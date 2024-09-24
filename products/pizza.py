from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from db import Base, session
from sqlalchemy.exc import SQLAlchemyError
from products.pizzaIngredient import add_pizza_ingredient
from products.ingredient import get_price, is_vegetarian, is_vegan

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
        price = 0.0
        all_ingredients_vegetarian = True  # Rename to avoid conflict with the function
        all_ingredients_vegan = True  # Rename to avoid conflict with the function
        
        for ingredient_id in ingredients:
            price += get_price(ingredient_id)
            if not is_vegetarian(ingredient_id):  # Use `not` for better readability
                all_ingredients_vegetarian = False
            if not is_vegan(ingredient_id):
                all_ingredients_vegan = False
        
        price *= 1.40 * 1.09  # 40% profit margin and 9% tax

        # Step 1: Add the new pizza
        new_pizza = Pizza(
            Name=name,
            Description=description,
            Price=price,
            IsVegetarian=all_ingredients_vegetarian,  # Use renamed variable
            IsVegan=all_ingredients_vegan  # Use renamed variable
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
