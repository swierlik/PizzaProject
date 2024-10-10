from Products.IngredientManagement import get_price_ingredient, is_vegan_ingredient, is_vegetarian_ingredient
from models.Ingredient import Ingredient
from models.PizzaIngredient import PizzaIngredient
from models.Pizza import Pizza
from db import session
from sqlalchemy.exc import SQLAlchemyError


def add_pizza(name, ingredients, description_preset=None, set_price=999):
    try:
        price = 0.0
        all_ingredients_vegetarian = True  # Rename to avoid conflict with the function
        all_ingredients_vegan = True  # Rename to avoid conflict with the function
        
        description=""

        for ingredient_id in ingredients:
            price += get_price_ingredient(ingredient_id)
            description += f'{get_ingredient_name(ingredient_id)}, '
            if not is_vegetarian_ingredient(ingredient_id):  # Use `not` for better readability
                all_ingredients_vegetarian = False
            if not is_vegan_ingredient(ingredient_id):
                all_ingredients_vegan = False

        if description_preset:
            description = description_preset
        
        price *= 1.40 * 1.09  # 40% profit margin and 9% tax

        # Step 1: Add the new pizza
        new_pizza = Pizza(
            Name=name,
            Description=description,
            Price=min(price, set_price),
            IsVegetarian=all_ingredients_vegetarian,  # Use renamed variable
            IsVegan=all_ingredients_vegan  # Use renamed variable
        )
        session.add(new_pizza)
        session.commit()


        # Step 2: Get the PizzaID of the newly created pizza
        pizza_id = new_pizza.PizzaID

        # Step 3: Add each ingredient from the ingredients list to the PizzaIngredient table
        for ingredient_id in ingredients:
            session.add(make_pizza_ingredient(pizza_id, ingredient_id))

        session.commit()
        print(f"Pizza '{name}' added to the database with ingredients.")
    
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error occurred: {e}")

def get_price_pizza(pizzaID):
    pizza = session.query(Pizza).filter(Pizza.PizzaID == pizzaID).first()
    return float(pizza.Price)

def make_pizza_ingredient(pizza_id, ingredient_id):
    new_pizza_ingredient = PizzaIngredient(
        PizzaID=pizza_id,
        IngredientID=ingredient_id
    )
    return new_pizza_ingredient

def get_ingredient_name(ingredientID):
    ingredient=session.query(Ingredient).filter(Ingredient.IngredientID == ingredientID).first()
    return ingredient.Name